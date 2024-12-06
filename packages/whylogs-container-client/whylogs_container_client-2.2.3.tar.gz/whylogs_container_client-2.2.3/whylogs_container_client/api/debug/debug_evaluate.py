from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.debug_llm_validate_request import DebugLLMValidateRequest
from ...models.evaluation_result import EvaluationResult
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: DebugLLMValidateRequest,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(x_whylabs_api_key, Unset):
        headers["X-Whylabs-API-Key"] = x_whylabs_api_key

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/debug/evaluate",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[EvaluationResult, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = EvaluationResult.from_dict(response.json())

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
) -> Response[Union[EvaluationResult, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: DebugLLMValidateRequest,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[EvaluationResult, HTTPValidationError]]:
    """Evaluate and log a single prompt/response pair using langkit and a policy file.

    Args:
        x_whylabs_api_key (Union[None, Unset, str]):
        body (DebugLLMValidateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EvaluationResult, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
        x_whylabs_api_key=x_whylabs_api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: DebugLLMValidateRequest,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[EvaluationResult, HTTPValidationError]]:
    """Evaluate and log a single prompt/response pair using langkit and a policy file.

    Args:
        x_whylabs_api_key (Union[None, Unset, str]):
        body (DebugLLMValidateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EvaluationResult, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        body=body,
        x_whylabs_api_key=x_whylabs_api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: DebugLLMValidateRequest,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[EvaluationResult, HTTPValidationError]]:
    """Evaluate and log a single prompt/response pair using langkit and a policy file.

    Args:
        x_whylabs_api_key (Union[None, Unset, str]):
        body (DebugLLMValidateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EvaluationResult, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
        x_whylabs_api_key=x_whylabs_api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: DebugLLMValidateRequest,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[EvaluationResult, HTTPValidationError]]:
    """Evaluate and log a single prompt/response pair using langkit and a policy file.

    Args:
        x_whylabs_api_key (Union[None, Unset, str]):
        body (DebugLLMValidateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EvaluationResult, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_whylabs_api_key=x_whylabs_api_key,
        )
    ).parsed
