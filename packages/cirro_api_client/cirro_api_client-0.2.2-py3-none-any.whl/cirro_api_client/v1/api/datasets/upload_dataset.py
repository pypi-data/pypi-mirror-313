from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.upload_dataset_create_response import UploadDatasetCreateResponse
from ...models.upload_dataset_request import UploadDatasetRequest
from ...types import Response


def _get_kwargs(
    project_id: str,
    *,
    body: UploadDatasetRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/projects/{project_id}/datasets/upload",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[UploadDatasetCreateResponse]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = UploadDatasetCreateResponse.from_dict(response.json())

        return response_201

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[UploadDatasetCreateResponse]:
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
    body: UploadDatasetRequest,
) -> Response[UploadDatasetCreateResponse]:
    """Upload private dataset

     Registers a dataset in the system that you upload files into

    Args:
        project_id (str):
        body (UploadDatasetRequest):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UploadDatasetCreateResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
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
    body: UploadDatasetRequest,
) -> Optional[UploadDatasetCreateResponse]:
    """Upload private dataset

     Registers a dataset in the system that you upload files into

    Args:
        project_id (str):
        body (UploadDatasetRequest):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UploadDatasetCreateResponse
    """

    try:
        return sync_detailed(
            project_id=project_id,
            client=client,
            body=body,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    project_id: str,
    *,
    client: Client,
    body: UploadDatasetRequest,
) -> Response[UploadDatasetCreateResponse]:
    """Upload private dataset

     Registers a dataset in the system that you upload files into

    Args:
        project_id (str):
        body (UploadDatasetRequest):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UploadDatasetCreateResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: Client,
    body: UploadDatasetRequest,
) -> Optional[UploadDatasetCreateResponse]:
    """Upload private dataset

     Registers a dataset in the system that you upload files into

    Args:
        project_id (str):
        body (UploadDatasetRequest):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UploadDatasetCreateResponse
    """

    try:
        return (
            await asyncio_detailed(
                project_id=project_id,
                client=client,
                body=body,
            )
        ).parsed
    except errors.NotFoundException:
        return None
