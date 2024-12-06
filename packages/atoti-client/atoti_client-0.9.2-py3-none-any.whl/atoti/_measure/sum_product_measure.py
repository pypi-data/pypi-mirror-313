from collections.abc import Sequence
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from .._data_type import is_array_type
from .._identification import MeasureIdentifier
from .._java_api import JavaApi
from .._measure_convertible import MeasureConvertible
from .._measure_description import MeasureDescription, convert_to_measure_description
from ..column import Column
from ..type import DOUBLE_ARRAY
from .utils import convert_measure_args


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class SumProductFieldsMeasure(MeasureDescription):
    """Sum of the product of factors for table fields."""

    _factors: Sequence[Column]

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        cube_name: str,
        java_api: JavaApi,
    ) -> MeasureIdentifier:
        # Checks fields are in the selection, otherwise use the other sum product implementation because UDAF needs fields in the selection.
        selection_fields = java_api.get_selection_fields(cube_name)
        if not all(factor._identifier in selection_fields for factor in self._factors):
            raise ValueError(
                f"The columns {[factor.name for factor in self._factors if factor._identifier not in selection_fields]}"
                f" cannot be used in a sum product aggregation without first being converted into measures.",
            )
        factors_and_type = {}
        for factor in self._factors:
            if is_array_type(factor.data_type) and factor.data_type != DOUBLE_ARRAY:
                raise TypeError(
                    f"Only array columns of type `{DOUBLE_ARRAY}` are supported and `{factor._identifier!r}` is not.",
                )
            factors_and_type[factor._identifier] = factor.data_type
        return java_api.create_measure(
            identifier,
            "SUM_PRODUCT_UDAF",
            [factor._identifier for factor in self._factors],
            factors_and_type,
            cube_name=cube_name,
        )


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class SumProductEncapsulationMeasure(MeasureDescription):
    """Create an intermediate measure needing to be aggregated with the key "ATOTI_SUM_PRODUCT"."""

    _factors: Sequence[MeasureConvertible]

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        cube_name: str,
        java_api: JavaApi,
    ) -> MeasureIdentifier:
        return java_api.create_measure(
            identifier,
            "SUM_PRODUCT_ENCAPSULATION",
            convert_measure_args(
                java_api=java_api,
                cube_name=cube_name,
                args=tuple(
                    convert_to_measure_description(factor) for factor in self._factors
                ),
            ),
            cube_name=cube_name,
        )
