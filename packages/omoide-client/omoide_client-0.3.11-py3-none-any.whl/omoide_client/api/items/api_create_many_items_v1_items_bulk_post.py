from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.item_input import ItemInput
from ...models.many_items_output import ManyItemsOutput
from ...types import Response


def _get_kwargs(
    *,
    body: List["ItemInput"],
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/v1/items/bulk",
    }

    _body = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _body.append(body_item)

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ManyItemsOutput]]:
    if response.status_code == 201:
        response_201 = ManyItemsOutput.from_dict(response.json())

        return response_201
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
    body: List["ItemInput"],
) -> Response[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Create Many Items

     Create many items in one request.

    Args:
        body (List['ItemInput']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ManyItemsOutput]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: List["ItemInput"],
) -> Optional[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Create Many Items

     Create many items in one request.

    Args:
        body (List['ItemInput']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ManyItemsOutput]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: List["ItemInput"],
) -> Response[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Create Many Items

     Create many items in one request.

    Args:
        body (List['ItemInput']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ManyItemsOutput]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: List["ItemInput"],
) -> Optional[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Create Many Items

     Create many items in one request.

    Args:
        body (List['ItemInput']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ManyItemsOutput]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
