from typing import (
    NoReturn,
)


def raise_exception(err: Exception) -> NoReturn:
    "function wrapper of the raise statement"
    raise err


def cast_exception(err: Exception) -> Exception:
    "Useful for safe casting an `Exception` subclass into `Exception`"
    return err
