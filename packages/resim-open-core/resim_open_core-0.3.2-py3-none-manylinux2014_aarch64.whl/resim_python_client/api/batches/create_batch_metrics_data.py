from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from typing import cast
from ...models.batch_metrics_data import BatchMetricsData
from typing import Dict



def _get_kwargs(
    project_id: str,
    batch_id: str,
    *,
    body: BatchMetricsData,

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}


    

    

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_id}/batches/{batch_id}/metricsData".format(project_id=project_id,batch_id=batch_id,),
    }

    _body = body.to_dict()


    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, BatchMetricsData]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = BatchMetricsData.from_dict(response.json())



        return response_201
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, BatchMetricsData]]:
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
    body: BatchMetricsData,

) -> Response[Union[Any, BatchMetricsData]]:
    """  Creates a new metrics data associated with a batch. If this metrics data is an external file, then
    the filename field must be populated.

    Args:
        project_id (str):
        batch_id (str):
        body (BatchMetricsData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BatchMetricsData]]
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
    body: BatchMetricsData,

) -> Optional[Union[Any, BatchMetricsData]]:
    """  Creates a new metrics data associated with a batch. If this metrics data is an external file, then
    the filename field must be populated.

    Args:
        project_id (str):
        batch_id (str):
        body (BatchMetricsData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BatchMetricsData]
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
    body: BatchMetricsData,

) -> Response[Union[Any, BatchMetricsData]]:
    """  Creates a new metrics data associated with a batch. If this metrics data is an external file, then
    the filename field must be populated.

    Args:
        project_id (str):
        batch_id (str):
        body (BatchMetricsData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BatchMetricsData]]
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
    body: BatchMetricsData,

) -> Optional[Union[Any, BatchMetricsData]]:
    """  Creates a new metrics data associated with a batch. If this metrics data is an external file, then
    the filename field must be populated.

    Args:
        project_id (str):
        batch_id (str):
        body (BatchMetricsData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BatchMetricsData]
     """


    return (await asyncio_detailed(
        project_id=project_id,
batch_id=batch_id,
client=client,
body=body,

    )).parsed
