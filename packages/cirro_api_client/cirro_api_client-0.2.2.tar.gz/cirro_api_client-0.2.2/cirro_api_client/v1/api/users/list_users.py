from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.paginated_response_user_dto import PaginatedResponseUserDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    username: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 5000,
    next_token: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_username: Union[None, Unset, str]
    if isinstance(username, Unset):
        json_username = UNSET
    else:
        json_username = username
    params["username"] = json_username

    params["limit"] = limit

    params["nextToken"] = next_token

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/users",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[PaginatedResponseUserDto]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PaginatedResponseUserDto.from_dict(response.json())

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[PaginatedResponseUserDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    username: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 5000,
    next_token: Union[Unset, str] = UNSET,
) -> Response[PaginatedResponseUserDto]:
    """List users

     Gets a list of users, matching an optional username pattern

    Args:
        username (Union[None, Unset, str]):
        limit (Union[Unset, int]):  Default: 5000.
        next_token (Union[Unset, str]):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedResponseUserDto]
    """

    kwargs = _get_kwargs(
        username=username,
        limit=limit,
        next_token=next_token,
    )

    response = client.get_httpx_client().request(
        auth=client.get_auth(),
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    username: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 5000,
    next_token: Union[Unset, str] = UNSET,
) -> Optional[PaginatedResponseUserDto]:
    """List users

     Gets a list of users, matching an optional username pattern

    Args:
        username (Union[None, Unset, str]):
        limit (Union[Unset, int]):  Default: 5000.
        next_token (Union[Unset, str]):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedResponseUserDto
    """

    try:
        return sync_detailed(
            client=client,
            username=username,
            limit=limit,
            next_token=next_token,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    *,
    client: Client,
    username: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 5000,
    next_token: Union[Unset, str] = UNSET,
) -> Response[PaginatedResponseUserDto]:
    """List users

     Gets a list of users, matching an optional username pattern

    Args:
        username (Union[None, Unset, str]):
        limit (Union[Unset, int]):  Default: 5000.
        next_token (Union[Unset, str]):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedResponseUserDto]
    """

    kwargs = _get_kwargs(
        username=username,
        limit=limit,
        next_token=next_token,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    username: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 5000,
    next_token: Union[Unset, str] = UNSET,
) -> Optional[PaginatedResponseUserDto]:
    """List users

     Gets a list of users, matching an optional username pattern

    Args:
        username (Union[None, Unset, str]):
        limit (Union[Unset, int]):  Default: 5000.
        next_token (Union[Unset, str]):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedResponseUserDto
    """

    try:
        return (
            await asyncio_detailed(
                client=client,
                username=username,
                limit=limit,
                next_token=next_token,
            )
        ).parsed
    except errors.NotFoundException:
        return None
