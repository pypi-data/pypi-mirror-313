from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_create_exif_v1_exif_item_uuid_post_response_api_create_exif_v1_exif_item_uuid_post import (
    ApiCreateExifV1ExifItemUuidPostResponseApiCreateExifV1ExifItemUuidPost,
)
from ...models.exif_model import EXIFModel
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    item_uuid: UUID,
    *,
    body: EXIFModel,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/v1/exif/{item_uuid}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ApiCreateExifV1ExifItemUuidPostResponseApiCreateExifV1ExifItemUuidPost, HTTPValidationError]]:
    if response.status_code == 201:
        response_201 = ApiCreateExifV1ExifItemUuidPostResponseApiCreateExifV1ExifItemUuidPost.from_dict(response.json())

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
) -> Response[Union[ApiCreateExifV1ExifItemUuidPostResponseApiCreateExifV1ExifItemUuidPost, HTTPValidationError]]:
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
    body: EXIFModel,
) -> Response[Union[ApiCreateExifV1ExifItemUuidPostResponseApiCreateExifV1ExifItemUuidPost, HTTPValidationError]]:
    """Api Create Exif

     Add EXIF data to existing item.

    Args:
        item_uuid (UUID):
        body (EXIFModel): Input info for EXIF creation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiCreateExifV1ExifItemUuidPostResponseApiCreateExifV1ExifItemUuidPost, HTTPValidationError]]
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
    body: EXIFModel,
) -> Optional[Union[ApiCreateExifV1ExifItemUuidPostResponseApiCreateExifV1ExifItemUuidPost, HTTPValidationError]]:
    """Api Create Exif

     Add EXIF data to existing item.

    Args:
        item_uuid (UUID):
        body (EXIFModel): Input info for EXIF creation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiCreateExifV1ExifItemUuidPostResponseApiCreateExifV1ExifItemUuidPost, HTTPValidationError]
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
    body: EXIFModel,
) -> Response[Union[ApiCreateExifV1ExifItemUuidPostResponseApiCreateExifV1ExifItemUuidPost, HTTPValidationError]]:
    """Api Create Exif

     Add EXIF data to existing item.

    Args:
        item_uuid (UUID):
        body (EXIFModel): Input info for EXIF creation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiCreateExifV1ExifItemUuidPostResponseApiCreateExifV1ExifItemUuidPost, HTTPValidationError]]
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
    body: EXIFModel,
) -> Optional[Union[ApiCreateExifV1ExifItemUuidPostResponseApiCreateExifV1ExifItemUuidPost, HTTPValidationError]]:
    """Api Create Exif

     Add EXIF data to existing item.

    Args:
        item_uuid (UUID):
        body (EXIFModel): Input info for EXIF creation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiCreateExifV1ExifItemUuidPostResponseApiCreateExifV1ExifItemUuidPost, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            item_uuid=item_uuid,
            client=client,
            body=body,
        )
    ).parsed
