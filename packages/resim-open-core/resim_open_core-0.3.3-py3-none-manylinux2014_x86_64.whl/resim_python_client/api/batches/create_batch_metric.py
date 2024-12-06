from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from typing import Dict
from ...models.batch_metric import BatchMetric
from typing import cast



def _get_kwargs(
    project_id: str,
    batch_id: str,
    *,
    body: BatchMetric,

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}


    

    

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_id}/batches/{batch_id}/metrics".format(project_id=project_id,batch_id=batch_id,),
    }

    _body = body.to_dict()


    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, BatchMetric]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = BatchMetric.from_dict(response.json())



        return response_201
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, BatchMetric]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    batch_id: str,
    *,
    client: AuthenticatedClient,
    body: BatchMetric,

) -> Response[Union[Any, BatchMetric]]:
    """  Adds a batch metric. ID and location should be omitted and will be returned in the response.

    Args:
        project_id (str):
        batch_id (str):
        body (BatchMetric):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BatchMetric]]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
batch_id=batch_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    batch_id: str,
    *,
    client: AuthenticatedClient,
    body: BatchMetric,

) -> Optional[Union[Any, BatchMetric]]:
    """  Adds a batch metric. ID and location should be omitted and will be returned in the response.

    Args:
        project_id (str):
        batch_id (str):
        body (BatchMetric):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BatchMetric]
     """


    return sync_detailed(
        project_id=project_id,
batch_id=batch_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    batch_id: str,
    *,
    client: AuthenticatedClient,
    body: BatchMetric,

) -> Response[Union[Any, BatchMetric]]:
    """  Adds a batch metric. ID and location should be omitted and will be returned in the response.

    Args:
        project_id (str):
        batch_id (str):
        body (BatchMetric):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BatchMetric]]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
batch_id=batch_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    batch_id: str,
    *,
    client: AuthenticatedClient,
    body: BatchMetric,

) -> Optional[Union[Any, BatchMetric]]:
    """  Adds a batch metric. ID and location should be omitted and will be returned in the response.

    Args:
        project_id (str):
        batch_id (str):
        body (BatchMetric):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BatchMetric]
     """


    return (await asyncio_detailed(
        project_id=project_id,
batch_id=batch_id,
client=client,
body=body,

    )).parsed
