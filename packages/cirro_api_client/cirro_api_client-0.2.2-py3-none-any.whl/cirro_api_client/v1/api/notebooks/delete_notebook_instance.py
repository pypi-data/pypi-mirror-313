from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...types import Response


def _get_kwargs(
    project_id: str,
    notebook_instance_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/projects/{project_id}/notebook-instances/{notebook_instance_id}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.ACCEPTED:
        return None

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    notebook_instance_id: str,
    *,
    client: Client,
) -> Response[Any]:
    """Delete notebook instance

     Triggers a deletion of the notebook instance

    Args:
        project_id (str):
        notebook_instance_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        notebook_instance_id=notebook_instance_id,
    )

    response = client.get_httpx_client().request(
        auth=client.get_auth(),
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    project_id: str,
    notebook_instance_id: str,
    *,
    client: Client,
) -> Response[Any]:
    """Delete notebook instance

     Triggers a deletion of the notebook instance

    Args:
        project_id (str):
        notebook_instance_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        notebook_instance_id=notebook_instance_id,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)
