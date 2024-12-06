from collections.abc import Callable
from typing import Literal, overload

import pandas as pd

from .._activeviam_client import ActiveViamClient
from .._cellset import CellSet
from .._cellset_to_mdx_query_result import cellset_to_mdx_query_result
from .._context import Context
from .._cube_discovery import CubeDiscovery
from .._get_data_types import GetDataTypes
from .._typing import Duration
from .._widget_conversion_details import WidgetConversionDetails
from ..mdx_query_result import MdxQueryResult
from ._enrich_mdx_query_context import enrich_mdx_query_context
from ._execute_arrow_query import execute_arrow_query


def _execute_mdx_to_cellset_query(
    *,
    activeviam_client: ActiveViamClient,
    context: Context,
    mdx: str,
    pivot_namespace: str,
) -> CellSet:
    route = activeviam_client.get_endpoint_path(
        namespace=pivot_namespace,
        route="cube/query/mdx",
    )
    response = activeviam_client.http_client.post(
        route,
        json={"context": {**context}, "mdx": mdx},
        # The timeout is part of `context` and is managed by the server.
        timeout=None,
    ).raise_for_status()
    body = response.content
    return activeviam_client.get_json_response_body_type_adapter(CellSet).validate_json(
        body,
    )


@overload
def execute_mdx_query(
    *,
    activeviam_client: ActiveViamClient,
    context: Context,
    get_cube_discovery: Callable[[], CubeDiscovery],
    get_data_types: GetDataTypes | None,
    get_widget_creation_code: Callable[[], str | None],
    has_data_export_service: bool,
    keep_totals: bool,
    mdx: str,
    mode: Literal["pretty"],
    pivot_namespace: str,
    session_id: str,
    timeout: Duration,
) -> MdxQueryResult: ...


@overload
def execute_mdx_query(
    *,
    activeviam_client: ActiveViamClient,
    context: Context,
    get_cube_discovery: Callable[[], CubeDiscovery],
    get_data_types: GetDataTypes | None,
    get_widget_creation_code: Callable[[], str | None],
    has_data_export_service: bool,
    keep_totals: bool,
    mdx: str,
    mode: Literal["raw"],
    pivot_namespace: str,
    session_id: str,
    timeout: Duration,
) -> pd.DataFrame: ...


def execute_mdx_query(
    *,
    activeviam_client: ActiveViamClient,
    context: Context,
    get_cube_discovery: Callable[[], CubeDiscovery],
    get_data_types: GetDataTypes | None,
    get_widget_creation_code: Callable[[], str | None],
    has_data_export_service: bool,
    keep_totals: bool,
    mdx: str,
    mode: Literal["pretty", "raw"],
    pivot_namespace: str,
    session_id: str,
    timeout: Duration,
) -> MdxQueryResult | pd.DataFrame:
    context = enrich_mdx_query_context(context, timeout=timeout)

    if mode == "raw":
        if not has_data_export_service:
            raise NotImplementedError(
                "`raw` mode is not supported by this Atoti Server.",
            )

        return execute_arrow_query(
            activeviam_client=activeviam_client,
            body={
                "jsonMdxQuery": {"mdx": mdx, "context": context},
                "outputConfiguration": {"format": "arrow"},
            },
            path=activeviam_client.get_endpoint_path(
                namespace=pivot_namespace,
                route="cube/dataexport/download",
            ),
        )

    cellset = _execute_mdx_to_cellset_query(
        activeviam_client=activeviam_client,
        context=context,
        mdx=mdx,
        pivot_namespace=pivot_namespace,
    )
    cube_discovery = get_cube_discovery()
    query_result = cellset_to_mdx_query_result(
        cellset,
        context=context,
        cube=cube_discovery.cubes[cellset.cube],
        get_data_types=get_data_types,
        keep_totals=keep_totals,
    )

    widget_creation_code = get_widget_creation_code()
    if widget_creation_code is not None and query_result._atoti_metadata is not None:
        query_result._atoti_metadata = (
            query_result._atoti_metadata.add_widget_conversion_details(
                WidgetConversionDetails(
                    mdx=mdx,
                    sessionId=session_id,
                    widgetCreationCode=widget_creation_code,
                ),
            )
        )

    return query_result
