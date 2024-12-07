from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_delete_exif_v1_exif_item_uuid_delete_response_api_delete_exif_v1_exif_item_uuid_delete import (
    ApiDeleteExifV1ExifItemUuidDeleteResponseApiDeleteExifV1ExifItemUuidDelete,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    item_uuid: UUID,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/v1/exif/{item_uuid}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ApiDeleteExifV1ExifItemUuidDeleteResponseApiDeleteExifV1ExifItemUuidDelete, HTTPValidationError]]:
    if response.status_code == 202:
        response_202 = ApiDeleteExifV1ExifItemUuidDeleteResponseApiDeleteExifV1ExifItemUuidDelete.from_dict(
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
) -> Response[Union[ApiDeleteExifV1ExifItemUuidDeleteResponseApiDeleteExifV1ExifItemUuidDelete, HTTPValidationError]]:
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
) -> Response[Union[ApiDeleteExifV1ExifItemUuidDeleteResponseApiDeleteExifV1ExifItemUuidDelete, HTTPValidationError]]:
    """Api Delete Exif

     Delete EXIF data from exising item.

    Args:
        item_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiDeleteExifV1ExifItemUuidDeleteResponseApiDeleteExifV1ExifItemUuidDelete, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        item_uuid=item_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    item_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[ApiDeleteExifV1ExifItemUuidDeleteResponseApiDeleteExifV1ExifItemUuidDelete, HTTPValidationError]]:
    """Api Delete Exif

     Delete EXIF data from exising item.

    Args:
        item_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiDeleteExifV1ExifItemUuidDeleteResponseApiDeleteExifV1ExifItemUuidDelete, HTTPValidationError]
    """

    return sync_detailed(
        item_uuid=item_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    item_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[ApiDeleteExifV1ExifItemUuidDeleteResponseApiDeleteExifV1ExifItemUuidDelete, HTTPValidationError]]:
    """Api Delete Exif

     Delete EXIF data from exising item.

    Args:
        item_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiDeleteExifV1ExifItemUuidDeleteResponseApiDeleteExifV1ExifItemUuidDelete, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        item_uuid=item_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    item_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[ApiDeleteExifV1ExifItemUuidDeleteResponseApiDeleteExifV1ExifItemUuidDelete, HTTPValidationError]]:
    """Api Delete Exif

     Delete EXIF data from exising item.

    Args:
        item_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiDeleteExifV1ExifItemUuidDeleteResponseApiDeleteExifV1ExifItemUuidDelete, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            item_uuid=item_uuid,
            client=client,
        )
    ).parsed
