"Coproduct module"
from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity._bug import (
    LibraryBug,
)
from typing import (
    Callable,
    Generic,
    NoReturn,
    TypeVar,
    Union,
)

_L = TypeVar("_L")
_R = TypeVar("_R")
_T = TypeVar("_T")


@dataclass(frozen=True)
class _Empty:
    pass


@dataclass(frozen=True)
class _Coproduct(Generic[_L, _R]):
    "Internal/private Coproduct definition"
    left: Union[_L, _Empty]
    right: Union[_R, _Empty]
    left_val: bool

    @staticmethod
    def assert_non_empty(item: Union[_T, _Empty]) -> _T | NoReturn:
        "Ensure item is not `_Empty` or raise failure"
        if isinstance(item, _Empty):
            LibraryBug.new(ValueError("assert_non_empty received empty input"))
        return item


@dataclass(frozen=True)
class Coproduct(Generic[_L, _R]):
    """
    Also know as the union type, `Coproduct` unambiguously
    differentiate between the left and right case. This enables
    a better way of handling generic union types where `isinstance`
    cannot be used to differentiate the left-right cases.

    e.g. Union[None, None] = None # left and right injections are equal
    Coproduct[None, None] = Bool # left and right injections are NOT equal
    """

    _inner: _Coproduct[_L, _R]

    @staticmethod
    def inl(value: _L) -> Coproduct[_L, _R]:
        "The left injection: constucts a `Coproduct` from a value of a left type `_L`"
        return Coproduct(_Coproduct(value, _Empty(), True))

    @staticmethod
    def inr(value: _R) -> Coproduct[_L, _R]:
        "The right injection: constucts a `Coproduct` from a value of a right type `_R`"
        return Coproduct(_Coproduct(_Empty(), value, False))

    def map(
        self, transform_1: Callable[[_L], _T], transform_2: Callable[[_R], _T]
    ) -> _T:
        "Core transform from a `Coproduct` into some other type `_T`"
        if self._inner.left_val:
            return transform_1(_Coproduct.assert_non_empty(self._inner.left))
        return transform_2(_Coproduct.assert_non_empty(self._inner.right))

    def __str__(self) -> str:
        return self.__class__.__name__ + self.map(
            lambda lv: ".inl(" + str(lv) + ")",
            lambda rv: ".inr(" + str(rv) + ")",
        )


@dataclass(frozen=True)
class CoproductFactory(Generic[_L, _R]):
    """
    When type induction fails to recognize the left or right type,
    this factory can be used to explicitly indicate the types.
    """

    def inl(self, value: _L) -> Coproduct[_L, _R]:
        "Left injection for `Coproduct`"
        return Coproduct.inl(value)

    def inr(self, value: _R) -> Coproduct[_L, _R]:
        "Right injection for `Coproduct`"
        return Coproduct.inr(value)


@dataclass(frozen=True)
class UnionFactory(Generic[_L, _R]):
    """
    When type induction fails to recognize the left or right type
    on the built in Union this factory can help to set the types
    explicitly.
    """

    def inl(self, value: _L) -> Union[_L, _R]:
        "Left injection for builtin `Union`"
        return value

    def inr(self, value: _R) -> Union[_L, _R]:
        "Right injection for builtin `Union`"
        return value
