# Iterable transforms
# should always return a new instance because Iterables are mutable
# result should be wrapped in a Cmd

from collections import (
    deque as deque_iter,
)
from fa_purity._core.cmd import (
    Cmd,
    CmdUnwrapper,
)
from fa_purity._core.frozen import (
    FrozenList,
    FrozenTools,
)
from itertools import (
    chain as _chain,
)
import more_itertools
from typing import (
    Callable,
    Iterable,
    Optional,
    Tuple,
    TypeVar,
)

_T = TypeVar("_T")
_R = TypeVar("_R")
_S = TypeVar("_S")


def chain(
    unchained: Iterable[Iterable[_T]],
) -> Iterable[_T]:
    return _chain.from_iterable(unchained)


def chunked(items: Iterable[_T], size: int) -> Iterable[FrozenList[_T]]:
    return map(FrozenTools.freeze, more_itertools.chunked(items, size))


def deque(items: Iterable[_T]) -> None:
    deque_iter(items, maxlen=0)


def filter_none(items: Iterable[Optional[_T]]) -> Iterable[_T]:
    return (i for i in items if i is not None)


def find_first(
    criteria: Callable[[_T], bool], items: Iterable[_T]
) -> Optional[_T]:
    for item in items:
        if criteria(item):
            return item
    return None


def squash(items: Iterable[Cmd[_T]]) -> Cmd[Iterable[_T]]:
    def _action(unwrapper: CmdUnwrapper) -> Iterable[_T]:
        for item in items:
            yield unwrapper.act(item)

    return Cmd.new_cmd(_action)


def until_none(items: Iterable[Optional[_T]]) -> Iterable[_T]:
    for item in items:
        if item is None:
            break
        yield item


def infinite_gen(function: Callable[[_T], _T], init: _T) -> Iterable[_T]:
    yield init
    current = init
    while True:
        current = function(current)
        yield current


def gen_next(
    function: Callable[[_S, _T], Tuple[_S, _R]],
    init_state: _S,
    iter: Iterable[_T],
) -> Iterable[_R]:
    state = init_state
    for i in iter:
        state, current = function(state, i)
        yield current
