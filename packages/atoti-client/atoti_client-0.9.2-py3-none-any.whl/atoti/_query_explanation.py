from __future__ import annotations

from typing import Annotated, TypeAlias, final

from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass

from ._collections import FrozenMapping, FrozenSequence
from ._identification import MeasureName
from ._pydantic import (
    PYDANTIC_CONFIG as __PYDANTIC_CONFIG,
    create_camel_case_alias_generator,
)

_PYDANTIC_CONFIG: ConfigDict = {
    **__PYDANTIC_CONFIG,
    "alias_generator": create_camel_case_alias_generator(),
    "arbitrary_types_allowed": False,
    "extra": "ignore",
}


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class QueryFilter:
    id: int
    description: str


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class AggregateRetrieval:
    id: Annotated[int, Field(alias="retrievalId")]
    filter_id: int
    measure_names: Annotated[FrozenSequence[MeasureName], Field(alias="measures")]
    type: str


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class DatabaseRetrieval:
    id: Annotated[int, Field(alias="retrievalId")]


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class QueryPlan:
    info: Annotated[FrozenMapping[str, object], Field(alias="planInfo")]
    aggregate_retrievals: FrozenSequence[AggregateRetrieval]
    dependencies: FrozenMapping[str, FrozenSequence[int]]
    database_retrievals: FrozenSequence[DatabaseRetrieval]
    database_dependencies: FrozenMapping[str, FrozenSequence[int]]
    filters: Annotated[FrozenSequence[QueryFilter], Field(alias="queryFilters")]
    summary: Annotated[FrozenMapping[str, object], Field(alias="querySummary")]


QueryExplanation: TypeAlias = FrozenSequence[QueryPlan]
