from typing import Final, Protocol, final

from typing_extensions import override

from ._identification import CubeIdentifier


class _GetCapacity(Protocol):
    def __call__(self, cube_name: str, /) -> int: ...


class _SetCapacity(Protocol):
    def __call__(self, cube_name: str, capacity: int, /) -> None: ...


@final
class AggregatesCache:
    """The aggregates cache associated with a :class:`~atoti.Cube`."""

    def __init__(
        self,
        *,
        cube_identifier: CubeIdentifier,
        set_capacity: _SetCapacity,
        get_capacity: _GetCapacity,
    ) -> None:
        self._cube_identifier: Final = cube_identifier
        self._set_capacity: Final = set_capacity
        self._get_capacity: Final = get_capacity

    @property
    def capacity(self) -> int:
        """Capacity of the cache.

        If:

        * ``> 0``: corresponds to the maximum amount of ``{location: measure}`` pairs that the cache can hold.
        * ``0``: Sharing is enabled but caching is disabled.
          Queries will share their computations if they are executed at the same time, but the aggregated values will not be stored to be retrieved later.
        * ``< 0``: Caching and sharing are disabled.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> table = session.create_table("Example", data_types={"id": "int"})
            >>> cube = session.create_cube(table)
            >>> cube.aggregates_cache.capacity
            100
            >>> cube.aggregates_cache.capacity = -1
            >>> cube.aggregates_cache.capacity
            -1
        """
        return self._get_capacity(self._cube_identifier.cube_name)

    @capacity.setter
    def capacity(self, capacity: int) -> None:
        self._set_capacity(self._cube_identifier.cube_name, capacity)

    @override
    def __repr__(self) -> str:
        return repr({"capacity": self.capacity})
