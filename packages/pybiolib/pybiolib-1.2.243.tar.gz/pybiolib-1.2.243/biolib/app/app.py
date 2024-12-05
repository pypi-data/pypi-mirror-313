import io
import json
import os
import random
import string
from pathlib import Path

from biolib import utils
from biolib.biolib_api_client import JobState
from biolib.biolib_api_client.app_types import App, AppVersion
from biolib.biolib_api_client.biolib_app_api import BiolibAppApi
from biolib.biolib_api_client.biolib_job_api import BiolibJobApi
from biolib.biolib_binary_format import ModuleInput
from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger
from biolib.compute_node.job_worker.job_worker import JobWorker
from biolib.experiments.experiment import Experiment
from biolib.jobs import Job
from biolib.typing_utils import Optional
from biolib.utils.app_uri import parse_app_uri


class BioLibApp:
    def __init__(self, uri: str):
        app_response = BiolibAppApi.get_by_uri(uri)
        self._app: App = app_response['app']
        self._app_uri = app_response['app_uri']
        self._app_version: AppVersion = app_response['app_version']

        logger.info(f'Loaded project {self._app_uri}')

    def __str__(self) -> str:
        return self._app_uri

    @property
    def uri(self) -> str:
        return self._app_uri

    @property
    def uuid(self) -> str:
        return self._app['public_id']

    @property
    def version(self) -> AppVersion:
        return self._app_version

    def cli(
        self,
        args=None,
        stdin=None,
        files=None,
        override_command=False,
        machine='',
        blocking: bool = True,
        experiment_id: Optional[str] = None,
        result_prefix: Optional[str] = None,
        timeout: Optional[int] = None,
        notify: bool = False,
        machine_count: Optional[int] = None,
        experiment: Optional[str] = None,
    ) -> Job:
        if experiment_id and experiment:
            raise ValueError('Only one of experiment_id and experiment can be specified')

        if not experiment_id:
            experiment_instance = Experiment(experiment) if experiment else Experiment.get_experiment_in_context()
            experiment_id = experiment_instance.uuid if experiment_instance else None

        module_input_serialized = self._get_serialized_module_input(args, stdin, files)

        if machine == 'local':
            if not blocking:
                raise BioLibError('The argument "blocking" cannot be False when running locally')

            if experiment_id:
                logger.warning('The argument "experiment_id" is ignored when running locally')

            if result_prefix:
                logger.warning('The argument "result_prefix" is ignored when running locally')

            return self._run_locally(module_input_serialized)

        job = Job._start_job_in_cloud(  # pylint: disable=protected-access
            app_uri=self._app_uri,
            app_version_uuid=self._app_version['public_id'],
            experiment_id=experiment_id,
            machine=machine,
            module_input_serialized=module_input_serialized,
            notify=notify,
            override_command=override_command,
            result_prefix=result_prefix,
            timeout=timeout,
            requested_machine_count=machine_count,
        )
        if blocking:
            # TODO: Deprecate utils.STREAM_STDOUT and always stream logs by simply calling job.stream_logs()
            if utils.IS_RUNNING_IN_NOTEBOOK:
                utils.STREAM_STDOUT = True

            enable_print = bool(
                utils.STREAM_STDOUT
                and (self._app_version.get('main_output_file') or self._app_version.get('stdout_render_type') == 'text')
            )
            job._stream_logs(enable_print=enable_print)  # pylint: disable=protected-access

        return job

    def exec(self, args=None, stdin=None, files=None, machine=''):
        return self.cli(args, stdin, files, override_command=True, machine=machine)

    def __call__(self, *args, **kwargs):
        if not args and not kwargs:
            self.cli()

        else:
            raise BioLibError("""
Calling an app directly with app() is currently being reworked.
To use the previous functionality, please call app.cli() instead. 
Example: "app.cli('--help')"
""")

    @staticmethod
    def _get_serialized_module_input(args=None, stdin=None, files=None) -> bytes:
        if args is None:
            args = []

        if stdin is None:
            stdin = b''

        if isinstance(args, str):
            args = list(filter(lambda p: p != '', args.split(' ')))

        if not isinstance(args, list):
            raise Exception('The given input arguments must be list or str')

        if isinstance(stdin, str):
            stdin = stdin.encode('utf-8')

        if files is None:
            files = []

        files_dict = {}
        for idx, arg in enumerate(args):
            if isinstance(arg, str):
                if os.path.isfile(arg) or os.path.isdir(arg):
                    files.append(arg)
                    args[idx] = Path(arg).name

                # support --myarg=file.txt
                elif os.path.isfile(arg.split('=')[-1]) or os.path.isdir(arg.split('=')[-1]):
                    files.append(arg.split('=')[-1])
                    args[idx] = arg.split('=')[0] + '=' + Path(arg.split('=')[-1]).name
                else:
                    pass  # a normal string arg was given
            else:
                tmp_filename = f'input_{"".join(random.choices(string.ascii_letters + string.digits, k=7))}'
                if isinstance(arg, io.StringIO):
                    file_data = arg.getvalue().encode()
                elif isinstance(arg, io.BytesIO):
                    file_data = arg.getvalue()
                else:
                    raise Exception(f'Unexpected type of argument: {arg}')
                files_dict[f'/{tmp_filename}'] = file_data
                args[idx] = tmp_filename

        if isinstance(files, list):
            for file in files:
                path = Path(file).absolute()

                # Recursively add data from files if dir
                if path.is_dir():
                    for filename in path.rglob('*'):
                        if filename.is_dir():
                            continue
                        file = open(filename, 'rb')
                        relative_path = '/' + path.name + '/' + '/'.join(filename.relative_to(path).parts)
                        files_dict[relative_path] = file.read()
                        file.close()

                # Add file data
                else:
                    file = open(path, 'rb')
                    path_short = '/' + path.name

                    files_dict[path_short] = file.read()
                    file.close()

        elif isinstance(files, dict):
            files_dict.update(files)
        else:
            raise Exception('The given files input must be list or dict or None')

        module_input_serialized: bytes = ModuleInput().serialize(
            stdin=stdin,
            arguments=args,
            files=files_dict,
        )
        return module_input_serialized

    def _run_locally(self, module_input_serialized: bytes) -> Job:
        job_dict = BiolibJobApi.create(
            app_version_id=self._app_version['public_id'],
            app_resource_name_prefix=parse_app_uri(self._app_uri)['resource_name_prefix'],
        )
        job = Job(job_dict)

        try:
            BiolibJobApi.update_state(job.id, JobState.IN_PROGRESS)
            module_output = JobWorker().run_job_locally(job_dict, module_input_serialized)
            job._set_result_module_output(module_output)  # pylint: disable=protected-access
            BiolibJobApi.update_state(job.id, JobState.COMPLETED)
        except BaseException as error:
            BiolibJobApi.update_state(job.id, JobState.FAILED)
            raise error

        return job

    def run(self, **kwargs) -> Job:
        args = []
        biolib_kwargs = {}
        for key, value in kwargs.items():
            if key.startswith('biolib_'):
                biolib_kwarg_key = key.replace('biolib_', '')
                biolib_kwargs[biolib_kwarg_key] = value
                continue

            if isinstance(value, dict):
                value = io.StringIO(json.dumps(value))

            if not key.startswith('--'):
                key = f'--{key}'

            args.append(key)
            if isinstance(value, list):
                # TODO: only do this if argument key is of type file list
                args.extend(value)
            else:
                args.append(value)

        return self.cli(args, **biolib_kwargs)

    def start(self, **kwargs) -> Job:
        return self.run(biolib_blocking=False, **kwargs)
