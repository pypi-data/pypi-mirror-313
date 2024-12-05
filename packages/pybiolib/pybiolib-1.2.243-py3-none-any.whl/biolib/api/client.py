from urllib.parse import urlencode, urljoin

import importlib_metadata

from biolib._internal.http_client import HttpClient, HttpResponse
from biolib.biolib_api_client import BiolibApiClient as DeprecatedApiClient
from biolib.typing_utils import Dict, Optional, Union, cast

OptionalHeaders = Union[
    Optional[Dict[str, str]],
    Optional[Dict[str, Union[str, None]]],
]


def _get_biolib_package_version() -> str:
    # try fetching version, if it fails (usually when in dev), add default
    try:
        return cast(str, importlib_metadata.version('pybiolib'))
    except importlib_metadata.PackageNotFoundError:
        return '0.0.0'


class ApiClient(HttpClient):
    _biolib_package_version: str = _get_biolib_package_version()

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Union[str, int]]] = None,
        headers: OptionalHeaders = None,
        authenticate: bool = True,
        retries: int = 10,
    ) -> HttpResponse:
        return self.request(
            headers=self._get_headers(opt_headers=headers, authenticate=authenticate),
            method='GET',
            retries=retries,
            url=self._get_absolute_url(path=path, query_params=params),
        )

    def post(
        self,
        path: str,
        data: Optional[Union[Dict, bytes]] = None,
        headers: OptionalHeaders = None,
        authenticate: bool = True,
        retries: int = 50,  # TODO: reduce this back to 5 when timeout errors have been solved
    ) -> HttpResponse:
        return self.request(
            data=data,
            headers=self._get_headers(opt_headers=headers, authenticate=authenticate),
            method='POST',
            retries=retries,
            url=self._get_absolute_url(path=path, query_params=None),
        )

    def patch(
        self,
        path: str,
        data: Dict,
        headers: OptionalHeaders = None,
        retries: int = 5,
        params: Optional[Dict[str, Union[str, int]]] = None,
    ) -> HttpResponse:
        return self.request(
            data=data,
            headers=self._get_headers(opt_headers=headers, authenticate=True),
            method='PATCH',
            retries=retries,
            url=self._get_absolute_url(path=path, query_params=params),
        )

    @staticmethod
    def _get_headers(opt_headers: OptionalHeaders, authenticate: bool) -> Dict[str, str]:
        # Only keep header keys with a value
        headers: Dict[str, str] = {key: value for key, value in (opt_headers or {}).items() if value}

        deprecated_api_client = DeprecatedApiClient.get()

        if deprecated_api_client.is_signed_in:
            deprecated_api_client.refresh_access_token()

        # Adding access_token outside is_signed_in check as job_worker.py currently sets access_token
        # without setting refresh_token
        access_token = deprecated_api_client.access_token
        if access_token and authenticate:
            headers['Authorization'] = f'Bearer {access_token}'

        headers['client-type'] = 'biolib-python'
        headers['client-version'] = ApiClient._biolib_package_version

        return headers

    @staticmethod
    def _get_absolute_url(path: str, query_params: Optional[Dict[str, Union[str, int]]]) -> str:
        deprecated_api_client = DeprecatedApiClient.get()
        base_api_url = urljoin(deprecated_api_client.base_url, '/api/')
        url = urljoin(base_api_url, path.strip('/') + '/')
        if query_params:
            url = url + '?' + urlencode(query_params)

        return url
