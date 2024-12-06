from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.log_embedding_request import LogEmbeddingRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: LogEmbeddingRequest,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(x_whylabs_api_key, Unset):
        headers["X-Whylabs-API-Key"] = x_whylabs_api_key

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/log-embeddings",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = response.json()
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
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: LogEmbeddingRequest,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    r"""Profile embeddings

     This endpoint requires a custom configuration to set up before hand. See
    https://docs.whylabs.ai/docs/integrations-whylogs-container/
    for setting up embeddings support.

    Log embeddings data. The Swagger UI isn't able to call this currently.

    ## Sample curl request:

    ```bash
    curl -X 'POST'         -H \"X-API-Key: <password>\"         -H \"Content-Type: application/octet-
    stream\"         'http://localhost:8000/log-embeddings'         --data-raw '{
        \"datasetId\": \"model-62\",
        \"timestamp\": 1634235000,
        \"embeddings\": {
            \"embeddings\": [[0.12, 0.45, 0.33, 0.92]]
        }
    }'
    ```

    ## Sample Python request (using `requests`):
    ```python
    import requests

    # Define your API key
    api_key = \"<password>\"

    # API endpoint
    url = 'http://localhost:8000/log-embeddings'

    # Sample data
    data = {
        \"datasetId\": \"model-62\",
        \"timestamp\": 1634235000,  # an example timestamp
        \"embeddings\": {
            \"embeddings\": [[0.12, 0.45, 0.33, 0.92]]
        }
    }

    # Make the POST request
    headers = {\"X-API-Key\": api_key, \"Content-Type\": \"application/octet-stream\"}
    response = requests.post(url, json=data, headers=headers)
    ```

    Args:
        x_whylabs_api_key (Union[None, Unset, str]):
        body (LogEmbeddingRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
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
    body: LogEmbeddingRequest,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    r"""Profile embeddings

     This endpoint requires a custom configuration to set up before hand. See
    https://docs.whylabs.ai/docs/integrations-whylogs-container/
    for setting up embeddings support.

    Log embeddings data. The Swagger UI isn't able to call this currently.

    ## Sample curl request:

    ```bash
    curl -X 'POST'         -H \"X-API-Key: <password>\"         -H \"Content-Type: application/octet-
    stream\"         'http://localhost:8000/log-embeddings'         --data-raw '{
        \"datasetId\": \"model-62\",
        \"timestamp\": 1634235000,
        \"embeddings\": {
            \"embeddings\": [[0.12, 0.45, 0.33, 0.92]]
        }
    }'
    ```

    ## Sample Python request (using `requests`):
    ```python
    import requests

    # Define your API key
    api_key = \"<password>\"

    # API endpoint
    url = 'http://localhost:8000/log-embeddings'

    # Sample data
    data = {
        \"datasetId\": \"model-62\",
        \"timestamp\": 1634235000,  # an example timestamp
        \"embeddings\": {
            \"embeddings\": [[0.12, 0.45, 0.33, 0.92]]
        }
    }

    # Make the POST request
    headers = {\"X-API-Key\": api_key, \"Content-Type\": \"application/octet-stream\"}
    response = requests.post(url, json=data, headers=headers)
    ```

    Args:
        x_whylabs_api_key (Union[None, Unset, str]):
        body (LogEmbeddingRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        body=body,
        x_whylabs_api_key=x_whylabs_api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: LogEmbeddingRequest,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    r"""Profile embeddings

     This endpoint requires a custom configuration to set up before hand. See
    https://docs.whylabs.ai/docs/integrations-whylogs-container/
    for setting up embeddings support.

    Log embeddings data. The Swagger UI isn't able to call this currently.

    ## Sample curl request:

    ```bash
    curl -X 'POST'         -H \"X-API-Key: <password>\"         -H \"Content-Type: application/octet-
    stream\"         'http://localhost:8000/log-embeddings'         --data-raw '{
        \"datasetId\": \"model-62\",
        \"timestamp\": 1634235000,
        \"embeddings\": {
            \"embeddings\": [[0.12, 0.45, 0.33, 0.92]]
        }
    }'
    ```

    ## Sample Python request (using `requests`):
    ```python
    import requests

    # Define your API key
    api_key = \"<password>\"

    # API endpoint
    url = 'http://localhost:8000/log-embeddings'

    # Sample data
    data = {
        \"datasetId\": \"model-62\",
        \"timestamp\": 1634235000,  # an example timestamp
        \"embeddings\": {
            \"embeddings\": [[0.12, 0.45, 0.33, 0.92]]
        }
    }

    # Make the POST request
    headers = {\"X-API-Key\": api_key, \"Content-Type\": \"application/octet-stream\"}
    response = requests.post(url, json=data, headers=headers)
    ```

    Args:
        x_whylabs_api_key (Union[None, Unset, str]):
        body (LogEmbeddingRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
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
    body: LogEmbeddingRequest,
    x_whylabs_api_key: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    r"""Profile embeddings

     This endpoint requires a custom configuration to set up before hand. See
    https://docs.whylabs.ai/docs/integrations-whylogs-container/
    for setting up embeddings support.

    Log embeddings data. The Swagger UI isn't able to call this currently.

    ## Sample curl request:

    ```bash
    curl -X 'POST'         -H \"X-API-Key: <password>\"         -H \"Content-Type: application/octet-
    stream\"         'http://localhost:8000/log-embeddings'         --data-raw '{
        \"datasetId\": \"model-62\",
        \"timestamp\": 1634235000,
        \"embeddings\": {
            \"embeddings\": [[0.12, 0.45, 0.33, 0.92]]
        }
    }'
    ```

    ## Sample Python request (using `requests`):
    ```python
    import requests

    # Define your API key
    api_key = \"<password>\"

    # API endpoint
    url = 'http://localhost:8000/log-embeddings'

    # Sample data
    data = {
        \"datasetId\": \"model-62\",
        \"timestamp\": 1634235000,  # an example timestamp
        \"embeddings\": {
            \"embeddings\": [[0.12, 0.45, 0.33, 0.92]]
        }
    }

    # Make the POST request
    headers = {\"X-API-Key\": api_key, \"Content-Type\": \"application/octet-stream\"}
    response = requests.post(url, json=data, headers=headers)
    ```

    Args:
        x_whylabs_api_key (Union[None, Unset, str]):
        body (LogEmbeddingRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_whylabs_api_key=x_whylabs_api_key,
        )
    ).parsed
