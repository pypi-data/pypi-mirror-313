from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.user_detail import UserDetail
from ...types import Response


def _get_kwargs(
    username: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/users/{username}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[UserDetail]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UserDetail.from_dict(response.json())

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[UserDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    username: str,
    *,
    client: Client,
) -> Response[UserDetail]:
    """Get user

     Get user information

    Args:
        username (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserDetail]
    """

    kwargs = _get_kwargs(
        username=username,
    )

    response = client.get_httpx_client().request(
        auth=client.get_auth(),
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    username: str,
    *,
    client: Client,
) -> Optional[UserDetail]:
    """Get user

     Get user information

    Args:
        username (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserDetail
    """

    try:
        return sync_detailed(
            username=username,
            client=client,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    username: str,
    *,
    client: Client,
) -> Response[UserDetail]:
    """Get user

     Get user information

    Args:
        username (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserDetail]
    """

    kwargs = _get_kwargs(
        username=username,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    username: str,
    *,
    client: Client,
) -> Optional[UserDetail]:
    """Get user

     Get user information

    Args:
        username (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserDetail
    """

    try:
        return (
            await asyncio_detailed(
                username=username,
                client=client,
            )
        ).parsed
    except errors.NotFoundException:
        return None
