from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from functools import cache, cached_property
from threading import Lock
from typing import Final, final

from typing_extensions import override

from .._column_convertible import ColumnCondition, ColumnOperation as _ColumnOperation
from .._constant import Constant
from .._data_type import DataType
from .._function_operation import FunctionOperation
from .._identification import ColumnIdentifier, MeasureIdentifier
from .._java_api import JavaApi
from .._measure_description import MeasureDescription
from .._operation import (
    ArithmeticOperation,
    Condition,
    Operand,
    Operation as _Operation,
    decombine_condition,
)
from .._udaf_operation import (
    AdditionOperation,
    ColumnOperation,
    ConstantOperation,
    DivisionOperation,
    EqualOperation,
    GreaterThanOperation,
    GreaterThanOrEqualOperation,
    JavaFunctionOperation,
    LowerThanOperation,
    LowerThanOrEqualOperation,
    MultiplicationOperation,
    NotEqualOperation,
    Operation,
    SubtractionOperation,
    TernaryOperation,
)
from .._udaf_utils import (
    ARRAY_MEAN,
    ARRAY_SUM,
    LongAggregationOperationVisitor,
    MaxAggregationOperationVisitor,
    MeanAggregationOperationVisitor,
    MinAggregationOperationVisitor,
    MultiplyAggregationOperationVisitor,
    ShortAggregationOperationVisitor,
    SingleValueNullableAggregationOperationVisitor,
    SquareSumAggregationOperationVisitor,
    SumAggregationOperationVisitor,
)
from .._udaf_utils.java_operation_visitor import OperationVisitor
from .._where_operation import WhereOperation

OPERATION_VISITORS = {
    "SUM": SumAggregationOperationVisitor,
    "MEAN": MeanAggregationOperationVisitor,
    "MULTIPLY": MultiplyAggregationOperationVisitor,
    "MIN": MinAggregationOperationVisitor,
    "MAX": MaxAggregationOperationVisitor,
    "SQ_SUM": SquareSumAggregationOperationVisitor,
    "SHORT": ShortAggregationOperationVisitor,
    "LONG": LongAggregationOperationVisitor,
    "SINGLE_VALUE_NULLABLE": SingleValueNullableAggregationOperationVisitor,
}


@final
class _AtomicCounter:
    """Threadsafe counter to get unique IDs."""

    def __init__(self) -> None:
        self._value = 0
        self._lock: Final = Lock()

    def read_and_increment(self) -> int:
        with self._lock:
            self._value += 1
            return self._value


@cache
def _get_id_provider() -> _AtomicCounter:
    return _AtomicCounter()


@final
@dataclass(frozen=True, kw_only=True)
class _UserDefinedAggregateFunction:
    """A class template which builds the sources to compile an AUserDefinedAggregate function at runtime.

    This class parses the combination of operations passed and converts them into Java source code blocks.
    These source code blocks are then compiled using Javassist into a new aggregation function which is then registered on the session.
    """

    _operation: Operation
    _plugin_key: str

    @property
    def _columns(self) -> Sequence[ColumnIdentifier]:
        return self._operation.columns

    @cached_property
    def plugin_key(self) -> str:
        column_names = "".join([column.column_name for column in self._columns])
        return f"{column_names}{_get_id_provider().read_and_increment()}.{self._plugin_key}"

    def register_aggregation_function(self, *, java_api: JavaApi) -> None:
        """Generate the required Java source code blocks and pass them to the Java process to be compiled into a new UserDefinedAggregateFunction."""
        visitor_class = OPERATION_VISITORS[self._plugin_key]
        visitor: OperationVisitor = visitor_class(  # type: ignore[abstract]
            columns=self._columns,
            java_api=java_api,
        )

        java_operation = visitor.build_java_operation(self._operation)
        java_api.register_aggregation_function(
            additional_imports=java_operation.additional_imports,
            additional_methods=java_operation.additional_methods_source_codes,
            contribute_source_code=java_operation.contribute_source_code,
            decontribute_source_code=java_operation.decontribute_source_code,
            merge_source_code=java_operation.merge_source_code,
            terminate_source_code=java_operation.terminate_source_code,
            buffer_types=java_operation.buffer_types,
            output_type=java_operation.output_type,
            plugin_key=self.plugin_key,
        )


