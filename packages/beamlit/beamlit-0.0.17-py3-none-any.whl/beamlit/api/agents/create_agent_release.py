from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_release import AgentRelease
from ...types import Response


def _get_kwargs(
    agent_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/agents/{agent_name}/release",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AgentRelease]:
    if response.status_code == 200:
        response_200 = AgentRelease.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AgentRelease]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_name: str,
    *,
    client: AuthenticatedClient,
) -> Response[AgentRelease]:
    """Create release for a agent from an environment

    Args:
        agent_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentRelease]
    """

    kwargs = _get_kwargs(
        agent_name=agent_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    agent_name: str,
    *,
    client: AuthenticatedClient,
) -> Optional[AgentRelease]:
    """Create release for a agent from an environment

    Args:
        agent_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentRelease
    """

    return sync_detailed(
        agent_name=agent_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    agent_name: str,
    *,
    client: AuthenticatedClient,
) -> Response[AgentRelease]:
    """Create release for a agent from an environment

    Args:
        agent_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentRelease]
    """

    kwargs = _get_kwargs(
        agent_name=agent_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    agent_name: str,
    *,
    client: AuthenticatedClient,
) -> Optional[AgentRelease]:
    """Create release for a agent from an environment

    Args:
        agent_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentRelease
    """

    return (
        await asyncio_detailed(
            agent_name=agent_name,
            client=client,
        )
    ).parsed
