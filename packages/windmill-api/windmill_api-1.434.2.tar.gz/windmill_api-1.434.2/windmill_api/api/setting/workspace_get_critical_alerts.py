from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.workspace_get_critical_alerts_response_200_item import WorkspaceGetCriticalAlertsResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 10,
    acknowledged: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["page"] = page

    params["page_size"] = page_size

    params["acknowledged"] = acknowledged

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/critical_alerts".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["WorkspaceGetCriticalAlertsResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = WorkspaceGetCriticalAlertsResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["WorkspaceGetCriticalAlertsResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 10,
    acknowledged: Union[Unset, None, bool] = UNSET,
) -> Response[List["WorkspaceGetCriticalAlertsResponse200Item"]]:
    """Get all critical alerts for this workspace

    Args:
        workspace (str):
        page (Union[Unset, None, int]): The page number to retrieve (minimum value is 1) Default:
            1.
        page_size (Union[Unset, None, int]): Number of alerts per page (maximum is 100) Default:
            10.
        acknowledged (Union[Unset, None, bool]): Filter by acknowledgment status; true for
            acknowledged, false for unacknowledged, and omit for all alerts

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['WorkspaceGetCriticalAlertsResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        page=page,
        page_size=page_size,
        acknowledged=acknowledged,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 10,
    acknowledged: Union[Unset, None, bool] = UNSET,
) -> Optional[List["WorkspaceGetCriticalAlertsResponse200Item"]]:
    """Get all critical alerts for this workspace

    Args:
        workspace (str):
        page (Union[Unset, None, int]): The page number to retrieve (minimum value is 1) Default:
            1.
        page_size (Union[Unset, None, int]): Number of alerts per page (maximum is 100) Default:
            10.
        acknowledged (Union[Unset, None, bool]): Filter by acknowledgment status; true for
            acknowledged, false for unacknowledged, and omit for all alerts

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['WorkspaceGetCriticalAlertsResponse200Item']
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        page=page,
        page_size=page_size,
        acknowledged=acknowledged,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 10,
    acknowledged: Union[Unset, None, bool] = UNSET,
) -> Response[List["WorkspaceGetCriticalAlertsResponse200Item"]]:
    """Get all critical alerts for this workspace

    Args:
        workspace (str):
        page (Union[Unset, None, int]): The page number to retrieve (minimum value is 1) Default:
            1.
        page_size (Union[Unset, None, int]): Number of alerts per page (maximum is 100) Default:
            10.
        acknowledged (Union[Unset, None, bool]): Filter by acknowledgment status; true for
            acknowledged, false for unacknowledged, and omit for all alerts

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['WorkspaceGetCriticalAlertsResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        page=page,
        page_size=page_size,
        acknowledged=acknowledged,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = 1,
    page_size: Union[Unset, None, int] = 10,
    acknowledged: Union[Unset, None, bool] = UNSET,
) -> Optional[List["WorkspaceGetCriticalAlertsResponse200Item"]]:
    """Get all critical alerts for this workspace

    Args:
        workspace (str):
        page (Union[Unset, None, int]): The page number to retrieve (minimum value is 1) Default:
            1.
        page_size (Union[Unset, None, int]): Number of alerts per page (maximum is 100) Default:
            10.
        acknowledged (Union[Unset, None, bool]): Filter by acknowledgment status; true for
            acknowledged, false for unacknowledged, and omit for all alerts

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['WorkspaceGetCriticalAlertsResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            page=page,
            page_size=page_size,
            acknowledged=acknowledged,
        )
    ).parsed
