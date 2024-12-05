from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.model_deployment_metrics import ModelDeploymentMetrics
from ...types import Response


def _get_kwargs(
    model_name: str,
    environment_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/models/{model_name}/deployments/{environment_name}/metrics",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ModelDeploymentMetrics]:
    if response.status_code == 200:
        response_200 = ModelDeploymentMetrics.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ModelDeploymentMetrics]:
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
) -> Response[ModelDeploymentMetrics]:
    """Returns metrics for a model deployment by name.

    Args:
        model_name (str):
        environment_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelDeploymentMetrics]
    """

    kwargs = _get_kwargs(
        model_name=model_name,
        environment_name=environment_name,
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
) -> Optional[ModelDeploymentMetrics]:
    """Returns metrics for a model deployment by name.

    Args:
        model_name (str):
        environment_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ModelDeploymentMetrics
    """

    return sync_detailed(
        model_name=model_name,
        environment_name=environment_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    model_name: str,
    environment_name: str,
    *,
    client: AuthenticatedClient,
) -> Response[ModelDeploymentMetrics]:
    """Returns metrics for a model deployment by name.

    Args:
        model_name (str):
        environment_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelDeploymentMetrics]
    """

    kwargs = _get_kwargs(
        model_name=model_name,
        environment_name=environment_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    model_name: str,
    environment_name: str,
    *,
    client: AuthenticatedClient,
) -> Optional[ModelDeploymentMetrics]:
    """Returns metrics for a model deployment by name.

    Args:
        model_name (str):
        environment_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ModelDeploymentMetrics
    """

    return (
        await asyncio_detailed(
            model_name=model_name,
            environment_name=environment_name,
            client=client,
        )
    ).parsed
