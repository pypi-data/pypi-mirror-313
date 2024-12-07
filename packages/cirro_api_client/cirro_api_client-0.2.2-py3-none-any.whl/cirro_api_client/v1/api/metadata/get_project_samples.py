from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.paginated_response_sample_dto import PaginatedResponseSampleDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    *,
    limit: Union[Unset, int] = 5000,
    next_token: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["limit"] = limit

    params["nextToken"] = next_token

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/samples",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[PaginatedResponseSampleDto]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PaginatedResponseSampleDto.from_dict(response.json())

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[PaginatedResponseSampleDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 5000,
    next_token: Union[Unset, str] = UNSET,
) -> Response[PaginatedResponseSampleDto]:
    """Get project samples

     Retrieves a list of samples associated with a project along with their metadata

    Args:
        project_id (str):
        limit (Union[Unset, int]):  Default: 5000.
        next_token (Union[Unset, str]):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedResponseSampleDto]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        limit=limit,
        next_token=next_token,
    )

    response = client.get_httpx_client().request(
        auth=client.get_auth(),
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 5000,
    next_token: Union[Unset, str] = UNSET,
) -> Optional[PaginatedResponseSampleDto]:
    """Get project samples

     Retrieves a list of samples associated with a project along with their metadata

    Args:
        project_id (str):
        limit (Union[Unset, int]):  Default: 5000.
        next_token (Union[Unset, str]):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedResponseSampleDto
    """

    try:
        return sync_detailed(
            project_id=project_id,
            client=client,
            limit=limit,
            next_token=next_token,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    project_id: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 5000,
    next_token: Union[Unset, str] = UNSET,
) -> Response[PaginatedResponseSampleDto]:
    """Get project samples

     Retrieves a list of samples associated with a project along with their metadata

    Args:
        project_id (str):
        limit (Union[Unset, int]):  Default: 5000.
        next_token (Union[Unset, str]):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedResponseSampleDto]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        limit=limit,
        next_token=next_token,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 5000,
    next_token: Union[Unset, str] = UNSET,
) -> Optional[PaginatedResponseSampleDto]:
    """Get project samples

     Retrieves a list of samples associated with a project along with their metadata

    Args:
        project_id (str):
        limit (Union[Unset, int]):  Default: 5000.
        next_token (Union[Unset, str]):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedResponseSampleDto
    """

    try:
        return (
            await asyncio_detailed(
                project_id=project_id,
                client=client,
                limit=limit,
                next_token=next_token,
            )
        ).parsed
    except errors.NotFoundException:
        return None
