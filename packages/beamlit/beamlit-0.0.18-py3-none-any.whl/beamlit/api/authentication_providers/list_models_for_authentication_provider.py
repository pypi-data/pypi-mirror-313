from http import HTTPStatus
from typing import Any, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.authentication_provider_model import AuthenticationProviderModel
from ...types import Response


def _get_kwargs(
    authentication_provider_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/authentication_providers/{authentication_provider_name}/models",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["AuthenticationProviderModel"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AuthenticationProviderModel.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["AuthenticationProviderModel"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    authentication_provider_name: str,
    *,
    client: AuthenticatedClient,
) -> Response[List["AuthenticationProviderModel"]]:
    """List models for a authentication provider

     Returns a list of all models for an integration by ID.

    Args:
        authentication_provider_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['AuthenticationProviderModel']]
    """

    kwargs = _get_kwargs(
        authentication_provider_name=authentication_provider_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    authentication_provider_name: str,
    *,
    client: AuthenticatedClient,
) -> Optional[List["AuthenticationProviderModel"]]:
    """List models for a authentication provider

     Returns a list of all models for an integration by ID.

    Args:
        authentication_provider_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['AuthenticationProviderModel']
    """

    return sync_detailed(
        authentication_provider_name=authentication_provider_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    authentication_provider_name: str,
    *,
    client: AuthenticatedClient,
) -> Response[List["AuthenticationProviderModel"]]:
    """List models for a authentication provider

     Returns a list of all models for an integration by ID.

    Args:
        authentication_provider_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['AuthenticationProviderModel']]
    """

    kwargs = _get_kwargs(
        authentication_provider_name=authentication_provider_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    authentication_provider_name: str,
    *,
    client: AuthenticatedClient,
) -> Optional[List["AuthenticationProviderModel"]]:
    """List models for a authentication provider

     Returns a list of all models for an integration by ID.

    Args:
        authentication_provider_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['AuthenticationProviderModel']
    """

    return (
        await asyncio_detailed(
            authentication_provider_name=authentication_provider_name,
            client=client,
        )
    ).parsed
