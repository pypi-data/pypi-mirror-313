from __future__ import annotations

import math
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from dataclasses import KW_ONLY, dataclass as _dataclass
from itertools import chain
from typing import (
    Annotated,
    Generic,
    Literal,
    NoReturn,
    TypeAlias,
    TypeVar,
    final,
    overload,
)

from pydantic import AfterValidator
from pydantic.dataclasses import dataclass
from typing_extensions import override

from .._collections import FrozenSequence
from .._constant import Constant, ConstantValue
from .._identification import (
    HasIdentifier,
    HierarchyIdentifier,
    Identifier,
    IdentifierT_co,
)
from .._pydantic import PYDANTIC_CONFIG
from ._arithmetic_operator import ArithmeticOperator
from ._boolean_operator import BooleanOperator
from ._other_identifier import OtherIdentifierT_co
from .comparison_operator import OPERATOR_TO_INVERSE_OPERATOR, ComparisonOperator


@overload
def convert_to_operand(value: None, /) -> None: ...


@overload
def convert_to_operand(value: ConstantValue, /) -> Constant: ...


@overload
def convert_to_operand(value: HasIdentifier[IdentifierT_co], /) -> IdentifierT_co: ...


@overload
def convert_to_operand(
    value: OperandCondition[IdentifierT_co],
    /,
) -> OperandCondition[IdentifierT_co]: ...


@overload
def convert_to_operand(
    value: Operation[IdentifierT_co],
    /,
) -> Operation[IdentifierT_co]: ...


def convert_to_operand(
    value: OperandCondition[IdentifierT_co]
    | ConstantValue
    | HasIdentifier[IdentifierT_co]
    | Operation[IdentifierT_co]
    | None,
    /,
) -> Operand[IdentifierT_co] | None:
    if value is None or isinstance(value, Condition | Operation):
        return value
    if isinstance(value, HasIdentifier):
        return value._identifier
    return Constant.of(value)


