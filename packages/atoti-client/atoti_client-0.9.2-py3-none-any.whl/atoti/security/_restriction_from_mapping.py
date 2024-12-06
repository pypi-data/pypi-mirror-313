from __future__ import annotations

from collections.abc import Collection, Mapping

from .._constant import Constant
from .._identification import ColumnIdentifier, TableIdentifier
from .._operation import IsinCondition, combine_conditions
from ._restriction import Restriction


def restriction_from_mapping(
    restriction: Mapping[str, Mapping[str, Collection[str]]],
    /,
) -> Restriction:
    conditions = [
        IsinCondition[ColumnIdentifier, Constant](
            subject=ColumnIdentifier(TableIdentifier(table_name), column_name),
            elements={Constant.of(element) for element in elements},
        ).normalized
        for table_name, column_restriction in restriction.items()
        for column_name, elements in column_restriction.items()
    ]
    return combine_conditions((conditions,))
