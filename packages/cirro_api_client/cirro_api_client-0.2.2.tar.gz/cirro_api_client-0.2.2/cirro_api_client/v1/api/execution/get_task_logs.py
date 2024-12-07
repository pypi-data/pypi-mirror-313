from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.get_execution_logs_response import GetExecutionLogsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    dataset_id: str,
    task_id: str,
    *,
    force_live: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["forceLive"] = force_live

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/execution/{dataset_id}/tasks/{task_id}/logs",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[GetExecutionLogsResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetExecutionLogsResponse.from_dict(response.json())

        return response_200

    errors.handle_error_response(response, client.raise_on_unexpected_status)


def _build_response(*, client: Client, response: httpx.Response) -> Response[GetExecutionLogsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    dataset_id: str,
    task_id: str,
    *,
    client: Client,
    force_live: Union[Unset, bool] = False,
) -> Response[GetExecutionLogsResponse]:
    """Get task logs

     Gets the log output from an individual task

    Args:
        project_id (str):
        dataset_id (str):
        task_id (str):
        force_live (Union[Unset, bool]):  Default: False.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetExecutionLogsResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        dataset_id=dataset_id,
        task_id=task_id,
        force_live=force_live,
    )

    response = client.get_httpx_client().request(
        auth=client.get_auth(),
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    dataset_id: str,
    task_id: str,
    *,
    client: Client,
    force_live: Union[Unset, bool] = False,
) -> Optional[GetExecutionLogsResponse]:
    """Get task logs

     Gets the log output from an individual task

    Args:
        project_id (str):
        dataset_id (str):
        task_id (str):
        force_live (Union[Unset, bool]):  Default: False.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetExecutionLogsResponse
    """

    try:
        return sync_detailed(
            project_id=project_id,
            dataset_id=dataset_id,
            task_id=task_id,
            client=client,
            force_live=force_live,
        ).parsed
    except errors.NotFoundException:
        return None


async def asyncio_detailed(
    project_id: str,
    dataset_id: str,
    task_id: str,
    *,
    client: Client,
    force_live: Union[Unset, bool] = False,
) -> Response[GetExecutionLogsResponse]:
    """Get task logs

     Gets the log output from an individual task

    Args:
        project_id (str):
        dataset_id (str):
        task_id (str):
        force_live (Union[Unset, bool]):  Default: False.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetExecutionLogsResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        dataset_id=dataset_id,
        task_id=task_id,
        force_live=force_live,
    )

    response = await client.get_async_httpx_client().request(auth=client.get_auth(), **kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    dataset_id: str,
    task_id: str,
    *,
    client: Client,
    force_live: Union[Unset, bool] = False,
) -> Optional[GetExecutionLogsResponse]:
    """Get task logs

     Gets the log output from an individual task

    Args:
        project_id (str):
        dataset_id (str):
        task_id (str):
        force_live (Union[Unset, bool]):  Default: False.
        client (Client): instance of the API client

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetExecutionLogsResponse
    """

    try:
        return (
            await asyncio_detailed(
                project_id=project_id,
                dataset_id=dataset_id,
                task_id=task_id,
                client=client,
                force_live=force_live,
            )
        ).parsed
    except errors.NotFoundException:
        return None
