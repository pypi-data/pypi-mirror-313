from __future__ import annotations

from dataclasses import dataclass
from typing import final

from typing_extensions import override

from .._constant import Constant
from .._identification import MeasureIdentifier
from .._java_api import JavaApi
from .._measure_description import MeasureDescription
from .._py4j_utils import to_java_object


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class ConstantMeasure(MeasureDescription):
    """A measure equal to a constant."""

    _value: Constant

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        cube_name: str,
        java_api: JavaApi,
    ) -> MeasureIdentifier:
        value = to_java_object(self._value.value, gateway=java_api.gateway)
        return java_api.create_measure(
            identifier,
            "CONSTANT",
            value,
            cube_name=cube_name,
        )
