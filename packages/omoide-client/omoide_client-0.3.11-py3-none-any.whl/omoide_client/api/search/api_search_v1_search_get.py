from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_search_v1_search_get_order import ApiSearchV1SearchGetOrder
from ...models.http_validation_error import HTTPValidationError
from ...models.many_items_output import ManyItemsOutput
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: Union[Unset, str] = "",
    order: Union[Unset, ApiSearchV1SearchGetOrder] = ApiSearchV1SearchGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["q"] = q

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
        "url": "/v1/search",
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
    q: Union[Unset, str] = "",
    order: Union[Unset, ApiSearchV1SearchGetOrder] = ApiSearchV1SearchGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Response[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Search

     Perform search request.

    Given input will be split into tags.
    For example 'cats + dogs - frogs' will be treated as
    [must include 'cats', must include 'dogs', must not include 'frogs'].

    Args:
        q (Union[Unset, str]):  Default: ''.
        order (Union[Unset, ApiSearchV1SearchGetOrder]):  Default:
            ApiSearchV1SearchGetOrder.RANDOM.
        collections (Union[Unset, bool]):  Default: False.
        last_seen (Union[None, Unset, int]):
        limit (Union[Unset, int]):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ManyItemsOutput]]
    """

    kwargs = _get_kwargs(
        q=q,
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
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, str] = "",
    order: Union[Unset, ApiSearchV1SearchGetOrder] = ApiSearchV1SearchGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Optional[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Search

     Perform search request.

    Given input will be split into tags.
    For example 'cats + dogs - frogs' will be treated as
    [must include 'cats', must include 'dogs', must not include 'frogs'].

    Args:
        q (Union[Unset, str]):  Default: ''.
        order (Union[Unset, ApiSearchV1SearchGetOrder]):  Default:
            ApiSearchV1SearchGetOrder.RANDOM.
        collections (Union[Unset, bool]):  Default: False.
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
        q=q,
        order=order,
        collections=collections,
        last_seen=last_seen,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, str] = "",
    order: Union[Unset, ApiSearchV1SearchGetOrder] = ApiSearchV1SearchGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Response[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Search

     Perform search request.

    Given input will be split into tags.
    For example 'cats + dogs - frogs' will be treated as
    [must include 'cats', must include 'dogs', must not include 'frogs'].

    Args:
        q (Union[Unset, str]):  Default: ''.
        order (Union[Unset, ApiSearchV1SearchGetOrder]):  Default:
            ApiSearchV1SearchGetOrder.RANDOM.
        collections (Union[Unset, bool]):  Default: False.
        last_seen (Union[None, Unset, int]):
        limit (Union[Unset, int]):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ManyItemsOutput]]
    """

    kwargs = _get_kwargs(
        q=q,
        order=order,
        collections=collections,
        last_seen=last_seen,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, str] = "",
    order: Union[Unset, ApiSearchV1SearchGetOrder] = ApiSearchV1SearchGetOrder.RANDOM,
    collections: Union[Unset, bool] = False,
    last_seen: Union[None, Unset, int] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Optional[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Search

     Perform search request.

    Given input will be split into tags.
    For example 'cats + dogs - frogs' will be treated as
    [must include 'cats', must include 'dogs', must not include 'frogs'].

    Args:
        q (Union[Unset, str]):  Default: ''.
        order (Union[Unset, ApiSearchV1SearchGetOrder]):  Default:
            ApiSearchV1SearchGetOrder.RANDOM.
        collections (Union[Unset, bool]):  Default: False.
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
            q=q,
            order=order,
            collections=collections,
            last_seen=last_seen,
            limit=limit,
        )
    ).parsed
