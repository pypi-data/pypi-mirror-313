from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_action_copy_image_v1_actions_copy_image_post_response_api_action_copy_image_v1_actions_copy_image_post import (
    ApiActionCopyImageV1ActionsCopyImagePostResponseApiActionCopyImageV1ActionsCopyImagePost,
)
from ...models.copy_image_input import CopyImageInput
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    body: CopyImageInput,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/v1/actions/copy_image",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[ApiActionCopyImageV1ActionsCopyImagePostResponseApiActionCopyImageV1ActionsCopyImagePost, HTTPValidationError]
]:
    if response.status_code == 202:
        response_202 = (
            ApiActionCopyImageV1ActionsCopyImagePostResponseApiActionCopyImageV1ActionsCopyImagePost.from_dict(
                response.json()
            )
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
    Union[ApiActionCopyImageV1ActionsCopyImagePostResponseApiActionCopyImageV1ActionsCopyImagePost, HTTPValidationError]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyImageInput,
) -> Response[
    Union[ApiActionCopyImageV1ActionsCopyImagePostResponseApiActionCopyImageV1ActionsCopyImagePost, HTTPValidationError]
]:
    """Api Action Copy Image

     Copy image from one item to another.

    This will invoke copying of content, preview and a thumbnail.

    Args:
        body (CopyImageInput): Info about affected items.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiActionCopyImageV1ActionsCopyImagePostResponseApiActionCopyImageV1ActionsCopyImagePost, HTTPValidationError]]
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
    body: CopyImageInput,
) -> Optional[
    Union[ApiActionCopyImageV1ActionsCopyImagePostResponseApiActionCopyImageV1ActionsCopyImagePost, HTTPValidationError]
]:
    """Api Action Copy Image

     Copy image from one item to another.

    This will invoke copying of content, preview and a thumbnail.

    Args:
        body (CopyImageInput): Info about affected items.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiActionCopyImageV1ActionsCopyImagePostResponseApiActionCopyImageV1ActionsCopyImagePost, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyImageInput,
) -> Response[
    Union[ApiActionCopyImageV1ActionsCopyImagePostResponseApiActionCopyImageV1ActionsCopyImagePost, HTTPValidationError]
]:
    """Api Action Copy Image

     Copy image from one item to another.

    This will invoke copying of content, preview and a thumbnail.

    Args:
        body (CopyImageInput): Info about affected items.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiActionCopyImageV1ActionsCopyImagePostResponseApiActionCopyImageV1ActionsCopyImagePost, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyImageInput,
) -> Optional[
    Union[ApiActionCopyImageV1ActionsCopyImagePostResponseApiActionCopyImageV1ActionsCopyImagePost, HTTPValidationError]
]:
    """Api Action Copy Image

     Copy image from one item to another.

    This will invoke copying of content, preview and a thumbnail.

    Args:
        body (CopyImageInput): Info about affected items.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiActionCopyImageV1ActionsCopyImagePostResponseApiActionCopyImageV1ActionsCopyImagePost, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
