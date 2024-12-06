from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import (
    Collection,
    ItemsView,
    Iterator,
    KeysView,
    Mapping,
    ValuesView,
)
from typing import Generic, TypeVar, final

from typing_extensions import override

from .._ipython import KeyCompletable

AmbiguousKey = TypeVar("AmbiguousKey", bound=str | tuple[str, ...])
UnambiguousKey = TypeVar("UnambiguousKey", bound=str | tuple[str, ...])
Value = TypeVar("Value")


class DelegatingKeyDisambiguatingMapping(
    Mapping[AmbiguousKey, Value],
    Generic[AmbiguousKey, UnambiguousKey, Value],
    KeyCompletable,
    ABC,
):
    @abstractmethod
    def _get_delegate(
        self,
        *,
        key: AmbiguousKey | None,
    ) -> Mapping[UnambiguousKey, Value]:
        """Retrieve and return the delegate collection.

        Args:
            key: If not ``None``, only that key needs to be retrieved.
                This is an optimization used by the `__getitem__()` method.
                If *key* is not in the delegate collection, an empty mapping must be returned or a `KeyError` must be raised.
        """

    @final
    @override
    def __getitem__(self, key: AmbiguousKey, /) -> Value:
        delegate = self._get_delegate(key=key)
        match len(delegate):
            case 0:
                raise KeyError(key)
            case 1:
                return next(iter(delegate.values()))
            case _:
                raise ValueError(
                    f"Disambiguate `{key}` to narrow it down to one of {list(delegate)}.",
                )

    @final
    @override
    def __iter__(self) -> Iterator[UnambiguousKey]:  # type: ignore[override]
        return iter(self._get_delegate(key=None))

    @final
    @override
    def keys(self) -> KeysView[UnambiguousKey]:  # type: ignore[override]
        return self._get_delegate(key=None).keys()

    @final
    @override
    def values(self) -> ValuesView[Value]:
        return self._get_delegate(key=None).values()

    @final
    @override
    def items(self) -> ItemsView[UnambiguousKey, Value]:  # type: ignore[override]
        return self._get_delegate(key=None).items()

    @final
    @override
    def __len__(self) -> int:
        return len(self._get_delegate(key=None))

    @override
    def __repr__(self) -> str:
        return repr(self._get_delegate(key=None))

    @final
    @override
    def _get_key_completions(self) -> Collection[str]:
        return frozenset(key if isinstance(key, str) else key[-1] for key in self)
