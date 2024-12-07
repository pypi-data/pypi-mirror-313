from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.project_access_request import ProjectAccessRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    *,
    include_closed: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["includeClosed"] = include_closed

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/access-requests",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[List["ProjectAccessRequest"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ProjectAccessRequest.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[List["ProjectAccessRequest"]]:
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
    include_closed: Union[Unset, bool] = False,
) -> Response[List["ProjectAccessRequest"]]:
    """Get access requests

     Gets users who have requested access to the project

    Args:
        project_id (str):
        include_closed (Union[Unset, bool]):  Default: False.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ProjectAccessRequest']]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        include_closed=include_closed,
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
    include_closed: Union[Unset, bool] = False,
) -> Optional[List["ProjectAccessRequest"]]:
    """Get access requests

     Gets users who have requested access to the project

    Args:
        project_id (str):
        include_closed (Union[Unset, bool]):  Default: False.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ProjectAccessRequest']
    """

    try:
        return sync_detailed(
            project_id=project_id,
            client=client,
            include_closed=include_closed,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    project_id: str,
    *,
    client: Client,
    include_closed: Union[Unset, bool] = False,
) -> Response[List["ProjectAccessRequest"]]:
    """Get access requests

     Gets users who have requested access to the project

    Args:
        project_id (str):
        include_closed (Union[Unset, bool]):  Default: False.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ProjectAccessRequest']]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        include_closed=include_closed,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: Client,
    include_closed: Union[Unset, bool] = False,
) -> Optional[List["ProjectAccessRequest"]]:
    """Get access requests

     Gets users who have requested access to the project

    Args:
        project_id (str):
        include_closed (Union[Unset, bool]):  Default: False.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ProjectAccessRequest']
    """

    try:
        return (
            await asyncio_detailed(
                project_id=project_id,
                client=client,
                include_closed=include_closed,
            )
        ).parsed
    except errors.NotFoundException:
        return None
