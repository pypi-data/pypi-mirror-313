from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_home_v1_home_get_order import ApiHomeV1HomeGetOrder
from ...models.http_validation_error import HTTPValidationError
from ...models.many_items_output import ManyItemsOutput
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    order: Union[Unset, ApiHomeV1HomeGetOrder] = ApiHomeV1HomeGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    direct: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_order: Union[Unset, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["collections"] = collections

    params["direct"] = direct

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
        "url": "/v1/home",
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
    *,
    client: Union[AuthenticatedClient, Client],
    order: Union[Unset, ApiHomeV1HomeGetOrder] = ApiHomeV1HomeGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    direct: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Response[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Home

     Return items for user home page.

    Combined collections of all available users.

    Args:
        order (Union[Unset, ApiHomeV1HomeGetOrder]):  Default: ApiHomeV1HomeGetOrder.RANDOM.
        collections (Union[Unset, bool]):  Default: False.
        direct (Union[Unset, bool]):  Default: False.
        last_seen (Union[None, Unset, int]):
        limit (Union[Unset, int]):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ManyItemsOutput]]
    """

    kwargs = _get_kwargs(
        order=order,
        collections=collections,
        direct=direct,
        last_seen=last_seen,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    order: Union[Unset, ApiHomeV1HomeGetOrder] = ApiHomeV1HomeGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    direct: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Optional[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Home

     Return items for user home page.

    Combined collections of all available users.

    Args:
        order (Union[Unset, ApiHomeV1HomeGetOrder]):  Default: ApiHomeV1HomeGetOrder.RANDOM.
        collections (Union[Unset, bool]):  Default: False.
        direct (Union[Unset, bool]):  Default: False.
        last_seen (Union[None, Unset, int]):
        limit (Union[Unset, int]):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ManyItemsOutput]
    """

    return sync_detailed(
        client=client,
        order=order,
        collections=collections,
        direct=direct,
        last_seen=last_seen,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    order: Union[Unset, ApiHomeV1HomeGetOrder] = ApiHomeV1HomeGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    direct: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Response[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Home

     Return items for user home page.

    Combined collections of all available users.

    Args:
        order (Union[Unset, ApiHomeV1HomeGetOrder]):  Default: ApiHomeV1HomeGetOrder.RANDOM.
        collections (Union[Unset, bool]):  Default: False.
        direct (Union[Unset, bool]):  Default: False.
        last_seen (Union[None, Unset, int]):
        limit (Union[Unset, int]):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ManyItemsOutput]]
    """

    kwargs = _get_kwargs(
        order=order,
        collections=collections,
        direct=direct,
        last_seen=last_seen,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    order: Union[Unset, ApiHomeV1HomeGetOrder] = ApiHomeV1HomeGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    direct: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Optional[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Home

     Return items for user home page.

    Combined collections of all available users.

    Args:
        order (Union[Unset, ApiHomeV1HomeGetOrder]):  Default: ApiHomeV1HomeGetOrder.RANDOM.
        collections (Union[Unset, bool]):  Default: False.
        direct (Union[Unset, bool]):  Default: False.
        last_seen (Union[None, Unset, int]):
        limit (Union[Unset, int]):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ManyItemsOutput]
    """

    return (
        await asyncio_detailed(
            client=client,
            order=order,
            collections=collections,
            direct=direct,
            last_seen=last_seen,
            limit=limit,
        )
    ).parsed
