from dataclasses import KW_ONLY, dataclass
from typing import final

from typing_extensions import override

from .._identification import HierarchyIdentifier, MeasureIdentifier
from .._java_api import JavaApi
from .._measure_description import MeasureDescription


@final
@dataclass(eq=False, frozen=True)
class HierarchyMeasure(MeasureDescription):
    _hierarchy_identifier: HierarchyIdentifier
    _: KW_ONLY

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
            "HIERARCHY",
            self._hierarchy_identifier._java_description,
            cube_name=cube_name,
        )
