from dataclasses import (
    dataclass,
)
from fa_purity._core import (
    iter_factory,
)
from fa_purity._core.cmd import (
    Cmd,
    CmdUnwrapper,
)
from fa_purity._core.maybe import (
    Maybe,
)
from fa_purity._core.pure_iter import (
    PureIter,
)
from fa_purity._core.unsafe import (
    Unsafe,
)
from typing import (
    Optional,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class PureIterTransform:
    "`PureIter` common transforms"

    @staticmethod
    def chain(
        unchained: PureIter[PureIter[_T]],
    ) -> PureIter[_T]:
        return unchained.bind(lambda x: x)

    @staticmethod
    def consume(p_iter: PureIter[Cmd[None]]) -> Cmd[None]:
        def _action(unwrapper: CmdUnwrapper) -> None:
            for c in p_iter:
                unwrapper.act(c)

        return Cmd.new_cmd(_action)

    @staticmethod
    def filter_opt(items: PureIter[Optional[_T]]) -> PureIter[_T]:
        return Unsafe.pure_iter_from_cmd(
            Cmd.wrap_impure(lambda: iter_factory.filter_none(items))
        )

    @classmethod
    def filter_maybe(cls, items: PureIter[Maybe[_T]]) -> PureIter[_T]:
        return cls.filter_opt(items.map(lambda x: x.value_or(None)))

    @staticmethod
    def until_none(items: PureIter[Optional[_T]]) -> PureIter[_T]:
        return Unsafe.pure_iter_from_cmd(
            Cmd.wrap_impure(lambda: iter_factory.until_none(items))
        )

    @classmethod
    def until_empty(cls, items: PureIter[Maybe[_T]]) -> PureIter[_T]:
        return cls.until_none(items.map(lambda m: m.value_or(None)))