def _operand_to_udaf_operation(  # noqa: C901, PLR0911, PLR0912
    operand: Operand[ColumnIdentifier] | Operation | None,
    /,
    *,
    get_column_data_type: Callable[[ColumnIdentifier], DataType],
) -> Operation:
    if isinstance(operand, Operation):
        return operand

    if isinstance(operand, Constant):
        return ConstantOperation(operand)

    if isinstance(operand, ColumnIdentifier):
        return ColumnOperation(operand, get_column_data_type(operand))

    if isinstance(operand, Condition):
        # Mypy is flaky here, try removing `unused-ignore` when upgrading it.
        decombined_conditions = decombine_condition(  # type: ignore[var-annotated,type-var,unused-ignore]
            operand,
            allowed_subject_types=(ColumnIdentifier,),
            allowed_target_types=(type(None), Constant, ColumnIdentifier, _Operation),
            allowed_isin_element_types=(),
            allowed_combination_operators=(),
        )
        condition = decombined_conditions[0][0][0]
        operator = condition.operator
        left_operand, right_operand = (
            _operand_to_udaf_operation(
                # Mypy is flaky here, try removing `unused-ignore` when upgrading it.
                sub_operand,  # type: ignore[arg-type,unused-ignore]
                get_column_data_type=get_column_data_type,
            )
            for sub_operand in (condition.subject, condition.target)
        )

        if operator == "eq":
            return EqualOperation(left_operand, right_operand)
        if operator == "ge":
            return GreaterThanOrEqualOperation(left_operand, right_operand)
        if operator == "gt":
            return GreaterThanOperation(left_operand, right_operand)
        if operator == "le":
            return LowerThanOrEqualOperation(left_operand, right_operand)
        if operator == "lt":
            return LowerThanOperation(left_operand, right_operand)
        if operator == "ne":
            return NotEqualOperation(left_operand, right_operand)

    if isinstance(operand, ArithmeticOperation):
        operator = operand.operator
        left_operand, right_operand = (
            _operand_to_udaf_operation(
                sub_operand,
                get_column_data_type=get_column_data_type,
            )
            for sub_operand in operand.operands
        )

        if operator == "add":
            return AdditionOperation(left_operand, right_operand)
        if operator == "mul":
            return MultiplicationOperation(left_operand, right_operand)
        if operator == "sub":
            return SubtractionOperation(left_operand, right_operand)
        if operator == "truediv":
            return DivisionOperation(left_operand, right_operand)
        raise AssertionError(f"Unexpected arithmetic operator: `{operator}`.")

    if isinstance(operand, FunctionOperation):
        function_key = operand.function_key
        if function_key == "array_mean":
            return ARRAY_MEAN(operand.operands[0])
        if function_key == "array_sum":
            return ARRAY_SUM(operand.operands[0])
        raise AssertionError(f"Unexpected function key: `{function_key}`.")

    if isinstance(operand, WhereOperation):
        return TernaryOperation(
            condition=_operand_to_udaf_operation(
                operand.condition,
                get_column_data_type=get_column_data_type,
            ),
            true_operation=_operand_to_udaf_operation(
                operand.true_value,
                get_column_data_type=get_column_data_type,
            ),
            false_operation=None
            if operand.false_value is None
            else _operand_to_udaf_operation(
                operand.false_value,
                get_column_data_type=get_column_data_type,
            ),
        )

    raise AssertionError(f"Unexpected operand type: `{type(operand).__name__}`.")


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class UdafMeasure(MeasureDescription):
    _plugin_key: str
    _operation: ColumnCondition | _ColumnOperation | JavaFunctionOperation

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        cube_name: str,
        java_api: JavaApi,
    ) -> MeasureIdentifier:
        udaf_operation = _operand_to_udaf_operation(
            self._operation,
            get_column_data_type=lambda identifier: java_api.get_column_data_type(
                identifier,
            ),
        )
        udaf = _UserDefinedAggregateFunction(
            _operation=udaf_operation,
            _plugin_key=self._plugin_key,
        )
        udaf.register_aggregation_function(java_api=java_api)
        return java_api.create_measure(
            identifier,
            "ATOTI_UDAF_MEASURE",
            udaf._columns,
            udaf.plugin_key,
            self._plugin_key,
            cube_name=cube_name,
        )
