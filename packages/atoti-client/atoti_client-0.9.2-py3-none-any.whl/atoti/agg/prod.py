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
def prod(operand: LevelOrVariableColumnConvertible, /) -> MeasureDescription: ...


@overload
def prod(
    operand: VariableMeasureConvertible,
    /,
    *,
    scope: Scope,
) -> MeasureDescription: ...


@doc(
    _BASIC_DOC,
    args=_BASIC_ARGS_DOC,
    value="product",
    example="""
        >>> m["Other.PROD"] = tt.agg.prod(table["Other"])
        >>> cube.query(m["Other.PROD"])
          Other.PROD
        0          4""".replace("\n", "", 1),
)
def prod(
    operand: LevelOrVariableColumnConvertible | VariableMeasureConvertible,
    /,
    *,
    scope: Scope | None = None,
) -> MeasureDescription:
    # The type checkers cannot see that the `@overload` above ensure that this call is valid.
    return agg(operand, plugin_key="MULTIPLY", scope=scope)  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]
