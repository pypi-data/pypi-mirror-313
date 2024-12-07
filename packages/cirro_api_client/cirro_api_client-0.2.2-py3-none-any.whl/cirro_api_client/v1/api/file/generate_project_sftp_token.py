from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.generate_sftp_credentials_request import GenerateSftpCredentialsRequest
from ...models.sftp_credentials import SftpCredentials
from ...types import Response


def _get_kwargs(
    project_id: str,
    *,
    body: GenerateSftpCredentialsRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/projects/{project_id}/sftp-token",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[SftpCredentials]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SftpCredentials.from_dict(response.json())

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[SftpCredentials]:
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
    body: GenerateSftpCredentialsRequest,
) -> Response[SftpCredentials]:
    """Create project SFTP Token

     Generates credentials used for connecting via SFTP

    Args:
        project_id (str):
        body (GenerateSftpCredentialsRequest):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SftpCredentials]
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
    body: GenerateSftpCredentialsRequest,
) -> Optional[SftpCredentials]:
    """Create project SFTP Token

     Generates credentials used for connecting via SFTP

    Args:
        project_id (str):
        body (GenerateSftpCredentialsRequest):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SftpCredentials
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
    body: GenerateSftpCredentialsRequest,
) -> Response[SftpCredentials]:
    """Create project SFTP Token

     Generates credentials used for connecting via SFTP

    Args:
        project_id (str):
        body (GenerateSftpCredentialsRequest):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SftpCredentials]
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
    body: GenerateSftpCredentialsRequest,
) -> Optional[SftpCredentials]:
    """Create project SFTP Token

     Generates credentials used for connecting via SFTP

    Args:
        project_id (str):
        body (GenerateSftpCredentialsRequest):
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SftpCredentials
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
