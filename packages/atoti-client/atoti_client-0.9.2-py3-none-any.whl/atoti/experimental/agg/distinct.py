from __future__ import annotations

from typing import overload

from ..._measure_convertible import VariableMeasureConvertible
from ..._measure_description import MeasureDescription
from ...agg._agg import agg
from ...agg._utils import LevelOrVariableColumnConvertible
from ...scope._scope import Scope


@overload
def distinct(operand: LevelOrVariableColumnConvertible, /) -> MeasureDescription: ...


@overload
def distinct(
    operand: VariableMeasureConvertible,
    /,
    *,
    scope: Scope,
) -> MeasureDescription: ...


def distinct(
    operand: LevelOrVariableColumnConvertible | VariableMeasureConvertible,
    /,
    *,
    scope: Scope | None = None,
) -> MeasureDescription:
    """Return an array measure representing the distinct values of the passed measure."""
    # The type checkers cannot see that the `@overload` above ensure that this call is valid.
    return agg(operand, plugin_key="DISTINCT", scope=scope)  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]
