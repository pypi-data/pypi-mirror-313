from __future__ import annotations

from typing import overload

from .._doc import doc
from .._docs_utils import (
    STD_AND_VAR_DOC as _STD_AND_VAR_DOC,
    VAR_DOC_KWARGS as _VAR_DOC_KWARGS,
)
from .._measure_convertible import VariableMeasureConvertible
from .._measure_description import MeasureDescription
from ..array.var import _Mode
from ..scope._scope import Scope
from ._count import count
from ._utils import (
    QUANTILE_STD_AND_VAR_DOC_KWARGS as _QUANTILE_STD_AND_VAR_DOC_KWARGS,
    SCOPE_DOC as _SCOPE_DOC,
    LevelOrVariableColumnConvertible,
)
from .mean import mean
from .square_sum import square_sum


@overload
def var(
    operand: LevelOrVariableColumnConvertible,
    /,
    *,
    mode: _Mode = ...,
) -> MeasureDescription: ...


@overload
def var(
    operand: VariableMeasureConvertible,
    /,
    *,
    mode: _Mode = ...,
    scope: Scope,
) -> MeasureDescription: ...


@doc(
    _STD_AND_VAR_DOC,
    _SCOPE_DOC,
    **_VAR_DOC_KWARGS,
    **_QUANTILE_STD_AND_VAR_DOC_KWARGS,
)
def var(
    operand: LevelOrVariableColumnConvertible | VariableMeasureConvertible,
    /,
    *,
    mode: _Mode = "sample",
    scope: Scope | None = None,
) -> MeasureDescription:
    # The type checkers cannot see that the `@overload` above ensure that these calls are valid.
    size = count(operand, scope=scope)  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]
    mean_value = mean(operand, scope=scope)  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]
    population_var = square_sum(operand, scope=scope) / size - mean_value * mean_value  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]
    if mode == "population":
        return population_var  # type: ignore[return-value] # pyright: ignore[reportReturnType]
    # Apply Bessel's correction
    return (
        population_var * size / (size - 1)  # type: ignore[return-value] # pyright: ignore[reportReturnType]
    )
