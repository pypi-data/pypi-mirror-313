from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.environment import Environment
from ...types import Response


def _get_kwargs(
    environment_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/environments/{environment_name}",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Environment]:
    if response.status_code == 200:
        response_200 = Environment.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Environment]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    environment_name: str,
    *,
    client: AuthenticatedClient,
) -> Response[Environment]:
    """Delete environment

     Deletes an environment by name.

    Args:
        environment_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Environment]
    """

    kwargs = _get_kwargs(
        environment_name=environment_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    environment_name: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Environment]:
    """Delete environment

     Deletes an environment by name.

    Args:
        environment_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Environment
    """

    return sync_detailed(
        environment_name=environment_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    environment_name: str,
    *,
    client: AuthenticatedClient,
) -> Response[Environment]:
    """Delete environment

     Deletes an environment by name.

    Args:
        environment_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Environment]
    """

    kwargs = _get_kwargs(
        environment_name=environment_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    environment_name: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Environment]:
    """Delete environment

     Deletes an environment by name.

    Args:
        environment_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Environment
    """

    return (
        await asyncio_detailed(
            environment_name=environment_name,
            client=client,
        )
    ).parsed
