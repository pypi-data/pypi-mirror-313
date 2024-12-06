from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence, Set as AbstractSet
from typing import Generic, TypeVar, final, overload

from typing_extensions import Self

from .._ipython import KeyCompletable
from .delegating_key_disambiguating_mapping import (
    AmbiguousKey,
    DelegatingKeyDisambiguatingMapping,
    UnambiguousKey,
    Value as ReadValue,
)

WriteValue = TypeVar("WriteValue")


class _DelegatingConvertingMapping(
    DelegatingKeyDisambiguatingMapping[AmbiguousKey, UnambiguousKey, ReadValue],
    Generic[AmbiguousKey, UnambiguousKey, ReadValue, WriteValue],
    KeyCompletable,
    ABC,
):
    """A `Mapping` that also implements `MutableMapping` methods but where they read and write types can differ."""

    @abstractmethod
    def _update_delegate(
        self,
        other: Mapping[AmbiguousKey, WriteValue],
        /,
    ) -> None: ...

    @overload
    def update(
        self,
        other: Mapping[AmbiguousKey, WriteValue],
        /,
        **kwargs: WriteValue,
    ) -> None: ...

    @overload
    def update(
        self,
        # Using `Sequence | AbstractSet` instead of `Iterable` or `Collection` to have Pydantic validate `other` without converting it to a `ValidatorIterator`.
        other: Sequence[tuple[AmbiguousKey, WriteValue]]
        | AbstractSet[tuple[AmbiguousKey, WriteValue]],
        /,
        **kwargs: WriteValue,
    ) -> None: ...

    @overload
    def update(self, **kwargs: WriteValue) -> None: ...

    # `MutableMapping` method.
    @final  # type: ignore[misc]
    def update(  # pyright: ignore[reportInconsistentOverload]
        self,
        other: Mapping[AmbiguousKey, WriteValue]
        | Sequence[tuple[AmbiguousKey, WriteValue]]
        | AbstractSet[tuple[AmbiguousKey, WriteValue]]
        | None = None,
        /,
        **kwargs: WriteValue,
    ) -> None:
        _other: dict[AmbiguousKey, WriteValue] = {}
        if other is not None:
            _other.update(other)
        _other.update(**kwargs)
        self._update_delegate(_other)

    # Not a `MutableMapping` method but present on `dict`.
    @final
    def __ior__(self, other: Mapping[AmbiguousKey, WriteValue], /) -> Self:
        self.update(other)
        return self

    # `MutableMapping` method.
    @final
    def __setitem__(self, key: AmbiguousKey, value: WriteValue, /) -> None:
        self.update({key: value})

    @abstractmethod
    def _delete_delegate_keys(
        self,
        keys: AbstractSet[AmbiguousKey | UnambiguousKey],
        /,
    ) -> None: ...

    # `MutableMapping` method.
    @final
    def clear(self) -> None:
        return self._delete_delegate_keys(self.keys())

    # `MutableMapping` method.
    @final
    def __delitem__(self, key: AmbiguousKey, /) -> None:
        return self._delete_delegate_keys({key})


class DelegatingConvertingMapping(
    _DelegatingConvertingMapping[AmbiguousKey, UnambiguousKey, ReadValue, WriteValue],
    ABC,
):
    # Not a `MutableMapping` method but useful to avoid repeating the key in `my_measure = cube.measure.set("name", tt.agg.sum(...)); my_measure.description = ...; my_measure.formatter = ...`
    # It only makes sense on truly converting mappings (where ReadValue != WriteValue), not on `DelegatingMutableMapping`.
    @final
    def set(
        self,
        key: AmbiguousKey,
        value: WriteValue,
        /,
    ) -> ReadValue:
        """Add *value* to the mapping under *key* and return the converted value.

        :meta private:
        """
        self[key] = value
        return self[key]