class OperandConvertible(Generic[IdentifierT_co], ABC):
    @property
    @abstractmethod
    def _operation_operand(self) -> _UnconditionalVariableOperand[IdentifierT_co]: ...

    def isnull(
        self,
    ) -> Condition[
        _UnconditionalVariableOperand[IdentifierT_co],
        Literal["eq"],
        None,
        None,
    ]:
        """Return a condition evaluating to ``True`` when the element evaluates to ``None`` and ``False`` otherwise.

        Use `~obj.isnull()` for the opposite behavior.
        """
        return ComparisonCondition(self._operation_operand, "eq", None)

    @final
    def __bool__(self) -> NoReturn:
        raise AssertionError(
            f"Instances of `{type(self).__name__}` cannot be cast to a boolean. Use a comparison operator to create a `{Condition.__name__}` instead.",
        )

    @override
    def __hash__(self) -> int:
        # The public API sometimes requires instances of this class to be used as mapping keys so they must be hashable.
        # However, these keys are only ever iterated upon (i.e. there is no get by key access) so the hash is not important.
        # The ID of the object is thus used, like `object.__hash__()` would do.
        return id(self)

    @final
    def __iter__(self) -> NoReturn:
        # Implementing this method and making it raise an error is required to avoid an endless loop when validating incorrect `AbstractSet`s with Pydantic.
        # For instance, without this, `tt.OriginScope(some_level)` never returns (`tt.OriginScope({some_level})` is the right code).
        # Making this method raise an error prevents Pydantic from calling `__getitem__()` which returns a new `IndexingOperation` instead of an attribute value.
        raise TypeError(f"Instances of {self.__class__.__name__} are not iterable.")

    @final
    def __getitem__(
        self,
        index: HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co]
        | slice
        | int
        | Sequence[int],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return IndexingOperation(
            self._operation_operand,
            index._identifier if isinstance(index, HasIdentifier) else index,
        )

    @override
    # The signature is not compatible with `object.__eq__()` on purpose.
    def __eq__(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        _UnconditionalVariableOperand[IdentifierT_co],
        Literal["eq"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]:
        assert other is not None, "Use `isnull()` instead."
        return ComparisonCondition(
            self._operation_operand,
            "eq",
            convert_to_operand(other),
        )

    def __ge__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        _UnconditionalVariableOperand[IdentifierT_co],
        Literal["ge"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]:
        return ComparisonCondition(
            self._operation_operand,
            "ge",
            convert_to_operand(other),
        )

    def __gt__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        _UnconditionalVariableOperand[IdentifierT_co],
        Literal["gt"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]:
        return ComparisonCondition(
            self._operation_operand,
            "gt",
            convert_to_operand(other),
        )

    def __le__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        _UnconditionalVariableOperand[IdentifierT_co],
        Literal["le"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]:
        return ComparisonCondition(
            self._operation_operand,
            "le",
            convert_to_operand(other),
        )

    def __lt__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        _UnconditionalVariableOperand[IdentifierT_co],
        Literal["lt"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]:
        return ComparisonCondition(
            self._operation_operand,
            "lt",
            convert_to_operand(other),
        )

    @override
    # The signature is not compatible with `object.__ne__()` on purpose.
    def __ne__(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        _UnconditionalVariableOperand[IdentifierT_co],
        Literal["ne"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]:
        assert other is not None, "Use `~isnull()` instead."
        return ComparisonCondition(
            self._operation_operand,
            "ne",
            convert_to_operand(other),
        )

    @final
    def __add__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (self._operation_operand, convert_to_operand(other)),
            "add",
        )

    @final
    def __radd__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (convert_to_operand(other), self._operation_operand),
            "add",
        )

    @final
    def __floordiv__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (self._operation_operand, convert_to_operand(other)),
            "floordiv",
        )

    @final
    def __rfloordiv__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (convert_to_operand(other), self._operation_operand),
            "floordiv",
        )

    @final
    def __mod__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (self._operation_operand, convert_to_operand(other)),
            "mod",
        )

    @final
    def __rmod__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (convert_to_operand(other), self._operation_operand),
            "mod",
        )

    @final
    def __mul__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (self._operation_operand, convert_to_operand(other)),
            "mul",
        )

    @final
    def __rmul__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (convert_to_operand(other), self._operation_operand),
            "mul",
        )

    @final
    def __neg__(
        self,
    ) -> Operation[IdentifierT_co]:
        return ArithmeticOperation((self._operation_operand,), "neg")

    @final
    def __pow__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (self._operation_operand, convert_to_operand(other)),
            "pow",
        )

    @final
    def __rpow__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (convert_to_operand(other), self._operation_operand),
            "pow",
        )

    @final
    def __sub__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (self._operation_operand, convert_to_operand(other)),
            "sub",
        )

    @final
    def __rsub__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (convert_to_operand(other), self._operation_operand),
            "sub",
        )

    @final
    def __truediv__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (self._operation_operand, convert_to_operand(other)),
            "truediv",
        )

    @final
    def __rtruediv__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (convert_to_operand(other), self._operation_operand),
            "truediv",
        )


OperandConvertibleBound = OperandConvertible[Identifier]


class _BaseOperation(ABC):
    """An operation is made out of one or more operands and possibly some other primitive attributes such as strings or numbers.

    To ensure that operations are immutable and serializable, operands must never be of type `ConstantValue` or `HasIdentifier`.
    These must be converted to `Constant` and `Identifier` instead.

    This base class' sole purpose is to provide a shared fundation for `Condition` and `Operation`.
    All classes inheriting from `_BaseOperation` must inherit from one of these two classes.
    As such, this class must remain private and not referenced outside this file.
    """

    @property
    @abstractmethod
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        """The set of types of the identifiers used in this operation.

        This is used, for instance, to detect whether an operation is purely column-based and could thus be the input of a UDAF.
        """

    @classmethod
    def _get_identifier_types(
        cls,
        operand: Operand[Identifier] | None,
        /,
    ) -> frozenset[type[Identifier]]:
        if operand is None or isinstance(operand, Constant):
            return frozenset()
        if isinstance(operand, Identifier):
            return frozenset([type(operand)])
        return operand._identifier_types


