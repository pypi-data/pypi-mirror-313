from typing import Literal, final

from pydantic.dataclasses import dataclass

from ..._collections import FrozenMapping, FrozenSequence
from ..._constant import Constant
from ..._identification import (
    ColumnIdentifier,
    ExternalColumnIdentifier,
    ExternalTableIdentifier,
    Identifiable,
    TableIdentifier,
)
from ..._operation import Condition
from ..._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from ._external_measure import ExternalMeasure

_Filter = Condition[
    ColumnIdentifier,
    Literal["eq", "isin"],
    Constant,
    Literal["and"] | None,
]


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class ExternalAggregateTable:
    """An external aggregate table is a table in the external database containing aggregated data.

    It is used to feed some partial providers faster.
    For instance, if the same aggregate query is run every day to feed the same partial provider with the same data, the result of the query can instead be stored into an external table and this table used to feed the provider every day.
    """

    granular_table: Identifiable[TableIdentifier]
    """The table containing the granular facts, i.e. the fact table from which the data has been aggregated into the aggregate table."""

    aggregate_table: Identifiable[ExternalTableIdentifier]

    mapping: FrozenMapping[
        Identifiable[ColumnIdentifier],
        Identifiable[ExternalColumnIdentifier],
    ]
    """The mapping from one column in :attr:granular_table` (or a table joined to it) to the corresponding column in :attr:`aggregate_table`."""

    measures: FrozenSequence[ExternalMeasure]
    """The measures provided by :attr:`aggregate_table`."""

    filter: _Filter | None = None
    """The condition on the granular columns describing which facts have been pre-aggregated into the external table.

    The columns used in the condition must be keys of :attr:`mapping`."""
