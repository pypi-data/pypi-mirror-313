from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.search_total_output import SearchTotalOutput
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: Union[Unset, str] = "",
    collections: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["q"] = q

    params["collections"] = collections

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/search/total",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, SearchTotalOutput]]:
    if response.status_code == 200:
        response_200 = SearchTotalOutput.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, SearchTotalOutput]]:
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
    collections: Union[Unset, bool] = False,
) -> Response[Union[HTTPValidationError, SearchTotalOutput]]:
    """Api Search Total

     Return total amount of items that correspond to search query.

    Args:
        q (Union[Unset, str]):  Default: ''.
        collections (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SearchTotalOutput]]
    """

    kwargs = _get_kwargs(
        q=q,
        collections=collections,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, str] = "",
    collections: Union[Unset, bool] = False,
) -> Optional[Union[HTTPValidationError, SearchTotalOutput]]:
    """Api Search Total

     Return total amount of items that correspond to search query.

    Args:
        q (Union[Unset, str]):  Default: ''.
        collections (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SearchTotalOutput]
    """

    return sync_detailed(
        client=client,
        q=q,
        collections=collections,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, str] = "",
    collections: Union[Unset, bool] = False,
) -> Response[Union[HTTPValidationError, SearchTotalOutput]]:
    """Api Search Total

     Return total amount of items that correspond to search query.

    Args:
        q (Union[Unset, str]):  Default: ''.
        collections (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SearchTotalOutput]]
    """

    kwargs = _get_kwargs(
        q=q,
        collections=collections,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, str] = "",
    collections: Union[Unset, bool] = False,
) -> Optional[Union[HTTPValidationError, SearchTotalOutput]]:
    """Api Search Total

     Return total amount of items that correspond to search query.

    Args:
        q (Union[Unset, str]):  Default: ''.
        collections (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SearchTotalOutput]
    """

    return (
        await asyncio_detailed(
            client=client,
            q=q,
            collections=collections,
        )
    ).parsed
