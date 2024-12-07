"""Contains shared errors types that can be raised from API functions"""

from http import HTTPStatus
from typing import Dict

import httpx

from cirro_api_client.v1.models import PortalErrorResponse


def handle_error_response(response: httpx.Response, raise_on_unexpected_status: bool) -> None:
    """Parses a response from the server and returns an exception if the response indicates an error"""
    if response.status_code == HTTPStatus.BAD_REQUEST:
        raise BadRequestException(response.json())

    if response.status_code == HTTPStatus.NOT_FOUND:
        raise NotFoundException(response.json())

    if response.status_code == HTTPStatus.FORBIDDEN:
        raise ForbiddenException(response.json())

    if raise_on_unexpected_status:
        raise UnexpectedStatus(response.status_code, response.content)


class UnexpectedStatus(Exception):
    """Raised by api functions when the response status an undocumented status and Client.raise_on_unexpected_status is True"""

    def __init__(self, status_code: int, content: bytes):
        self.status_code = status_code
        self.content = content

        super().__init__(
            f"Unexpected status code: {status_code}\n\nResponse content:\n{content.decode(errors='ignore')}"
        )


class CirroException(Exception):
    """Raised when the server returns a known error response"""

    def __init__(self, error_response_data: Dict):
        self.error_response = PortalErrorResponse.from_dict(error_response_data)

        super().__init__(self.error_response.error_detail)


class NotFoundException(CirroException):
    """Raised when the item requested is not found"""


class BadRequestException(CirroException):
    """Raised when request is invalid"""


class ForbiddenException(CirroException):
    """Raised when the user is not authorized to perform the requested action"""


__all__ = ["UnexpectedStatus", "NotFoundException", "BadRequestException", "ForbiddenException"]
