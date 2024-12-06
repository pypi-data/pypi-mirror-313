from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.report_log_input import ReportLogInput
from ...models.report_log import ReportLog
from typing import cast
from typing import Dict



def _get_kwargs(
    project_id: str,
    report_id: str,
    *,
    body: ReportLogInput,

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}


    

    

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_id}/reports/{report_id}/logs".format(project_id=project_id,report_id=report_id,),
    }

    _body = body.to_dict()


    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, ReportLog]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = ReportLog.from_dict(response.json())



        return response_201
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, ReportLog]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    report_id: str,
    *,
    client: AuthenticatedClient,
    body: ReportLogInput,

) -> Response[Union[Any, ReportLog]]:
    """  Adds a log

    Args:
        project_id (str):
        report_id (str):
        body (ReportLogInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ReportLog]]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
report_id=report_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    report_id: str,
    *,
    client: AuthenticatedClient,
    body: ReportLogInput,

) -> Optional[Union[Any, ReportLog]]:
    """  Adds a log

    Args:
        project_id (str):
        report_id (str):
        body (ReportLogInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ReportLog]
     """


    return sync_detailed(
        project_id=project_id,
report_id=report_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    report_id: str,
    *,
    client: AuthenticatedClient,
    body: ReportLogInput,

) -> Response[Union[Any, ReportLog]]:
    """  Adds a log

    Args:
        project_id (str):
        report_id (str):
        body (ReportLogInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ReportLog]]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
report_id=report_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    report_id: str,
    *,
    client: AuthenticatedClient,
    body: ReportLogInput,

) -> Optional[Union[Any, ReportLog]]:
    """  Adds a log

    Args:
        project_id (str):
        report_id (str):
        body (ReportLogInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ReportLog]
     """


    return (await asyncio_detailed(
        project_id=project_id,
report_id=report_id,
client=client,
body=body,

    )).parsed
