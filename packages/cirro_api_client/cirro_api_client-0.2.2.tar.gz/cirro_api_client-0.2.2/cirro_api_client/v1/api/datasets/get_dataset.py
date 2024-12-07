from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.dataset_detail import DatasetDetail
from ...types import Response


def _get_kwargs(
    project_id: str,
    dataset_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/datasets/{dataset_id}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[DatasetDetail]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DatasetDetail.from_dict(response.json())

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[DatasetDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    dataset_id: str,
    *,
    client: Client,
) -> Response[DatasetDetail]:
    """Get dataset

     Gets detailed information about a dataset

    Args:
        project_id (str):
        dataset_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetDetail]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        dataset_id=dataset_id,
    )

    response = client.get_httpx_client().request(
        auth=client.get_auth(),
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    dataset_id: str,
    *,
    client: Client,
) -> Optional[DatasetDetail]:
    """Get dataset

     Gets detailed information about a dataset

    Args:
        project_id (str):
        dataset_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetDetail
    """

    try:
        return sync_detailed(
            project_id=project_id,
            dataset_id=dataset_id,
            client=client,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    project_id: str,
    dataset_id: str,
    *,
    client: Client,
) -> Response[DatasetDetail]:
    """Get dataset

     Gets detailed information about a dataset

    Args:
        project_id (str):
        dataset_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetDetail]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        dataset_id=dataset_id,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    dataset_id: str,
    *,
    client: Client,
) -> Optional[DatasetDetail]:
    """Get dataset

     Gets detailed information about a dataset

    Args:
        project_id (str):
        dataset_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetDetail
    """

    try:
        return (
            await asyncio_detailed(
                project_id=project_id,
                dataset_id=dataset_id,
                client=client,
            )
        ).parsed
    except errors.NotFoundException:
        return None
