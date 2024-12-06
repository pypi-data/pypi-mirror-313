from __future__ import annotations

from collections.abc import Callable
from textwrap import dedent
from typing import Any, TypeVar, cast

from typing_extensions import ParamSpec

_P = ParamSpec("_P")
_R = TypeVar("_R")


# Taken from Pandas:
# https://github.com/pandas-dev/pandas/blame/8aa707298428801199280b2b994632080591700a/pandas/util/_decorators.py#L332
def doc(
    *args: str | Callable[..., Any],
    **kwargs: str,
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    """Take docstring templates, concatenate them and perform string substitution."""

    def decorator(function: Callable[_P, _R]) -> Callable[_P, _R]:
        docstring_components: list[str | Callable[..., Any]] = []

        if function.__doc__:
            docstring_components.append(dedent(function.__doc__))

        docstring_components.extend(
            arg for arg in cast(Any, args) if isinstance(arg, str) or arg.__doc__
        )

        # Formatting templates and concatenating docstring
        function.__doc__ = "".join(
            [
                arg.format(**kwargs)
                if isinstance(arg, str)
                else dedent(arg.__doc__ or "")
                for arg in docstring_components
            ],
        )

        return function

    return decorator
