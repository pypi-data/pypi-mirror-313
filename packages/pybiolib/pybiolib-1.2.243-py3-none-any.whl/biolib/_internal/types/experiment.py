from .typing import TypedDict


class ExperimentSlimDict(TypedDict):
    job_count: int
    job_running_count: int


class ExperimentDetailedDict(ExperimentSlimDict):
    pass
