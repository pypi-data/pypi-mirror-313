from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from .._identification import HierarchyIdentifier, MeasureIdentifier
from .._java_api import JavaApi
from .._measure.utils import get_measure_name
from .._measure_convertible import MeasureConvertible
from .._measure_description import MeasureDescription


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class ParentValue(MeasureDescription):
    """The value of the measure for the parent."""

    _underlying_measure: MeasureDescription | str
    _degrees: Mapping[HierarchyIdentifier, int]
    _total_value: MeasureConvertible | None
    _apply_filters: bool
    _dense: bool

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        cube_name: str,
        java_api: JavaApi,
    ) -> MeasureIdentifier:
        underlying_name = (
            self._underlying_measure
            if isinstance(self._underlying_measure, str)
            else get_measure_name(
                java_api=java_api,
                measure=self._underlying_measure,
                cube_name=cube_name,
            )
        )
        total_measure_name: str | None = (
            self._total_value._distil(
                java_api=java_api,
                cube_name=cube_name,
            ).measure_name
            if isinstance(self._total_value, MeasureDescription)
            else None
        )
        total_literal = self._total_value if total_measure_name is None else None

        return java_api.create_measure(
            identifier,
            "PARENT_VALUE",
            underlying_name,
            {
                identifier._java_description: degree
                for identifier, degree in self._degrees.items()
            },
            total_measure_name,
            total_literal,
            self._apply_filters,
            self._dense,
            cube_name=cube_name,
        )
