from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_action_rebuild_computed_tags_v1_actions_rebuild_computed_tags_post_response_api_action_rebuild_computed_tags_v1_actions_rebuild_computed_tags_post import (
    ApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPostResponseApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPost,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.rebuild_computed_tags_input import RebuildComputedTagsInput
from ...types import Response


def _get_kwargs(
    *,
    body: RebuildComputedTagsInput,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/v1/actions/rebuild_computed_tags",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        ApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPostResponseApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPost,
        HTTPValidationError,
    ]
]:
    if response.status_code == 202:
        response_202 = ApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPostResponseApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPost.from_dict(
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
    Union[
        ApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPostResponseApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPost,
        HTTPValidationError,
    ]
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
    body: RebuildComputedTagsInput,
) -> Response[
    Union[
        ApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPostResponseApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPost,
        HTTPValidationError,
    ]
]:
    """Api Action Rebuild Computed Tags

     Recalculate all computed tags for specific user.

    As a starting point we will take root item for this user.
    If `including_children` is set to True, this will also affect all
    descendants of the item. This operation potentially can take a lot of time.

    Args:
        body (RebuildComputedTagsInput): Info about target user for tag rebuilding.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPostResponseApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPost, HTTPValidationError]]
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
    body: RebuildComputedTagsInput,
) -> Optional[
    Union[
        ApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPostResponseApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPost,
        HTTPValidationError,
    ]
]:
    """Api Action Rebuild Computed Tags

     Recalculate all computed tags for specific user.

    As a starting point we will take root item for this user.
    If `including_children` is set to True, this will also affect all
    descendants of the item. This operation potentially can take a lot of time.

    Args:
        body (RebuildComputedTagsInput): Info about target user for tag rebuilding.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPostResponseApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPost, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RebuildComputedTagsInput,
) -> Response[
    Union[
        ApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPostResponseApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPost,
        HTTPValidationError,
    ]
]:
    """Api Action Rebuild Computed Tags

     Recalculate all computed tags for specific user.

    As a starting point we will take root item for this user.
    If `including_children` is set to True, this will also affect all
    descendants of the item. This operation potentially can take a lot of time.

    Args:
        body (RebuildComputedTagsInput): Info about target user for tag rebuilding.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPostResponseApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPost, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RebuildComputedTagsInput,
) -> Optional[
    Union[
        ApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPostResponseApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPost,
        HTTPValidationError,
    ]
]:
    """Api Action Rebuild Computed Tags

     Recalculate all computed tags for specific user.

    As a starting point we will take root item for this user.
    If `including_children` is set to True, this will also affect all
    descendants of the item. This operation potentially can take a lot of time.

    Args:
        body (RebuildComputedTagsInput): Info about target user for tag rebuilding.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPostResponseApiActionRebuildComputedTagsV1ActionsRebuildComputedTagsPost, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
