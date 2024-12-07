from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.many_items_output import ManyItemsOutput
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    owner_uuid: Union[None, UUID, Unset] = UNSET,
    parent_uuid: Union[None, UUID, Unset] = UNSET,
    name: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_owner_uuid: Union[None, Unset, str]
    if isinstance(owner_uuid, Unset):
        json_owner_uuid = UNSET
    elif isinstance(owner_uuid, UUID):
        json_owner_uuid = str(owner_uuid)
    else:
        json_owner_uuid = owner_uuid
    params["owner_uuid"] = json_owner_uuid

    json_parent_uuid: Union[None, Unset, str]
    if isinstance(parent_uuid, Unset):
        json_parent_uuid = UNSET
    elif isinstance(parent_uuid, UUID):
        json_parent_uuid = str(parent_uuid)
    else:
        json_parent_uuid = parent_uuid
    params["parent_uuid"] = json_parent_uuid

    json_name: Union[None, Unset, str]
    if isinstance(name, Unset):
        json_name = UNSET
    else:
        json_name = name
    params["name"] = json_name

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/items",
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
    owner_uuid: Union[None, UUID, Unset] = UNSET,
    parent_uuid: Union[None, UUID, Unset] = UNSET,
    name: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Response[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Get Many Items

     Get exising items.

    Args:
        owner_uuid (Union[None, UUID, Unset]):
        parent_uuid (Union[None, UUID, Unset]):
        name (Union[None, Unset, str]):
        limit (Union[Unset, int]):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ManyItemsOutput]]
    """

    kwargs = _get_kwargs(
        owner_uuid=owner_uuid,
        parent_uuid=parent_uuid,
        name=name,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    owner_uuid: Union[None, UUID, Unset] = UNSET,
    parent_uuid: Union[None, UUID, Unset] = UNSET,
    name: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Optional[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Get Many Items

     Get exising items.

    Args:
        owner_uuid (Union[None, UUID, Unset]):
        parent_uuid (Union[None, UUID, Unset]):
        name (Union[None, Unset, str]):
        limit (Union[Unset, int]):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ManyItemsOutput]
    """

    return sync_detailed(
        client=client,
        owner_uuid=owner_uuid,
        parent_uuid=parent_uuid,
        name=name,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    owner_uuid: Union[None, UUID, Unset] = UNSET,
    parent_uuid: Union[None, UUID, Unset] = UNSET,
    name: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Response[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Get Many Items

     Get exising items.

    Args:
        owner_uuid (Union[None, UUID, Unset]):
        parent_uuid (Union[None, UUID, Unset]):
        name (Union[None, Unset, str]):
        limit (Union[Unset, int]):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ManyItemsOutput]]
    """

    kwargs = _get_kwargs(
        owner_uuid=owner_uuid,
        parent_uuid=parent_uuid,
        name=name,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    owner_uuid: Union[None, UUID, Unset] = UNSET,
    parent_uuid: Union[None, UUID, Unset] = UNSET,
    name: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 30,
) -> Optional[Union[HTTPValidationError, ManyItemsOutput]]:
    """Api Get Many Items

     Get exising items.

    Args:
        owner_uuid (Union[None, UUID, Unset]):
        parent_uuid (Union[None, UUID, Unset]):
        name (Union[None, Unset, str]):
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
            owner_uuid=owner_uuid,
            parent_uuid=parent_uuid,
            name=name,
            limit=limit,
        )
    ).parsed
