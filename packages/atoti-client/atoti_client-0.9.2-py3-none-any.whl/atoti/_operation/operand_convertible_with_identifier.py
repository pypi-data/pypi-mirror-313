from __future__ import annotations

from abc import ABC
from typing import Literal, final, overload

from typing_extensions import override

from .._constant import Constant, ConstantValue
from .._identification import HasIdentifier, IdentifierT_co
from ._other_identifier import OtherIdentifierT_co
from .operation import (
    ComparisonCondition,
    Condition,
    OperandConvertible,
    Operation,
    convert_to_operand,
)


class OperandConvertibleWithIdentifier(
    OperandConvertible[IdentifierT_co],
    HasIdentifier[IdentifierT_co],
    ABC,
):
    """This class overrides `OperandConvertible`'s `Condition`-creating methods so that the type of the returned `Condition`'s `subject` is narrowed down to an instance of `Identifier` instead of `Identifier | Operation`.

    The returned `Condition`'s `target` is also kept as narrow as possible thanks to `@overload`s.
    """

    @override
    # Without this, the classes inheriting from this class are considered unhashable.
    def __hash__(self) -> int:
        return super().__hash__()

    @override
    def isnull(
        self,
    ) -> Condition[IdentifierT_co, Literal["eq"], None, None]:
        return ComparisonCondition(self._operation_operand, "eq", None)

    @property
    @override
    def _operation_operand(self) -> IdentifierT_co:
        return self._identifier

    # The signature is not compatible with `object.__eq__()` on purpose.
    @overload  # type: ignore[override]
    def __eq__(
        self,
        other: ConstantValue,
        /,
    ) -> Condition[IdentifierT_co, Literal["eq"], Constant, None]: ...

    @overload
    def __eq__(
        self,
        other: HasIdentifier[OtherIdentifierT_co],
        /,
    ) -> Condition[IdentifierT_co, Literal["eq"], OtherIdentifierT_co, None]: ...

    @overload
    def __eq__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        IdentifierT_co,
        Literal["eq"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]: ...

    @final
    @override
    # The signature is not compatible with `object.__eq__()` on purpose.
    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        IdentifierT_co,
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

    @overload
    def __ge__(
        self,
        other: ConstantValue,
        /,
    ) -> Condition[IdentifierT_co, Literal["ge"], Constant, None]: ...

    @overload
    def __ge__(
        self,
        other: HasIdentifier[OtherIdentifierT_co],
        /,
    ) -> Condition[IdentifierT_co, Literal["ge"], OtherIdentifierT_co, None]: ...

    @overload
    def __ge__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        IdentifierT_co,
        Literal["ge"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]: ...

    @override
    def __ge__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        IdentifierT_co,
        Literal["ge"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]:
        return ComparisonCondition(
            self._operation_operand,
            "ge",
            convert_to_operand(other),
        )

    @overload
    def __gt__(
        self,
        other: ConstantValue,
        /,
    ) -> Condition[IdentifierT_co, Literal["gt"], Constant, None]: ...

    @overload
    def __gt__(
        self,
        other: HasIdentifier[OtherIdentifierT_co],
        /,
    ) -> Condition[IdentifierT_co, Literal["gt"], OtherIdentifierT_co, None]: ...

    @overload
    def __gt__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        IdentifierT_co,
        Literal["gt"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]: ...

    @final
    @override
    def __gt__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        IdentifierT_co,
        Literal["gt"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]:
        return ComparisonCondition(
            self._operation_operand,
            "gt",
            convert_to_operand(other),
        )

    @overload
    def __le__(
        self,
        other: ConstantValue,
        /,
    ) -> Condition[IdentifierT_co, Literal["le"], Constant, None]: ...

    @overload
    def __le__(
        self,
        other: HasIdentifier[OtherIdentifierT_co],
        /,
    ) -> Condition[IdentifierT_co, Literal["le"], OtherIdentifierT_co, None]: ...

    @overload
    def __le__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        IdentifierT_co,
        Literal["le"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]: ...

    @final
    @override
    def __le__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        IdentifierT_co,
        Literal["le"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]:
        return ComparisonCondition(
            self._operation_operand,
            "le",
            convert_to_operand(other),
        )

    @overload
    def __lt__(
        self,
        other: ConstantValue,
        /,
    ) -> Condition[IdentifierT_co, Literal["lt"], Constant, None]: ...

    @overload
    def __lt__(
        self,
        other: HasIdentifier[OtherIdentifierT_co],
        /,
    ) -> Condition[IdentifierT_co, Literal["lt"], OtherIdentifierT_co, None]: ...

    @overload
    def __lt__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        IdentifierT_co,
        Literal["lt"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]: ...

    @final
    @override
    def __lt__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        IdentifierT_co,
        Literal["lt"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]:
        return ComparisonCondition(
            self._operation_operand,
            "lt",
            convert_to_operand(other),
        )

    # The signature is not compatible with `object.__ne__()` on purpose.
    @overload  # type: ignore[override]
    def __ne__(
        self,
        other: ConstantValue,
        /,
    ) -> Condition[IdentifierT_co, Literal["ne"], Constant, None]: ...

    @overload
    def __ne__(
        self,
        other: HasIdentifier[OtherIdentifierT_co],
        /,
    ) -> Condition[IdentifierT_co, Literal["ne"], OtherIdentifierT_co, None]: ...

    @overload
    def __ne__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        IdentifierT_co,
        Literal["ne"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
        None,
    ]: ...

    @final
    @override
    # The signature is not compatible with `object.__ne__()` on purpose.
    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Condition[
        IdentifierT_co,
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
