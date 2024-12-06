import builtins
from collections.abc import Collection
from inspect import getmodule, isclass, isfunction, ismethod, ismodule
from types import ModuleType

from .._get_root_module_name import get_root_module_name

_BUILTIN_TYPES: Collection[object] = {
    getattr(builtins, name)
    for name in dir(builtins)
    if isinstance(getattr(builtins, name), type)
}


_PERSONAL_TYPE_NAME = "__REDACTED_TYPE__"


def _is_non_personal_module(module: ModuleType, /) -> bool:
    return get_root_module_name(module.__name__) == "atoti"


def get_non_personal_type_name(value: object, /) -> str:
    module = getmodule(value)
    is_value = not (
        ismodule(value) or isclass(value) or isfunction(value) or ismethod(value)
    )
    value_type = type(value) if is_value else value
    return (
        f"{f'{module.__name__}.{value_type.__name__}' if is_value else value_type}"  # type: ignore[attr-defined] # pyright: ignore[reportAttributeAccessIssue]
        if module and _is_non_personal_module(module)
        else f"{value_type.__name__ if value_type in _BUILTIN_TYPES else _PERSONAL_TYPE_NAME}"  # type: ignore[attr-defined] # pyright: ignore[reportAttributeAccessIssue]
    )
