from typing import Literal, cast

from .._typing import get_literal_args

BooleanOperator = Literal["and", "or"]

BOOLEAN_OPERATORS = cast(
    tuple[BooleanOperator, ...],
    get_literal_args(BooleanOperator),
)
