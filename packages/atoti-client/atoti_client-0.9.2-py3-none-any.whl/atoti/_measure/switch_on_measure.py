from collections.abc import Mapping
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from .._constant import ConstantValue
from .._identification import LevelIdentifier, MeasureIdentifier
from .._java_api import JavaApi
from .._measure_description import MeasureDescription
from .._py4j_utils import to_java_map, to_java_object


@final
@dataclass(repr=True, frozen=True, kw_only=True)
class SwitchOnMeasure(MeasureDescription):
    """A measure that switches between different measures based on the value of a level."""

    _subject: LevelIdentifier
    _cases: Mapping[
        ConstantValue,
        MeasureDescription,
    ]
    _default: MeasureDescription | None = None
    _above_level: MeasureDescription | None = None

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        java_api: JavaApi,
        cube_name: str,
    ) -> MeasureIdentifier:
        return java_api.create_measure(
            identifier,
            "SWITCH_ON",
            java_api.gateway.jvm.com.activeviam.activepivot.core.intf.api.cube.metadata.LevelIdentifier.fromDescription(  # pyright: ignore[reportCallIssue,reportAttributeAccessIssue,reportOptionalCall,reportOptionalMemberAccess] # spell-checker: disable-line
                self._subject._java_description,  # pyright: ignore[reportCallIssue]
            ),
            to_java_map(
                {
                    to_java_object(key, gateway=java_api.gateway): value._distil(
                        java_api=java_api,
                        cube_name=cube_name,
                    ).measure_name
                    for key, value in self._cases.items()
                },
                gateway=java_api.gateway,
            ),
            None
            if self._default is None
            else self._default._distil(
                java_api=java_api,
                cube_name=cube_name,
            ).measure_name,
            None
            if self._above_level is None
            else self._above_level._distil(
                java_api=java_api,
                cube_name=cube_name,
            ).measure_name,
            cube_name=cube_name,
        )
