from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.process_detail import ProcessDetail
from ...types import Response


def _get_kwargs(
    process_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/processes/{process_id}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[ProcessDetail]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ProcessDetail.from_dict(response.json())

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[ProcessDetail]:
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
) -> Response[ProcessDetail]:
    """Get process

     Retrieves detailed information on a process

    Args:
        process_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProcessDetail]
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
) -> Optional[ProcessDetail]:
    """Get process

     Retrieves detailed information on a process

    Args:
        process_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProcessDetail
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
) -> Response[ProcessDetail]:
    """Get process

     Retrieves detailed information on a process

    Args:
        process_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProcessDetail]
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
) -> Optional[ProcessDetail]:
    """Get process

     Retrieves detailed information on a process

    Args:
        process_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProcessDetail
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
