from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_rename_item_v1_items_item_uuid_name_put_response_api_rename_item_v1_items_item_uuid_name_put import (
    ApiRenameItemV1ItemsItemUuidNamePutResponseApiRenameItemV1ItemsItemUuidNamePut,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.item_rename_input import ItemRenameInput
from ...types import Response


def _get_kwargs(
    item_uuid: UUID,
    *,
    body: ItemRenameInput,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/v1/items/{item_uuid}/name",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[ApiRenameItemV1ItemsItemUuidNamePutResponseApiRenameItemV1ItemsItemUuidNamePut, HTTPValidationError]
]:
    if response.status_code == 202:
        response_202 = ApiRenameItemV1ItemsItemUuidNamePutResponseApiRenameItemV1ItemsItemUuidNamePut.from_dict(
            response.json()
        )

        return response_202
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[ApiRenameItemV1ItemsItemUuidNamePutResponseApiRenameItemV1ItemsItemUuidNamePut, HTTPValidationError]
]:
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
    body: ItemRenameInput,
) -> Response[
    Union[ApiRenameItemV1ItemsItemUuidNamePutResponseApiRenameItemV1ItemsItemUuidNamePut, HTTPValidationError]
]:
    """Api Rename Item

     Rename exising item.

    Args:
        item_uuid (UUID):
        body (ItemRenameInput): Input info for item rename.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiRenameItemV1ItemsItemUuidNamePutResponseApiRenameItemV1ItemsItemUuidNamePut, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        item_uuid=item_uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    item_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ItemRenameInput,
) -> Optional[
    Union[ApiRenameItemV1ItemsItemUuidNamePutResponseApiRenameItemV1ItemsItemUuidNamePut, HTTPValidationError]
]:
    """Api Rename Item

     Rename exising item.

    Args:
        item_uuid (UUID):
        body (ItemRenameInput): Input info for item rename.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiRenameItemV1ItemsItemUuidNamePutResponseApiRenameItemV1ItemsItemUuidNamePut, HTTPValidationError]
    """

    return sync_detailed(
        item_uuid=item_uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    item_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ItemRenameInput,
) -> Response[
    Union[ApiRenameItemV1ItemsItemUuidNamePutResponseApiRenameItemV1ItemsItemUuidNamePut, HTTPValidationError]
]:
    """Api Rename Item

     Rename exising item.

    Args:
        item_uuid (UUID):
        body (ItemRenameInput): Input info for item rename.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiRenameItemV1ItemsItemUuidNamePutResponseApiRenameItemV1ItemsItemUuidNamePut, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        item_uuid=item_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    item_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ItemRenameInput,
) -> Optional[
    Union[ApiRenameItemV1ItemsItemUuidNamePutResponseApiRenameItemV1ItemsItemUuidNamePut, HTTPValidationError]
]:
    """Api Rename Item

     Rename exising item.

    Args:
        item_uuid (UUID):
        body (ItemRenameInput): Input info for item rename.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiRenameItemV1ItemsItemUuidNamePutResponseApiRenameItemV1ItemsItemUuidNamePut, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            item_uuid=item_uuid,
            client=client,
            body=body,
        )
    ).parsed
