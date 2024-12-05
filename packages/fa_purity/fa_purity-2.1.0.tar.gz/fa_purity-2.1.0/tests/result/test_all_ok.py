from fa_purity import (
    FrozenList,
    Result,
    ResultTransform,
    Unsafe,
)


def test_all_ok() -> None:
    success: FrozenList[Result[int, str]] = (
        Result.success(1),
        Result.success(2),
    )
    assert (
        ResultTransform.all_ok(success)
        .alt(lambda _: Unsafe.raise_exception(Exception("failure")))
        .to_union()
    )
    failure: FrozenList[Result[int, str]] = (
        Result.success(1),
        Result.failure("foo"),
    )
    assert (
        ResultTransform.all_ok(failure)
        .swap()
        .alt(lambda _: Unsafe.raise_exception(Exception("not failure")))
        .to_union()
    )
