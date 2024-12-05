"Internal library bug definition"
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    NoReturn,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass
class LibraryBug(Exception):
    "If raised then there is a bug in the `fa_purity` library"
    _private: _Private = field(repr=False, hash=False, compare=False)
    traceback: Exception

    @staticmethod
    def new(exception: Exception) -> NoReturn:
        "Raise a new `LibraryBug` error"
        raise LibraryBug(_Private(), exception)
