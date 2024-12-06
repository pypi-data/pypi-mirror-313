from __future__ import annotations

from typing import overload

from .._doc import doc
from .._measure_convertible import VariableMeasureConvertible
from .._measure_description import MeasureDescription
from ..scope._scope import Scope
from ._agg import agg
from ._utils import (
    BASIC_ARGS_DOC as _BASIC_ARGS_DOC,
    BASIC_DOC as _BASIC_DOC,
    LevelOrVariableColumnConvertible,
)


@overload
def mean(operand: LevelOrVariableColumnConvertible, /) -> MeasureDescription: ...


@overload
def mean(
    operand: VariableMeasureConvertible,
    /,
    *,
    scope: Scope,
) -> MeasureDescription: ...


@doc(
    _BASIC_DOC,
    args=_BASIC_ARGS_DOC,
    value="mean",
    example="""
        >>> m["Quantity.MEAN"] = tt.agg.mean(table["Quantity"])
        >>> cube.query(m["Quantity.MEAN"])
          Quantity.MEAN
        0        370.00""".replace("\n", "", 1),
)
def mean(
    operand: LevelOrVariableColumnConvertible | VariableMeasureConvertible,
    /,
    *,
    scope: Scope | None = None,
) -> MeasureDescription:
    # The type checkers cannot see that the `@overload` above ensure that this call is valid.
    return agg(operand, plugin_key="MEAN", scope=scope)  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]
