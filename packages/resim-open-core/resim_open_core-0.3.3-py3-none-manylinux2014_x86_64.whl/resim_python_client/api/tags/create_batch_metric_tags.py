from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from typing import Dict
from typing import cast, List
from typing import cast
from ...models.metric_tag import MetricTag



def _get_kwargs(
    project_id: str,
    batch_id: str,
    metric_id: str,
    *,
    body: List['MetricTag'],

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}


    

    

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_id}/batches/{batch_id}/metrics/{metric_id}/tags".format(project_id=project_id,batch_id=batch_id,metric_id=metric_id,),
    }

    _body = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _body.append(body_item)




    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, List['MetricTag']]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in (_response_201):
            response_201_item = MetricTag.from_dict(response_201_item_data)



            response_201.append(response_201_item)

        return response_201
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, List['MetricTag']]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    batch_id: str,
    metric_id: str,
    *,
    client: AuthenticatedClient,
    body: List['MetricTag'],

) -> Response[Union[Any, List['MetricTag']]]:
    """  Adds tags to the given batch metric

    Args:
        project_id (str):
        batch_id (str):
        metric_id (str):
        body (List['MetricTag']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['MetricTag']]]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
batch_id=batch_id,
metric_id=metric_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    batch_id: str,
    metric_id: str,
    *,
    client: AuthenticatedClient,
    body: List['MetricTag'],

) -> Optional[Union[Any, List['MetricTag']]]:
    """  Adds tags to the given batch metric

    Args:
        project_id (str):
        batch_id (str):
        metric_id (str):
        body (List['MetricTag']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['MetricTag']]
     """


    return sync_detailed(
        project_id=project_id,
batch_id=batch_id,
metric_id=metric_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    batch_id: str,
    metric_id: str,
    *,
    client: AuthenticatedClient,
    body: List['MetricTag'],

) -> Response[Union[Any, List['MetricTag']]]:
    """  Adds tags to the given batch metric

    Args:
        project_id (str):
        batch_id (str):
        metric_id (str):
        body (List['MetricTag']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['MetricTag']]]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
batch_id=batch_id,
metric_id=metric_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    batch_id: str,
    metric_id: str,
    *,
    client: AuthenticatedClient,
    body: List['MetricTag'],

) -> Optional[Union[Any, List['MetricTag']]]:
    """  Adds tags to the given batch metric

    Args:
        project_id (str):
        batch_id (str):
        metric_id (str):
        body (List['MetricTag']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['MetricTag']]
     """


    return (await asyncio_detailed(
        project_id=project_id,
batch_id=batch_id,
metric_id=metric_id,
client=client,
body=body,

    )).parsed
