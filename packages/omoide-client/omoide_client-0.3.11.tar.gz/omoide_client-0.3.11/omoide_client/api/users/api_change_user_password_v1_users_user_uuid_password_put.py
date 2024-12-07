from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.user_output import UserOutput
from ...models.user_value_input import UserValueInput
from ...types import Response


def _get_kwargs(
    user_uuid: UUID,
    *,
    body: UserValueInput,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/v1/users/{user_uuid}/password",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, UserOutput]]:
    if response.status_code == 202:
        response_202 = UserOutput.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, UserOutput]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UserValueInput,
) -> Response[Union[HTTPValidationError, UserOutput]]:
    """Api Change User Password

     Update password of existing user.

    Args:
        user_uuid (UUID):
        body (UserValueInput): New name/login/password.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UserOutput]]
    """

    kwargs = _get_kwargs(
        user_uuid=user_uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UserValueInput,
) -> Optional[Union[HTTPValidationError, UserOutput]]:
    """Api Change User Password

     Update password of existing user.

    Args:
        user_uuid (UUID):
        body (UserValueInput): New name/login/password.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UserOutput]
    """

    return sync_detailed(
        user_uuid=user_uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    user_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UserValueInput,
) -> Response[Union[HTTPValidationError, UserOutput]]:
    """Api Change User Password

     Update password of existing user.

    Args:
        user_uuid (UUID):
        body (UserValueInput): New name/login/password.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UserOutput]]
    """

    kwargs = _get_kwargs(
        user_uuid=user_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_uuid: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UserValueInput,
) -> Optional[Union[HTTPValidationError, UserOutput]]:
    """Api Change User Password

     Update password of existing user.

    Args:
        user_uuid (UUID):
        body (UserValueInput): New name/login/password.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UserOutput]
    """

    return (
        await asyncio_detailed(
            user_uuid=user_uuid,
            client=client,
            body=body,
        )
    ).parsed
