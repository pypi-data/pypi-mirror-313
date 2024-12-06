from collections import defaultdict
from collections.abc import Sequence
from math import ceil
from typing import final

import pandas as pd
from typing_extensions import TypedDict, assert_never

from .._activeviam_client import ActiveViamClient
from .._constant import Constant
from .._gaq_filter import GaqFilter
from .._identification import LevelIdentifier, MeasureIdentifier
from .._operation import decombine_condition
from .._typing import Duration
from ._execute_arrow_query import execute_arrow_query


@final
class _GaqOptions(TypedDict):
    equalConditions: dict[str, str]
    isinConditions: dict[str, list[str]]
    neConditions: dict[str, list[str]]


def _gaq_options_from_gaq_filter(
    condition: GaqFilter | None,
    /,
) -> _GaqOptions:
    serialized_conditions: _GaqOptions = {
        "equalConditions": {},
        "isinConditions": defaultdict(list),
        "neConditions": defaultdict(list),
    }

    if condition is None:
        return serialized_conditions

    (
        level_conditions,
        level_isin_conditions,
        hierarchy_isin_conditions,
    ) = decombine_condition(  # type: ignore[type-var]
        condition,
        allowed_subject_types=(LevelIdentifier,),
        allowed_comparison_operators=("eq", "ne"),
        allowed_target_types=(Constant,),
        allowed_combination_operators=("and",),
        allowed_isin_element_types=(Constant,),
    )[0]

    assert not hierarchy_isin_conditions

    for level_condition in level_conditions:
        if level_condition.operator == "eq":
            serialized_conditions["equalConditions"][
                level_condition.subject._java_description
            ] = str(level_condition.target._legacy_value_json)
        elif level_condition.operator == "ne":
            serialized_conditions["neConditions"][
                level_condition.subject._java_description
            ].append(str(level_condition.target._legacy_value_json))
        else:
            assert_never(level_condition.operator)  # type: ignore[arg-type]

    for level_isin_condition in level_isin_conditions:
        for element in sorted(level_isin_condition.elements):
            serialized_conditions["isinConditions"][
                level_isin_condition.subject._java_description
            ].append(str(element._legacy_value_json))

    return serialized_conditions


def execute_gaq(
    *,
    activeviam_client: ActiveViamClient,
    cube_name: str,
    filter: GaqFilter | None,  # noqa: A002
    level_identifiers: Sequence[LevelIdentifier],
    measure_identifiers: Sequence[MeasureIdentifier],
    scenario_name: str | None,
    timeout: Duration,
) -> pd.DataFrame:
    body = {
        "cubeName": cube_name,
        "branch": scenario_name,
        "measures": [
            measure_identifier.measure_name
            for measure_identifier in measure_identifiers
        ],
        "levelCoordinates": [
            level_identifier._java_description for level_identifier in level_identifiers
        ],
        **_gaq_options_from_gaq_filter(filter),
        "timeout": ceil(timeout.total_seconds()),
    }

    path = activeviam_client.get_endpoint_path(namespace="atoti", route="arrow/query")

    return execute_arrow_query(
        activeviam_client=activeviam_client,
        body=body,
        path=path,
    )
