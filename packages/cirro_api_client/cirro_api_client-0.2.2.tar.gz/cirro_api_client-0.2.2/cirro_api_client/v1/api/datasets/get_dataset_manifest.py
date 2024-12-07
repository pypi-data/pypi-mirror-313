from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.dataset_assets_manifest import DatasetAssetsManifest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    dataset_id: str,
    *,
    file_offset: Union[Unset, int] = 0,
    file_limit: Union[Unset, int] = 20000,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["fileOffset"] = file_offset

    params["fileLimit"] = file_limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/datasets/{dataset_id}/files",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[DatasetAssetsManifest]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DatasetAssetsManifest.from_dict(response.json())

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[DatasetAssetsManifest]:
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
    file_offset: Union[Unset, int] = 0,
    file_limit: Union[Unset, int] = 20000,
) -> Response[DatasetAssetsManifest]:
    """Get dataset manifest

     Gets a listing of files, charts, and other assets available for the dataset

    Args:
        project_id (str):
        dataset_id (str):
        file_offset (Union[Unset, int]):  Default: 0.
        file_limit (Union[Unset, int]):  Default: 20000.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetAssetsManifest]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        dataset_id=dataset_id,
        file_offset=file_offset,
        file_limit=file_limit,
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
    file_offset: Union[Unset, int] = 0,
    file_limit: Union[Unset, int] = 20000,
) -> Optional[DatasetAssetsManifest]:
    """Get dataset manifest

     Gets a listing of files, charts, and other assets available for the dataset

    Args:
        project_id (str):
        dataset_id (str):
        file_offset (Union[Unset, int]):  Default: 0.
        file_limit (Union[Unset, int]):  Default: 20000.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetAssetsManifest
    """

    try:
        return sync_detailed(
            project_id=project_id,
            dataset_id=dataset_id,
            client=client,
            file_offset=file_offset,
            file_limit=file_limit,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    project_id: str,
    dataset_id: str,
    *,
    client: Client,
    file_offset: Union[Unset, int] = 0,
    file_limit: Union[Unset, int] = 20000,
) -> Response[DatasetAssetsManifest]:
    """Get dataset manifest

     Gets a listing of files, charts, and other assets available for the dataset

    Args:
        project_id (str):
        dataset_id (str):
        file_offset (Union[Unset, int]):  Default: 0.
        file_limit (Union[Unset, int]):  Default: 20000.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetAssetsManifest]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        dataset_id=dataset_id,
        file_offset=file_offset,
        file_limit=file_limit,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    dataset_id: str,
    *,
    client: Client,
    file_offset: Union[Unset, int] = 0,
    file_limit: Union[Unset, int] = 20000,
) -> Optional[DatasetAssetsManifest]:
    """Get dataset manifest

     Gets a listing of files, charts, and other assets available for the dataset

    Args:
        project_id (str):
        dataset_id (str):
        file_offset (Union[Unset, int]):  Default: 0.
        file_limit (Union[Unset, int]):  Default: 20000.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetAssetsManifest
    """

    try:
        return (
            await asyncio_detailed(
                project_id=project_id,
                dataset_id=dataset_id,
                client=client,
                file_offset=file_offset,
                file_limit=file_limit,
            )
        ).parsed
    except errors.NotFoundException:
        return None
