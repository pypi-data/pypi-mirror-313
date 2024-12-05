from __future__ import (
    annotations,
)

from .coproduct import (
    Coproduct,
)
from .unit import (
    unit,
    UnitType,
)
from collections.abc import (
    Callable,
)
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    TypeVar,
)

_A = TypeVar("_A")


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class Bool:
    """
    Alternative to primitive bool.
    - useful to avoid `if-else` syntax
    - lazy evaluation on map
    """

    _private: _Private = field(repr=False, hash=False, compare=False)
    _value: Coproduct[UnitType, UnitType]

    @staticmethod
    def true_value() -> Bool:
        return Bool(_Private(), Coproduct.inl(unit))

    @staticmethod
    def false_value() -> Bool:
        return Bool(_Private(), Coproduct.inr(unit))

    @classmethod
    def from_primitive(cls, raw: bool) -> Bool:
        if raw:
            return cls.true_value()
        return cls.false_value()

    def map(
        self,
        true_case: Callable[[UnitType], _A],
        false_case: Callable[[UnitType], _A],
    ) -> _A:
        return self._value.map(true_case, false_case)

    def __str__(self) -> str:
        return self.__class__.__name__ + self.map(
            lambda _: ".True",
            lambda _: ".False",
        )
