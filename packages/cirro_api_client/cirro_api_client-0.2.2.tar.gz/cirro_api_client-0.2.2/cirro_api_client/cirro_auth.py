import typing
from abc import ABC

from attr import define
from httpx import Auth, Request, Response


class AuthMethod(Auth, ABC):
    """
    Defines the method used for authenticating with Cirro
    """


@define
class TokenAuth(AuthMethod):
    token: str

    def auth_flow(self, request: Request) -> typing.Generator[Request, Response, None]:
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request


@define
class RefreshableTokenAuth(AuthMethod):
    token_getter: typing.Callable[[], str]

    def auth_flow(self, request: Request) -> typing.Generator[Request, Response, None]:
        request.headers["Authorization"] = f"Bearer {self.token_getter()}"
        yield request
