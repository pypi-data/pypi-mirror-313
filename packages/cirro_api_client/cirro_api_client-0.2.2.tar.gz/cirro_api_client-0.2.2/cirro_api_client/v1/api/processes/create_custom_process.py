from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.create_response import CreateResponse
from ...models.error_message import ErrorMessage
from ...models.portal_error_response import PortalErrorResponse
from ...models.process_detail import ProcessDetail
from ...types import Response


def _get_kwargs(
    *,
    body: ProcessDetail,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/processes",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[CreateResponse, ErrorMessage, PortalErrorResponse]]:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = PortalErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ErrorMessage.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.CREATED:
        response_201 = CreateResponse.from_dict(response.json())

        return response_201

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[CreateResponse, ErrorMessage, PortalErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    body: ProcessDetail,
) -> Response[Union[CreateResponse, ErrorMessage, PortalErrorResponse]]:
    """Create custom process

     Creates a custom data type or pipeline which you can use in the listed projects.

    Args:
        body (ProcessDetail):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateResponse, ErrorMessage, PortalErrorResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        auth=client.get_auth(),
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    body: ProcessDetail,
) -> Optional[Union[CreateResponse, ErrorMessage, PortalErrorResponse]]:
    """Create custom process

     Creates a custom data type or pipeline which you can use in the listed projects.

    Args:
        body (ProcessDetail):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateResponse, ErrorMessage, PortalErrorResponse]
    """

    try:
        return sync_detailed(
            client=client,
            body=body,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    *,
    client: Client,
    body: ProcessDetail,
) -> Response[Union[CreateResponse, ErrorMessage, PortalErrorResponse]]:
    """Create custom process

     Creates a custom data type or pipeline which you can use in the listed projects.

    Args:
        body (ProcessDetail):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateResponse, ErrorMessage, PortalErrorResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: ProcessDetail,
) -> Optional[Union[CreateResponse, ErrorMessage, PortalErrorResponse]]:
    """Create custom process

     Creates a custom data type or pipeline which you can use in the listed projects.

    Args:
        body (ProcessDetail):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateResponse, ErrorMessage, PortalErrorResponse]
    """

    try:
        return (
            await asyncio_detailed(
                client=client,
                body=body,
            )
        ).parsed
    except errors.NotFoundException:
        return None
