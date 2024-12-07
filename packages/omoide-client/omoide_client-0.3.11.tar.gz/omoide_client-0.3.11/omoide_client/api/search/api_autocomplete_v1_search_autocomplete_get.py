from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.autocomplete_output import AutocompleteOutput
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    tag: Union[Unset, str] = "",
    limit: Union[Unset, int] = 10,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["tag"] = tag

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/search/autocomplete",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AutocompleteOutput, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = AutocompleteOutput.from_dict(response.json())

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
) -> Response[Union[AutocompleteOutput, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    tag: Union[Unset, str] = "",
    limit: Union[Unset, int] = 10,
) -> Response[Union[AutocompleteOutput, HTTPValidationError]]:
    """Api Autocomplete

     Return tags that match supplied string.

    You will get list of strings, ordered by their frequency.
    Most popular tags will be at the top.

    This endpoint can be used by anybody, but each user will get tailored
    output. String must be an exact match, no guessing is used.

    Args:
        tag (Union[Unset, str]):  Default: ''.
        limit (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AutocompleteOutput, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        tag=tag,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    tag: Union[Unset, str] = "",
    limit: Union[Unset, int] = 10,
) -> Optional[Union[AutocompleteOutput, HTTPValidationError]]:
    """Api Autocomplete

     Return tags that match supplied string.

    You will get list of strings, ordered by their frequency.
    Most popular tags will be at the top.

    This endpoint can be used by anybody, but each user will get tailored
    output. String must be an exact match, no guessing is used.

    Args:
        tag (Union[Unset, str]):  Default: ''.
        limit (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AutocompleteOutput, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        tag=tag,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    tag: Union[Unset, str] = "",
    limit: Union[Unset, int] = 10,
) -> Response[Union[AutocompleteOutput, HTTPValidationError]]:
    """Api Autocomplete

     Return tags that match supplied string.

    You will get list of strings, ordered by their frequency.
    Most popular tags will be at the top.

    This endpoint can be used by anybody, but each user will get tailored
    output. String must be an exact match, no guessing is used.

    Args:
        tag (Union[Unset, str]):  Default: ''.
        limit (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AutocompleteOutput, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        tag=tag,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    tag: Union[Unset, str] = "",
    limit: Union[Unset, int] = 10,
) -> Optional[Union[AutocompleteOutput, HTTPValidationError]]:
    """Api Autocomplete

     Return tags that match supplied string.

    You will get list of strings, ordered by their frequency.
    Most popular tags will be at the top.

    This endpoint can be used by anybody, but each user will get tailored
    output. String must be an exact match, no guessing is used.

    Args:
        tag (Union[Unset, str]):  Default: ''.
        limit (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AutocompleteOutput, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            tag=tag,
            limit=limit,
        )
    ).parsed