class Operation(OperandConvertible[IdentifierT_co], _BaseOperation, ABC):
    @property
    @override
    def _operation_operand(self) -> Operation[IdentifierT_co]:
        return self


OperationBound = Operation[Identifier]

# The following classes can be constructed from any `OperandConvertible` using Python's built-in operators.
# Because overriding these operators requires to implement methods on `OperandConvertible` instantiating the classes below, they all have to be declared in the same file to avoid circular imports.


ConditionSubjectBound = Identifier | OperationBound
ConditionSubjectT_co = TypeVar(
    "ConditionSubjectT_co",
    bound=ConditionSubjectBound,
    covariant=True,
)

ConditionComparisonOperatorBound = Literal[ComparisonOperator, "isin"]
ConditionComparisonOperatorT_co = TypeVar(
    "ConditionComparisonOperatorT_co",
    bound=ConditionComparisonOperatorBound,
    covariant=True,
)

ConditionTargetBound = Constant | Identifier | OperationBound | None
ConditionTargetT_co = TypeVar(
    "ConditionTargetT_co",
    bound=ConditionTargetBound,
    covariant=True,
)

ConditionCombinationOperatorBound = BooleanOperator | None
ConditionCombinationOperatorT_co = TypeVar(
    "ConditionCombinationOperatorT_co",
    bound=ConditionCombinationOperatorBound,
    covariant=True,
)

_OtherConditionSubjectT_co = TypeVar(
    "_OtherConditionSubjectT_co",
    bound=ConditionSubjectBound,
    covariant=True,
)
_OtherConditionComparisonOperatorT_co = TypeVar(
    "_OtherConditionComparisonOperatorT_co",
    bound=ConditionComparisonOperatorBound,
    covariant=True,
)
_OtherConditionTargetT_co = TypeVar(
    "_OtherConditionTargetT_co",
    bound=ConditionTargetBound,
    covariant=True,
)
_OtherConditionCombinationOperatorT_co = TypeVar(
    "_OtherConditionCombinationOperatorT_co",
    bound=ConditionCombinationOperatorBound,
    covariant=True,
)


class Condition(
    Generic[
        ConditionSubjectT_co,
        ConditionComparisonOperatorT_co,
        ConditionTargetT_co,
        ConditionCombinationOperatorT_co,
    ],
    _BaseOperation,
):
    @final
    def __and__(
        self,
        other: Condition[
            _OtherConditionSubjectT_co,
            _OtherConditionComparisonOperatorT_co,
            _OtherConditionTargetT_co,
            _OtherConditionCombinationOperatorT_co,
        ],
        /,
    ) -> CombinedCondition[
        ConditionSubjectT_co | _OtherConditionSubjectT_co,
        ConditionComparisonOperatorT_co | _OtherConditionComparisonOperatorT_co,
        ConditionTargetT_co | _OtherConditionTargetT_co,
        Literal["and"]
        | ConditionCombinationOperatorT_co
        | _OtherConditionCombinationOperatorT_co,
    ]:
        return CombinedCondition((self, other), "and")

    @final
    def __bool__(self) -> NoReturn:
        raise AssertionError(
            "Conditions cannot be cast to a boolean as they are only evaluated during query execution. To combine conditions, use the bitwise `&`, `|`, or `~` operators.",
        )

    @abstractmethod
    def __invert__(
        self,
    ) -> Condition[
        ConditionSubjectT_co,
        ConditionComparisonOperatorBound,
        ConditionTargetT_co,
        ConditionCombinationOperatorBound,
    ]: ...

    def __or__(
        self,
        other: Condition[
            _OtherConditionSubjectT_co,
            _OtherConditionComparisonOperatorT_co,
            _OtherConditionTargetT_co,
            _OtherConditionCombinationOperatorT_co,
        ],
        /,
    ) -> CombinedCondition[
        ConditionSubjectT_co | _OtherConditionSubjectT_co,
        ConditionComparisonOperatorT_co | _OtherConditionComparisonOperatorT_co,
        ConditionTargetT_co | _OtherConditionTargetT_co,
        Literal["or"]
        | ConditionCombinationOperatorT_co
        | _OtherConditionCombinationOperatorT_co,
    ]:
        return CombinedCondition((self, other), "or")

    def __xor__(
        self,
        other: Condition[
            _OtherConditionSubjectT_co,
            _OtherConditionComparisonOperatorT_co,
            _OtherConditionTargetT_co,
            _OtherConditionCombinationOperatorT_co,
        ],
        /,
    ) -> NoReturn:
        raise AssertionError("Conditions cannot be `xor`ed.")

    @abstractmethod
    @override
    def __repr__(self) -> str: ...


