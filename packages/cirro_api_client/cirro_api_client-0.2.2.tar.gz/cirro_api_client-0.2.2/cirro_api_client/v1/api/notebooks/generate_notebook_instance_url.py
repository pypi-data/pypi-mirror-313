from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.open_notebook_instance_response import OpenNotebookInstanceResponse
from ...types import Response


def _get_kwargs(
    project_id: str,
    notebook_instance_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/notebook-instances/{notebook_instance_id}:generate-url",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[OpenNotebookInstanceResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = OpenNotebookInstanceResponse.from_dict(response.json())

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[OpenNotebookInstanceResponse]:
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
) -> Response[OpenNotebookInstanceResponse]:
    """Generate notebook instance URL

     Creates an authenticated URL to open up the notebook instance in your browser

    Args:
        project_id (str):
        notebook_instance_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OpenNotebookInstanceResponse]
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


def sync(
    project_id: str,
    notebook_instance_id: str,
    *,
    client: Client,
) -> Optional[OpenNotebookInstanceResponse]:
    """Generate notebook instance URL

     Creates an authenticated URL to open up the notebook instance in your browser

    Args:
        project_id (str):
        notebook_instance_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OpenNotebookInstanceResponse
    """

    try:
        return sync_detailed(
            project_id=project_id,
            notebook_instance_id=notebook_instance_id,
            client=client,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    project_id: str,
    notebook_instance_id: str,
    *,
    client: Client,
) -> Response[OpenNotebookInstanceResponse]:
    """Generate notebook instance URL

     Creates an authenticated URL to open up the notebook instance in your browser

    Args:
        project_id (str):
        notebook_instance_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OpenNotebookInstanceResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        notebook_instance_id=notebook_instance_id,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    notebook_instance_id: str,
    *,
    client: Client,
) -> Optional[OpenNotebookInstanceResponse]:
    """Generate notebook instance URL

     Creates an authenticated URL to open up the notebook instance in your browser

    Args:
        project_id (str):
        notebook_instance_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OpenNotebookInstanceResponse
    """

    try:
        return (
            await asyncio_detailed(
                project_id=project_id,
                notebook_instance_id=notebook_instance_id,
                client=client,
            )
        ).parsed
    except errors.NotFoundException:
        return None
