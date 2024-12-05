from dataclasses import (
    dataclass,
)
from fa_purity._core.coproduct import (
    Coproduct,
    CoproductFactory,
    UnionFactory,
)
from typing import (
    Generic,
    TypeVar,
    Union,
)

_A = TypeVar("_A")
_B = TypeVar("_B")
_C = TypeVar("_C")
_L = TypeVar("_L")
_R = TypeVar("_R")


@dataclass(frozen=True)
class CoproductTransform(Generic[_L, _R]):
    _value: Coproduct[_L, _R]

    def swap(self) -> Coproduct[_R, _L]:
        def _right(item: _R) -> Coproduct[_R, _L]:
            return Coproduct.inl(item)

        def _left(item: _L) -> Coproduct[_R, _L]:
            return Coproduct.inr(item)

        return self._value.map(_left, _right)

    def to_union(self) -> Union[_L, _R]:
        factory: UnionFactory[_L, _R] = UnionFactory()
        return self._value.map(
            lambda l: factory.inl(l),
            lambda r: factory.inr(r),
        )

    @staticmethod
    def permutate(
        item: Coproduct[_A, Coproduct[_B, _C]]
    ) -> Coproduct[Coproduct[_A, _B], _C]:
        factory: CoproductFactory[Coproduct[_A, _B], _C] = CoproductFactory()
        return item.map(
            lambda a: factory.inl(Coproduct.inl(a)),
            lambda bc: bc.map(
                lambda b: factory.inl(Coproduct.inr(b)),
                lambda c: Coproduct.inr(c),
            ),
        )