ConditionBound = Condition[
    ConditionSubjectBound,
    ConditionComparisonOperatorBound,
    ConditionTargetBound,
    ConditionCombinationOperatorBound,
]


def _validate_combined_condition_operator(
    operator: ConditionCombinationOperatorBound,
    /,
) -> BooleanOperator:
    assert operator is not None, "Missing combination operator."
    return operator


@final
@dataclass(config=PYDANTIC_CONFIG, frozen=True)
class CombinedCondition(
    Condition[
        ConditionSubjectT_co,
        ConditionComparisonOperatorT_co,
        ConditionTargetT_co,
        ConditionCombinationOperatorT_co,
    ],
):
    sub_conditions: tuple[
        Condition[
            ConditionSubjectT_co,
            ConditionComparisonOperatorT_co,
            ConditionTargetT_co,
            ConditionCombinationOperatorT_co,
        ],
        Condition[
            ConditionSubjectT_co,
            ConditionComparisonOperatorT_co,
            ConditionTargetT_co,
            ConditionCombinationOperatorT_co,
        ],
    ]
    operator: Annotated[
        ConditionCombinationOperatorT_co,
        AfterValidator(_validate_combined_condition_operator),
    ]
    _: KW_ONLY

    @property
    def boolean_operator(self) -> BooleanOperator:
        operator: BooleanOperator | None = self.operator
        assert operator is not None
        return operator

    @override
    def __invert__(
        self,
    ) -> Condition[
        ConditionSubjectT_co,
        ConditionComparisonOperatorBound,
        ConditionTargetT_co,
        ConditionCombinationOperatorBound,
    ]:
        return CombinedCondition(
            (~self.sub_conditions[0], ~self.sub_conditions[1]),
            "or" if self.operator == "and" else "and",
        )

    @property
    @override
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        return frozenset(
            chain(
                *(
                    sub_condition._identifier_types
                    for sub_condition in self.sub_conditions
                ),
            ),
        )

    @override
    def __repr__(self) -> str:
        return f"({self.sub_conditions[0]!r}) {'&' if self.operator == 'and' else '|'} ({self.sub_conditions[1]!r})"


_ComparisonOperatorT_co = TypeVar(
    "_ComparisonOperatorT_co",
    bound=ComparisonOperator,
    covariant=True,
)

_COMPARISON_OPERATOR_TO_SYMBOL: Mapping[ComparisonOperator, str] = {
    "eq": "==",
    "ge": ">=",
    "gt": ">",
    "le": "<=",
    "lt": "<",
    "ne": "!=",
}


def _validate_condition_subject(
    subject: ConditionSubjectBound,
    /,
) -> ConditionSubjectBound:
    assert not isinstance(
        subject,
        HierarchyIdentifier,
    ), "Conditions on hierarchies must use `HierarchyIsinCondition`."
    return subject


def _validate_constant_target(target: Constant, /) -> Constant:
    if isinstance(target.value, float) and math.isnan(target.value):
        raise ValueError("Use the `isnan()` method to compare against NaN.")

    return target


def _validate_condition_target(
    target: ConditionTargetBound,
    /,
) -> ConditionTargetBound:
    return _validate_constant_target(target) if isinstance(target, Constant) else target


