from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.custom_pipeline_settings import CustomPipelineSettings
from ...types import Response


def _get_kwargs(
    process_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/processes/{process_id}:sync",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[CustomPipelineSettings]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CustomPipelineSettings.from_dict(response.json())

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[CustomPipelineSettings]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    process_id: str,
    *,
    client: Client,
) -> Response[CustomPipelineSettings]:
    """Sync custom process

     Updates the process definition from the repository

    Args:
        process_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CustomPipelineSettings]
    """

    kwargs = _get_kwargs(
        process_id=process_id,
    )

    response = client.get_httpx_client().request(
        auth=client.get_auth(),
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    process_id: str,
    *,
    client: Client,
) -> Optional[CustomPipelineSettings]:
    """Sync custom process

     Updates the process definition from the repository

    Args:
        process_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CustomPipelineSettings
    """

    try:
        return sync_detailed(
            process_id=process_id,
            client=client,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    process_id: str,
    *,
    client: Client,
) -> Response[CustomPipelineSettings]:
    """Sync custom process

     Updates the process definition from the repository

    Args:
        process_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CustomPipelineSettings]
    """

    kwargs = _get_kwargs(
        process_id=process_id,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    process_id: str,
    *,
    client: Client,
) -> Optional[CustomPipelineSettings]:
    """Sync custom process

     Updates the process definition from the repository

    Args:
        process_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CustomPipelineSettings
    """

    try:
        return (
            await asyncio_detailed(
                process_id=process_id,
                client=client,
            )
        ).parsed
    except errors.NotFoundException:
        return None
