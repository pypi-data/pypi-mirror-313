from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity._bug import (
    LibraryBug,
)
from fa_purity._core.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity._core.result import (
    Result,
    ResultE,
    ResultFactory,
)
from fa_purity._core.utils import (
    cast_exception,
)
from typing import (
    TypeVar,
)

_S = TypeVar("_S")
_F = TypeVar("_F")
_K = TypeVar("_K")
_V = TypeVar("_V")


@dataclass(frozen=True)
class ResultTransform:
    @staticmethod
    def all_ok(
        items: FrozenList[Result[_S, _F]]
    ) -> Result[FrozenList[_S], _F]:
        ok_list = []
        for i in items:
            if i.map(lambda _: True).value_or(False):
                val: _S = i.or_else_call(
                    lambda: LibraryBug.new(
                        ValueError("all_ok extract value bug")
                    )
                )
                ok_list.append(val)
            else:
                fail: _F = i.swap().or_else_call(
                    lambda: LibraryBug.new(
                        ValueError("all_ok extract fail bug")
                    )
                )
                return Result.failure(fail, FrozenList[_S])
        return Result.success(tuple(ok_list))

    @staticmethod
    def try_get(data: FrozenDict[_K, _V], key: _K) -> ResultE[_V]:
        factory: ResultFactory[_V, Exception] = ResultFactory()
        if key in data:
            return factory.success(data[key])
        return factory.failure(KeyError(key)).alt(cast_exception)