@final
@dataclass(config=PYDANTIC_CONFIG, frozen=True)
class ComparisonCondition(
    Condition[ConditionSubjectT_co, _ComparisonOperatorT_co, ConditionTargetT_co, None],
):
    subject: Annotated[
        ConditionSubjectT_co,
        AfterValidator(_validate_condition_subject),
    ]
    operator: _ComparisonOperatorT_co
    target: Annotated[ConditionTargetT_co, AfterValidator(_validate_condition_target)]
    _: KW_ONLY

    def __post_init__(self) -> None:
        assert self.target is not None or self.operator in {"eq", "ne"}

    @property
    @override
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        return frozenset(
            chain(
                *(
                    self._get_identifier_types(operand)
                    for operand in [self.subject, self.target]
                ),
            ),
        )

    @override
    def __invert__(
        self,
    ) -> Condition[ConditionSubjectT_co, ComparisonOperator, ConditionTargetT_co, None]:
        return ComparisonCondition(
            self.subject,
            OPERATOR_TO_INVERSE_OPERATOR[self.operator],
            self.target,
        )

    @override
    def __repr__(self) -> str:
        return f"{self.subject!r} {_COMPARISON_OPERATOR_TO_SYMBOL[self.operator]} {self.target.value if isinstance(self.target, Constant) else self.target!r}"


_ARITHMETIC_OPERATOR_TO_SYMBOL: Mapping[ArithmeticOperator, str] = {
    "add": "+",
    "floordiv": "//",
    "mod": "%",
    "mul": "*",
    "pow": "**",
    "sub": "-",
    "truediv": "/",
}


@final
@dataclass(config=PYDANTIC_CONFIG, eq=False, frozen=True)
class ArithmeticOperation(Operation[IdentifierT_co]):
    operands: FrozenSequence[_UnconditionalOperand[IdentifierT_co]]
    operator: ArithmeticOperator
    _: KW_ONLY

    @property
    @override
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        return frozenset(
            chain(*(self._get_identifier_types(operand) for operand in self.operands)),
        )

    @override
    def __repr__(self) -> str:
        if self.operator == "neg":
            return f"-{self._repr_operand(0)}"

        return f"{self._repr_operand(0)} {_ARITHMETIC_OPERATOR_TO_SYMBOL[self.operator]} {self._repr_operand(1)}"

    def _repr_operand(self, index: int, /) -> str:
        operand = self.operands[index]
        operand_representation = repr(operand)
        operation_is_function_call_result = not isinstance(
            operand,
            ArithmeticOperation | Condition | IndexingOperation,
        )
        return (
            operand_representation
            if operation_is_function_call_result
            else f"({operand_representation})"
        )


@final
@_dataclass(eq=False, frozen=True)
class IndexingOperation(Operation[IdentifierT_co]):
    operand: _UnconditionalVariableOperand[IdentifierT_co]
    index: (
        slice | int | FrozenSequence[int] | IdentifierT_co | Operation[IdentifierT_co]
    )
    _: KW_ONLY

    @property
    @override
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        return self._get_identifier_types(self.operand) | (
            frozenset()
            if isinstance(self.index, int | Sequence | slice)
            else self._get_identifier_types(self.index)
        )

    @override
    def __repr__(self) -> str:
        return f"{self.operand!r}[{self.index!r}]"


_UnconditionalVariableOperand: TypeAlias = IdentifierT_co | Operation[IdentifierT_co]
_UnconditionalOperand: TypeAlias = (
    Constant | _UnconditionalVariableOperand[IdentifierT_co]
)

OperandCondition: TypeAlias = Condition[
    _UnconditionalVariableOperand[IdentifierT_co],
    ConditionComparisonOperatorBound,
    _UnconditionalOperand[IdentifierT_co] | None,
    ConditionCombinationOperatorBound,
]

_VariableOperand: TypeAlias = (
    _UnconditionalVariableOperand[IdentifierT_co] | OperandCondition[IdentifierT_co]
)
Operand: TypeAlias = Constant | _VariableOperand[IdentifierT_co]
