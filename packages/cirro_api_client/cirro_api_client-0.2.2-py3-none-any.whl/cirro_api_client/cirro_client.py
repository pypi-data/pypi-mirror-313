import importlib.metadata
import platform

from attrs import define, field

from cirro_api_client.cirro_auth import AuthMethod
from cirro_api_client.v1.client import Client


def _get_user_agent(package_name: str, client_name: str) -> str:
    try:
        pkg_version = importlib.metadata.version(package_name)
    except (importlib.metadata.PackageNotFoundError, ValueError):
        pkg_version = "Unknown"
    python_version = platform.python_version()
    return f"{client_name} {pkg_version} (Python {python_version})"


# noinspection PyUnresolvedReferences
@define
class CirroApiClient(Client):
    """A class for interacting with the Cirro API

    Attributes:
        auth_method: The method used to authenticate API requests

        base_url: The base URL for the API, all requests are made to a relative path to this URL

        cookies: A dictionary of cookies to be sent with every request

        headers: A dictionary of headers to be sent with every request

        timeout: The maximum amount of a time a request can take. API functions will raise
        httpx.TimeoutException if this is exceeded.

        verify_ssl: Whether to verify the SSL certificate of the API server. This should be True in production,
        but can be set to False for testing purposes.

        follow_redirects: Whether to follow redirects. Default value is False.

        httpx_args: A dictionary of additional arguments to be passed to the ``httpx.Client`` and ``httpx.AsyncClient`` constructor.

        raise_on_unexpected_status: Whether to raise an errors.UnexpectedStatus if the API returns a
                status code that was not documented in the source OpenAPI document. Can also be provided as a keyword
                argument to the constructor.
    """

    auth_method: AuthMethod
    raise_on_unexpected_status: bool = field(default=True, kw_only=True)
    client_name: str = field(kw_only=True, default="Cirro API Client")
    package_name: str = field(kw_only=True, default="cirro-api-client")

    def __attrs_post_init__(self):
        self._headers["User-Agent"] = _get_user_agent(self.package_name, self.client_name)
