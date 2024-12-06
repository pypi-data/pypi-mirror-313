from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.debug_policies_response_debug_policies import DebugPoliciesResponseDebugPolicies
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(x_whylabs_api_key, Unset):
        headers["X-Whylabs-API-Key"] = x_whylabs_api_key

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/debug/policies",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DebugPoliciesResponseDebugPolicies, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DebugPoliciesResponseDebugPolicies.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DebugPoliciesResponseDebugPolicies, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[DebugPoliciesResponseDebugPolicies, HTTPValidationError]]:
    """Dump debug information about the known policies.

    Args:
        x_whylabs_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DebugPoliciesResponseDebugPolicies, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        x_whylabs_api_key=x_whylabs_api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[DebugPoliciesResponseDebugPolicies, HTTPValidationError]]:
    """Dump debug information about the known policies.

    Args:
        x_whylabs_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DebugPoliciesResponseDebugPolicies, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        x_whylabs_api_key=x_whylabs_api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[DebugPoliciesResponseDebugPolicies, HTTPValidationError]]:
    """Dump debug information about the known policies.

    Args:
        x_whylabs_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DebugPoliciesResponseDebugPolicies, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        x_whylabs_api_key=x_whylabs_api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[DebugPoliciesResponseDebugPolicies, HTTPValidationError]]:
    """Dump debug information about the known policies.

    Args:
        x_whylabs_api_key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DebugPoliciesResponseDebugPolicies, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            x_whylabs_api_key=x_whylabs_api_key,
        )
    ).parsed
