from .cmd import (
    Cmd,
    unsafe_unwrap,
)
from collections.abc import (
    Iterable,
)
from dataclasses import (
    dataclass,
)
from fa_purity._core.pure_iter import (
    PureIter,
    unsafe_from_cmd,
)
from fa_purity._core.stream import (
    Stream,
    unsafe_from_cmd as _unsafe_stream_from_cmd,
    unsafe_to_iter,
)
from typing import (
    NoReturn,
    TypeVar,
)

_A = TypeVar("_A")


@dataclass(frozen=True)
class Unsafe:
    """
    This class holds unsafe methods.
    - Type-check cannot ensure its proper use
    - Do not use until is strictly necessary
    - Do unit test over the function defined by these
    """

    @staticmethod
    def pure_iter_from_cmd(command: Cmd[Iterable[_A]]) -> PureIter[_A]:
        """
        The supplied commnad argument MUST produce semanticly equivalent iterables.
        This is: possibly different objects that represents the same thing

        - if Iterable is IMMUTABLE (e.g. tuple) then requirement is fulfilled
        - if Iterable is MUTABLE then the commnad must call the obj constructor (that is not pure)
        with the same arguments for ensuring equivalence.

        Non compliant code:
          y = map(lambda i: i + 1, range(0, 10))
          x = unsafe_create_pure_iter(
              Cmd.from_impure(lambda: y)
          )
          # y is a map obj instance; cmd lambda is pinned with a single ref
          # since map is MUTABLE the ref should change at every call

        Compliant code:
          x = unsafe_create_pure_iter(
              Cmd.from_impure(
                  lambda: map(lambda i: i + 1, range(0, 10))
              )
          )
          # cmd lambda produces a new ref in each call
          # but all of them are equivalent (created with the same args)
        """
        return unsafe_from_cmd(command)

    @staticmethod
    def stream_from_cmd(command: Cmd[Iterable[_A]]) -> Stream[_A]:
        """
        As with `unsafe_create_pure_iter` the cmd must return a new iterable
        object in each call to ensure that the stream is never consumed,
        nevertheless they can be semanticly different iterables.
        """
        return _unsafe_stream_from_cmd(command)

    @staticmethod
    def stream_to_iter(stream: Stream[_A]) -> Cmd[Iterable[_A]]:
        "If possible avoid to extract the inner iterable"
        return unsafe_to_iter(stream)

    @staticmethod
    def compute(command: Cmd[_A]) -> _A:
        """
        [WARNING] this will execute the Cmd
        [NOTICE] If you what to define a new `Cmd` using this,
        first consider using the `Cmd.new_cmd` constructor instead.

        Only use when:
        - all executions of the action `Cmd[_A]` result in the same
        output instance `_A`
        - side effects are not present or negligible

        e.g. unwrap a cmd when used on a cached function definition
        """
        return unsafe_unwrap(command)

    @staticmethod
    def raise_exception(err: Exception) -> NoReturn:
        """
        Function wrapper of the raise statement.
        This is unsafe since it should be not possible to
        raise an error on a pure program.
        Consider returning a `Result` object instead.
        """
        raise err
