# from datetime import (
#     timedelta,
#     timezone,
# )
# from fa_purity.date_time import (
#     DatetimeFactory,
# )


# def test_epoch() -> None:
#     assert DatetimeFactory.EPOCH_START


# def test_utc_addition() -> None:
#     delta = timedelta(1, 2, 3, 5, 6, 7)
#     date_time = DatetimeFactory.new_utc(2000, 1, 1, 0, 0, 0, 0)
#     assert (date_time + delta).date_time == date_time.date_time + delta


# def test_tz_addition() -> None:
#     delta = timedelta(1, 2, 3, 5, 6, 7)
#     date_time = DatetimeFactory.new_tz(2000, 1, 1, 0, 0, 0, 0, timezone.utc)
#     assert (date_time + delta).date_time == date_time.date_time + delta
