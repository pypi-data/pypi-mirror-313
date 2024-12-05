from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.model_deployment import ModelDeployment
from ...types import Response


def _get_kwargs(
    model_name: str,
    environment_name: str,
    *,
    body: ModelDeployment,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/models/{model_name}/deployments/{environment_name}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ModelDeployment]:
    if response.status_code == 200:
        response_200 = ModelDeployment.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ModelDeployment]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    model_name: str,
    environment_name: str,
    *,
    client: AuthenticatedClient,
    body: ModelDeployment,
) -> Response[ModelDeployment]:
    """Create or update model deployment

     Creates or updates a deployment for a model by name.

    Args:
        model_name (str):
        environment_name (str):
        body (ModelDeployment): An instance of a model, deployed in a specific environment

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelDeployment]
    """

    kwargs = _get_kwargs(
        model_name=model_name,
        environment_name=environment_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    model_name: str,
    environment_name: str,
    *,
    client: AuthenticatedClient,
    body: ModelDeployment,
) -> Optional[ModelDeployment]:
    """Create or update model deployment

     Creates or updates a deployment for a model by name.

    Args:
        model_name (str):
        environment_name (str):
        body (ModelDeployment): An instance of a model, deployed in a specific environment

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ModelDeployment
    """

    return sync_detailed(
        model_name=model_name,
        environment_name=environment_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    model_name: str,
    environment_name: str,
    *,
    client: AuthenticatedClient,
    body: ModelDeployment,
) -> Response[ModelDeployment]:
    """Create or update model deployment

     Creates or updates a deployment for a model by name.

    Args:
        model_name (str):
        environment_name (str):
        body (ModelDeployment): An instance of a model, deployed in a specific environment

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelDeployment]
    """

    kwargs = _get_kwargs(
        model_name=model_name,
        environment_name=environment_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    model_name: str,
    environment_name: str,
    *,
    client: AuthenticatedClient,
    body: ModelDeployment,
) -> Optional[ModelDeployment]:
    """Create or update model deployment

     Creates or updates a deployment for a model by name.

    Args:
        model_name (str):
        environment_name (str):
        body (ModelDeployment): An instance of a model, deployed in a specific environment

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ModelDeployment
    """

    return (
        await asyncio_detailed(
            model_name=model_name,
            environment_name=environment_name,
            client=client,
            body=body,
        )
    ).parsed
