from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.model_provider import ModelProvider
from ...types import Response


def _get_kwargs(
    model_provider_name: str,
    *,
    body: ModelProvider,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/model_providers/{model_provider_name}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ModelProvider]:
    if response.status_code == 200:
        response_200 = ModelProvider.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ModelProvider]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    model_provider_name: str,
    *,
    client: AuthenticatedClient,
    body: ModelProvider,
) -> Response[ModelProvider]:
    """Update model provider

     Update an integration by ID.

    Args:
        model_provider_name (str):
        body (ModelProvider): Model provider

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelProvider]
    """

    kwargs = _get_kwargs(
        model_provider_name=model_provider_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    model_provider_name: str,
    *,
    client: AuthenticatedClient,
    body: ModelProvider,
) -> Optional[ModelProvider]:
    """Update model provider

     Update an integration by ID.

    Args:
        model_provider_name (str):
        body (ModelProvider): Model provider

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ModelProvider
    """

    return sync_detailed(
        model_provider_name=model_provider_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    model_provider_name: str,
    *,
    client: AuthenticatedClient,
    body: ModelProvider,
) -> Response[ModelProvider]:
    """Update model provider

     Update an integration by ID.

    Args:
        model_provider_name (str):
        body (ModelProvider): Model provider

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelProvider]
    """

    kwargs = _get_kwargs(
        model_provider_name=model_provider_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    model_provider_name: str,
    *,
    client: AuthenticatedClient,
    body: ModelProvider,
) -> Optional[ModelProvider]:
    """Update model provider

     Update an integration by ID.

    Args:
        model_provider_name (str):
        body (ModelProvider): Model provider

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ModelProvider
    """

    return (
        await asyncio_detailed(
            model_provider_name=model_provider_name,
            client=client,
            body=body,
        )
    ).parsed
