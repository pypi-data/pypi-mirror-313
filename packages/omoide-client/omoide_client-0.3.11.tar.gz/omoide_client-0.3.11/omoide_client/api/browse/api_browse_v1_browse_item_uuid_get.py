from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_browse_v1_browse_item_uuid_get_order import ApiBrowseV1BrowseItemUuidGetOrder
from ...models.http_validation_error import HTTPValidationError
from ...models.many_items_output import ManyItemsOutput
from ...types import UNSET, Response, Unset


def _get_kwargs(
    item_uuid: UUID,
    *,
    direct: Union[Unset, bool] = False,
    order: Union[Unset, ApiBrowseV1BrowseItemUuidGetOrder] = ApiBrowseV1BrowseItemUuidGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["direct"] = direct

    json_order: Union[Unset, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["collections"] = collections

    json_last_seen: Union[None, Unset, int]
    if isinstance(last_seen, Unset):
        json_last_seen = UNSET
    else:
        json_last_seen = last_seen
    params["last_seen"] = json_last_seen

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/v1/browse/{item_uuid}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ManyItemsOutput]]:
    if response.status_code == 200:
        response_200 = ManyItemsOutput.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, ManyItemsOutput]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    item_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    direct: Union[Unset, bool] = False,
    order: Union[Unset, ApiBrowseV1BrowseItemUuidGetOrder] = ApiBrowseV1BrowseItemUuidGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Response[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Browse

     Perform browse request.

    Returns all descendants of a specified item.

    Args:
        item_uuid (UUID):
        direct (Union[Unset, bool]):  Default: False.
        order (Union[Unset, ApiBrowseV1BrowseItemUuidGetOrder]):  Default:
            ApiBrowseV1BrowseItemUuidGetOrder.RANDOM.
        collections (Union[Unset, bool]):  Default: False.
        last_seen (Union[None, Unset, int]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ManyItemsOutput]]
    """

    kwargs = _get_kwargs(
        item_uuid=item_uuid,
        direct=direct,
        order=order,
        collections=collections,
        last_seen=last_seen,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    item_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    direct: Union[Unset, bool] = False,
    order: Union[Unset, ApiBrowseV1BrowseItemUuidGetOrder] = ApiBrowseV1BrowseItemUuidGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Optional[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Browse

     Perform browse request.

    Returns all descendants of a specified item.

    Args:
        item_uuid (UUID):
        direct (Union[Unset, bool]):  Default: False.
        order (Union[Unset, ApiBrowseV1BrowseItemUuidGetOrder]):  Default:
            ApiBrowseV1BrowseItemUuidGetOrder.RANDOM.
        collections (Union[Unset, bool]):  Default: False.
        last_seen (Union[None, Unset, int]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ManyItemsOutput]
    """

    return sync_detailed(
        item_uuid=item_uuid,
        client=client,
        direct=direct,
        order=order,
        collections=collections,
        last_seen=last_seen,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    item_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    direct: Union[Unset, bool] = False,
    order: Union[Unset, ApiBrowseV1BrowseItemUuidGetOrder] = ApiBrowseV1BrowseItemUuidGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Response[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Browse

     Perform browse request.

    Returns all descendants of a specified item.

    Args:
        item_uuid (UUID):
        direct (Union[Unset, bool]):  Default: False.
        order (Union[Unset, ApiBrowseV1BrowseItemUuidGetOrder]):  Default:
            ApiBrowseV1BrowseItemUuidGetOrder.RANDOM.
        collections (Union[Unset, bool]):  Default: False.
        last_seen (Union[None, Unset, int]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ManyItemsOutput]]
    """

    kwargs = _get_kwargs(
        item_uuid=item_uuid,
        direct=direct,
        order=order,
        collections=collections,
        last_seen=last_seen,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    item_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    direct: Union[Unset, bool] = False,
    order: Union[Unset, ApiBrowseV1BrowseItemUuidGetOrder] = ApiBrowseV1BrowseItemUuidGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 25,
) -> Optional[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Browse

     Perform browse request.

    Returns all descendants of a specified item.

    Args:
        item_uuid (UUID):
        direct (Union[Unset, bool]):  Default: False.
        order (Union[Unset, ApiBrowseV1BrowseItemUuidGetOrder]):  Default:
            ApiBrowseV1BrowseItemUuidGetOrder.RANDOM.
        collections (Union[Unset, bool]):  Default: False.
        last_seen (Union[None, Unset, int]):
        limit (Union[Unset, int]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ManyItemsOutput]
    """

    return (
        await asyncio_detailed(
            item_uuid=item_uuid,
            client=client,
            direct=direct,
            order=order,
            collections=collections,
            last_seen=last_seen,
            limit=limit,
        )
    ).parsed
