from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_get_anon_tags_v1_users_anon_known_tags_get_response_api_get_anon_tags_v1_users_anon_known_tags_get import (
    ApiGetAnonTagsV1UsersAnonKnownTagsGetResponseApiGetAnonTagsV1UsersAnonKnownTagsGet,
)
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/users/anon/known_tags",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiGetAnonTagsV1UsersAnonKnownTagsGetResponseApiGetAnonTagsV1UsersAnonKnownTagsGet]:
    if response.status_code == 200:
        response_200 = ApiGetAnonTagsV1UsersAnonKnownTagsGetResponseApiGetAnonTagsV1UsersAnonKnownTagsGet.from_dict(
            response.json()
        )

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiGetAnonTagsV1UsersAnonKnownTagsGetResponseApiGetAnonTagsV1UsersAnonKnownTagsGet]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiGetAnonTagsV1UsersAnonKnownTagsGetResponseApiGetAnonTagsV1UsersAnonKnownTagsGet]:
    """Api Get Anon Tags

     Get all known tags for anon user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiGetAnonTagsV1UsersAnonKnownTagsGetResponseApiGetAnonTagsV1UsersAnonKnownTagsGet]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiGetAnonTagsV1UsersAnonKnownTagsGetResponseApiGetAnonTagsV1UsersAnonKnownTagsGet]:
    """Api Get Anon Tags

     Get all known tags for anon user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiGetAnonTagsV1UsersAnonKnownTagsGetResponseApiGetAnonTagsV1UsersAnonKnownTagsGet
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiGetAnonTagsV1UsersAnonKnownTagsGetResponseApiGetAnonTagsV1UsersAnonKnownTagsGet]:
    """Api Get Anon Tags

     Get all known tags for anon user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiGetAnonTagsV1UsersAnonKnownTagsGetResponseApiGetAnonTagsV1UsersAnonKnownTagsGet]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiGetAnonTagsV1UsersAnonKnownTagsGetResponseApiGetAnonTagsV1UsersAnonKnownTagsGet]:
    """Api Get Anon Tags

     Get all known tags for anon user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiGetAnonTagsV1UsersAnonKnownTagsGetResponseApiGetAnonTagsV1UsersAnonKnownTagsGet
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
