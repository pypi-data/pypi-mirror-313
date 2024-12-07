from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.dashboard import Dashboard
from ...models.dashboard_request import DashboardRequest
from ...types import Response


def _get_kwargs(
    project_id: str,
    dashboard_id: str,
    *,
    body: DashboardRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/projects/{project_id}/dashboards/{dashboard_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Dashboard]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Dashboard.from_dict(response.json())

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[Dashboard]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    dashboard_id: str,
    *,
    client: Client,
    body: DashboardRequest,
) -> Response[Dashboard]:
    """Update dashboard

     Updates a dashboard

    Args:
        project_id (str):
        dashboard_id (str):
        body (DashboardRequest):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Dashboard]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        dashboard_id=dashboard_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        auth=client.get_auth(),
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    dashboard_id: str,
    *,
    client: Client,
    body: DashboardRequest,
) -> Optional[Dashboard]:
    """Update dashboard

     Updates a dashboard

    Args:
        project_id (str):
        dashboard_id (str):
        body (DashboardRequest):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Dashboard
    """

    try:
        return sync_detailed(
            project_id=project_id,
            dashboard_id=dashboard_id,
            client=client,
            body=body,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    project_id: str,
    dashboard_id: str,
    *,
    client: Client,
    body: DashboardRequest,
) -> Response[Dashboard]:
    """Update dashboard

     Updates a dashboard

    Args:
        project_id (str):
        dashboard_id (str):
        body (DashboardRequest):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Dashboard]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        dashboard_id=dashboard_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    dashboard_id: str,
    *,
    client: Client,
    body: DashboardRequest,
) -> Optional[Dashboard]:
    """Update dashboard

     Updates a dashboard

    Args:
        project_id (str):
        dashboard_id (str):
        body (DashboardRequest):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Dashboard
    """

    try:
        return (
            await asyncio_detailed(
                project_id=project_id,
                dashboard_id=dashboard_id,
                client=client,
                body=body,
            )
        ).parsed
    except errors.NotFoundException:
        return None
