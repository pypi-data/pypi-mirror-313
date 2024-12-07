from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.audit_event import AuditEvent
from ...types import Response


def _get_kwargs(
    audit_event_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/audit-events/{audit_event_id}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[AuditEvent]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AuditEvent.from_dict(response.json())

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[AuditEvent]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    audit_event_id: str,
    *,
    client: Client,
) -> Response[AuditEvent]:
    """Get audit event

     Get audit event detailed information

    Args:
        audit_event_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuditEvent]
    """

    kwargs = _get_kwargs(
        audit_event_id=audit_event_id,
    )

    response = client.get_httpx_client().request(
        auth=client.get_auth(),
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    audit_event_id: str,
    *,
    client: Client,
) -> Optional[AuditEvent]:
    """Get audit event

     Get audit event detailed information

    Args:
        audit_event_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuditEvent
    """

    try:
        return sync_detailed(
            audit_event_id=audit_event_id,
            client=client,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    audit_event_id: str,
    *,
    client: Client,
) -> Response[AuditEvent]:
    """Get audit event

     Get audit event detailed information

    Args:
        audit_event_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuditEvent]
    """

    kwargs = _get_kwargs(
        audit_event_id=audit_event_id,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    audit_event_id: str,
    *,
    client: Client,
) -> Optional[AuditEvent]:
    """Get audit event

     Get audit event detailed information

    Args:
        audit_event_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuditEvent
    """

    try:
        return (
            await asyncio_detailed(
                audit_event_id=audit_event_id,
                client=client,
            )
        ).parsed
    except errors.NotFoundException:
        return None
