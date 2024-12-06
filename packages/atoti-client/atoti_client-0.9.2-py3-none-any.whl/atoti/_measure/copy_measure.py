from collections.abc import Collection, Mapping, Set as AbstractSet
from dataclasses import dataclass
from typing import Annotated, Any, final

from pydantic import Field
from typing_extensions import override

from .._constant import ConstantValue
from .._identification import (
    ColumnIdentifier,
    HierarchyIdentifier,
    MeasureIdentifier,
)
from .._java_api import JavaApi
from .._measure.utils import get_measure_name
from .._measure_description import MeasureDescription
from .._py4j_utils import (
    to_java_list,
    to_java_map,
    to_java_object_array,
    to_java_string_array,
)


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class CopyMeasure(MeasureDescription):
    _underlying_measure: MeasureDescription | str
    _source: Mapping[HierarchyIdentifier, Collection[Any]]
    _target: Mapping[HierarchyIdentifier, Collection[list[Any]]]

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        java_api: JavaApi,
        cube_name: str,
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
        return java_api.create_measure(
            identifier,
            "COPY_MEASURE",
            underlying_name,
            to_java_map(
                {
                    identifier._java_description: to_java_object_array(
                        location,
                        gateway=java_api.gateway,
                    )
                    for identifier, location in self._source.items()
                },
                gateway=java_api.gateway,
            ),
            to_java_map(
                {
                    identifier._java_description: to_java_list(
                        [
                            to_java_string_array(location, gateway=java_api.gateway)
                            for location in locations
                        ],
                        gateway=java_api.gateway,
                    )
                    for identifier, locations in self._target.items()
                },
                gateway=java_api.gateway,
            ),
            cube_name=cube_name,
        )


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class FullCopyMeasure(MeasureDescription):
    _underlying_measure: MeasureDescription | str
    _hierarchy: HierarchyIdentifier
    _hierarchy_columns: tuple[ColumnIdentifier, ...]
    _member_paths: Mapping[
        tuple[ConstantValue, ...],
        AbstractSet[tuple[ConstantValue, ...]],
    ]
    _consolidation_factors: Annotated[tuple[ColumnIdentifier, ...], Field(min_length=1)]

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        java_api: JavaApi,
        cube_name: str,
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
        java_mapping = to_java_list(
            [
                java_api.gateway.jvm.com.activeviam.tech.core.api.util.Pair(  # pyright: ignore[reportAttributeAccessIssue,reportCallIssue, reportOptionalCall, reportOptionalMemberAccess]
                    to_java_object_array(source_member_path, gateway=java_api.gateway),  # pyright: ignore[reportCallIssue]
                    to_java_list(
                        [
                            to_java_object_array(
                                target_member_path,
                                gateway=java_api.gateway,
                            )
                            for target_member_path in target_member_paths
                        ],
                        gateway=java_api.gateway,
                    ),
                )
                for source_member_path, target_member_paths in self._member_paths.items()
            ],
            gateway=java_api.gateway,
        )

        if not self._consolidation_factors:
            raise ValueError("Consolidation factors must be provided")

        return java_api.create_measure(
            identifier,
            "CONSOLIDATED_COPY_MEASURE",
            underlying_name,
            self._hierarchy._java_description,
            java_mapping,
            self._consolidation_factors[0].table_identifier.table_name,
            to_java_list(
                [column.column_name for column in self._hierarchy_columns],
                gateway=java_api.gateway,
            ),
            to_java_list(
                [column.column_name for column in self._consolidation_factors],
                gateway=java_api.gateway,
            ),
            cube_name=cube_name,
        )
