from __future__ import annotations

from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from .._collections import DelegatingMutableMapping
from .._constant import Constant
from .._identification import HierarchyIdentifier
from .._java_api import JavaApi
from .._operation import decombine_condition
from .masking_config import MaskingConfig


@final
class Masking(DelegatingMutableMapping[str, MaskingConfig]):
    def __init__(self, /, *, cube_name: str, java_api: JavaApi) -> None:
        self._cube_name: Final = cube_name
        self._java_api: Final = java_api

    @override
    def _get_delegate(self, *, key: str | None) -> Mapping[str, MaskingConfig]:
        raise NotImplementedError("Cannot get masking value.")

    @override
    def _update_delegate(self, other: Mapping[str, MaskingConfig], /) -> None:
        for key, value in other.items():
            includes = {}
            excludes = {}

            if value.only is not None:
                include_conditions = decombine_condition(
                    value.only,
                    allowed_subject_types=(HierarchyIdentifier,),
                    allowed_combination_operators=("and",),
                    allowed_target_types=(Constant,),
                )[0][2]

                for include in include_conditions:
                    includes[include.subject._java_description] = include.member_paths

            if value.exclude is not None:
                excludes_conditions = decombine_condition(
                    value.exclude,
                    allowed_subject_types=(HierarchyIdentifier,),
                    allowed_combination_operators=("and",),
                    allowed_target_types=(Constant,),
                )[0][2]

                for exclude in excludes_conditions:
                    excludes[exclude.subject._java_description] = exclude.member_paths

            self._java_api.set_masking_value(
                includes,
                excludes,
                cube_name=self._cube_name,
                role=key,
            )

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[str], /) -> None:
        raise NotImplementedError("Cannot delete masking value.")
