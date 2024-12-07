from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.billing_account import BillingAccount
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    include_archived: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["includeArchived"] = include_archived

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/billing",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[List["BillingAccount"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = BillingAccount.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[List["BillingAccount"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    include_archived: Union[Unset, bool] = False,
) -> Response[List["BillingAccount"]]:
    """List billing accounts

     Gets a list of billing accounts the current user has access to

    Args:
        include_archived (Union[Unset, bool]):  Default: False.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['BillingAccount']]
    """

    kwargs = _get_kwargs(
        include_archived=include_archived,
    )

    response = client.get_httpx_client().request(
        auth=client.get_auth(),
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    include_archived: Union[Unset, bool] = False,
) -> Optional[List["BillingAccount"]]:
    """List billing accounts

     Gets a list of billing accounts the current user has access to

    Args:
        include_archived (Union[Unset, bool]):  Default: False.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['BillingAccount']
    """

    try:
        return sync_detailed(
            client=client,
            include_archived=include_archived,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    *,
    client: Client,
    include_archived: Union[Unset, bool] = False,
) -> Response[List["BillingAccount"]]:
    """List billing accounts

     Gets a list of billing accounts the current user has access to

    Args:
        include_archived (Union[Unset, bool]):  Default: False.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['BillingAccount']]
    """

    kwargs = _get_kwargs(
        include_archived=include_archived,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    include_archived: Union[Unset, bool] = False,
) -> Optional[List["BillingAccount"]]:
    """List billing accounts

     Gets a list of billing accounts the current user has access to

    Args:
        include_archived (Union[Unset, bool]):  Default: False.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['BillingAccount']
    """

    try:
        return (
            await asyncio_detailed(
                client=client,
                include_archived=include_archived,
            )
        ).parsed
    except errors.NotFoundException:
        return None
