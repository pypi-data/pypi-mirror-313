from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.governance_classification import GovernanceClassification
from ...types import Response


def _get_kwargs(
    classification_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/governance/classifications/{classification_id}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[GovernanceClassification]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GovernanceClassification.from_dict(response.json())

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[GovernanceClassification]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    classification_id: str,
    *,
    client: Client,
) -> Response[GovernanceClassification]:
    """Get a classification

     Retrieve a data classification

    Args:
        classification_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GovernanceClassification]
    """

    kwargs = _get_kwargs(
        classification_id=classification_id,
    )

    response = client.get_httpx_client().request(
        auth=client.get_auth(),
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    classification_id: str,
    *,
    client: Client,
) -> Optional[GovernanceClassification]:
    """Get a classification

     Retrieve a data classification

    Args:
        classification_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GovernanceClassification
    """

    try:
        return sync_detailed(
            classification_id=classification_id,
            client=client,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    classification_id: str,
    *,
    client: Client,
) -> Response[GovernanceClassification]:
    """Get a classification

     Retrieve a data classification

    Args:
        classification_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GovernanceClassification]
    """

    kwargs = _get_kwargs(
        classification_id=classification_id,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    classification_id: str,
    *,
    client: Client,
) -> Optional[GovernanceClassification]:
    """Get a classification

     Retrieve a data classification

    Args:
        classification_id (str):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GovernanceClassification
    """

    try:
        return (
            await asyncio_detailed(
                classification_id=classification_id,
                client=client,
            )
        ).parsed
    except errors.NotFoundException:
        return None
