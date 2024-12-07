from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.classification_input import ClassificationInput
from ...models.governance_classification import GovernanceClassification
from ...types import Response


def _get_kwargs(
    *,
    body: ClassificationInput,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": "/governance/classifications",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[GovernanceClassification]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = GovernanceClassification.from_dict(response.json())

        return response_201

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[GovernanceClassification]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    body: ClassificationInput,
) -> Response[GovernanceClassification]:
    """Create classification

     Creates a classification

    Args:
        body (ClassificationInput):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GovernanceClassification]
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
    body: ClassificationInput,
) -> Optional[GovernanceClassification]:
    """Create classification

     Creates a classification

    Args:
        body (ClassificationInput):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GovernanceClassification
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
    body: ClassificationInput,
) -> Response[GovernanceClassification]:
    """Create classification

     Creates a classification

    Args:
        body (ClassificationInput):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GovernanceClassification]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: ClassificationInput,
) -> Optional[GovernanceClassification]:
    """Create classification

     Creates a classification

    Args:
        body (ClassificationInput):
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
                client=client,
                body=body,
            )
        ).parsed
    except errors.NotFoundException:
        return None
