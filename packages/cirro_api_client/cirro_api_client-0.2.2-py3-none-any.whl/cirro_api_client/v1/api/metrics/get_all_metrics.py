from http import HTTPStatus
from typing import Any, Dict, List, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.project_metrics import ProjectMetrics
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/metrics",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[List["ProjectMetrics"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ProjectMetrics.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[List["ProjectMetrics"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[List["ProjectMetrics"]]:
    """Get all project metrics

     Retrieves metrics for all projects.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ProjectMetrics']]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        auth=client.get_auth(),
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
) -> Optional[List["ProjectMetrics"]]:
    """Get all project metrics

     Retrieves metrics for all projects.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ProjectMetrics']
    """

    try:
        return sync_detailed(
            client=client,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[List["ProjectMetrics"]]:
    """Get all project metrics

     Retrieves metrics for all projects.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ProjectMetrics']]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[List["ProjectMetrics"]]:
    """Get all project metrics

     Retrieves metrics for all projects.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ProjectMetrics']
    """

    try:
        return (
            await asyncio_detailed(
                client=client,
            )
        ).parsed
    except errors.NotFoundException:
        return None
