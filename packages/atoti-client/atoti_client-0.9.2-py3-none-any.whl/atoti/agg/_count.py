from __future__ import annotations

from typing import overload

from .._measure_convertible import VariableMeasureConvertible
from .._measure_description import MeasureDescription
from ..scope._scope import Scope
from ._agg import agg
from ._utils import LevelOrVariableColumnConvertible


@overload
def count(operand: LevelOrVariableColumnConvertible, /) -> MeasureDescription: ...


@overload
def count(
    operand: VariableMeasureConvertible,
    /,
    *,
    scope: Scope,
) -> MeasureDescription: ...


def count(
    operand: LevelOrVariableColumnConvertible | VariableMeasureConvertible,
    /,
    *,
    scope: Scope | None = None,
) -> MeasureDescription:
    """Return a measure equal to the number of aggregated elements.

    See Also:
        :func:`atoti.agg.count_distinct`.
    """
    # The type checkers cannot see that the `@overload` above ensure that this call is valid.
    return agg(operand, plugin_key="COUNT", scope=scope)  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]
