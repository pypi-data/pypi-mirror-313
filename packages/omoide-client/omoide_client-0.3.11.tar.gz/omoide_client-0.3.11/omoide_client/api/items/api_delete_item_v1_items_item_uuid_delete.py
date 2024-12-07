from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_delete_item_v1_items_item_uuid_delete_desired_switch import (
    ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.item_delete_output import ItemDeleteOutput
from ...types import UNSET, Response, Unset


def _get_kwargs(
    item_uuid: UUID,
    *,
    desired_switch: Union[
        Unset, ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch
    ] = ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch.SIBLING,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_desired_switch: Union[Unset, str] = UNSET
    if not isinstance(desired_switch, Unset):
        json_desired_switch = desired_switch.value

    params["desired_switch"] = json_desired_switch

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/v1/items/{item_uuid}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ItemDeleteOutput]]:
    if response.status_code == 202:
        response_202 = ItemDeleteOutput.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ItemDeleteOutput]]:
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
    desired_switch: Union[
        Unset, ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch
    ] = ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch.SIBLING,
) -> Response[Union[HTTPValidationError, ItemDeleteOutput]]:
    """Api Delete Item

     Delete exising item.

    Args:
        item_uuid (UUID):
        desired_switch (Union[Unset, ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch]):  Default:
            ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch.SIBLING.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ItemDeleteOutput]]
    """

    kwargs = _get_kwargs(
        item_uuid=item_uuid,
        desired_switch=desired_switch,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    item_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    desired_switch: Union[
        Unset, ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch
    ] = ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch.SIBLING,
) -> Optional[Union[HTTPValidationError, ItemDeleteOutput]]:
    """Api Delete Item

     Delete exising item.

    Args:
        item_uuid (UUID):
        desired_switch (Union[Unset, ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch]):  Default:
            ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch.SIBLING.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ItemDeleteOutput]
    """

    return sync_detailed(
        item_uuid=item_uuid,
        client=client,
        desired_switch=desired_switch,
    ).parsed


async def asyncio_detailed(
    item_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    desired_switch: Union[
        Unset, ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch
    ] = ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch.SIBLING,
) -> Response[Union[HTTPValidationError, ItemDeleteOutput]]:
    """Api Delete Item

     Delete exising item.

    Args:
        item_uuid (UUID):
        desired_switch (Union[Unset, ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch]):  Default:
            ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch.SIBLING.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ItemDeleteOutput]]
    """

    kwargs = _get_kwargs(
        item_uuid=item_uuid,
        desired_switch=desired_switch,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    item_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    desired_switch: Union[
        Unset, ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch
    ] = ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch.SIBLING,
) -> Optional[Union[HTTPValidationError, ItemDeleteOutput]]:
    """Api Delete Item

     Delete exising item.

    Args:
        item_uuid (UUID):
        desired_switch (Union[Unset, ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch]):  Default:
            ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch.SIBLING.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ItemDeleteOutput]
    """

    return (
        await asyncio_detailed(
            item_uuid=item_uuid,
            client=client,
            desired_switch=desired_switch,
        )
    ).parsed
