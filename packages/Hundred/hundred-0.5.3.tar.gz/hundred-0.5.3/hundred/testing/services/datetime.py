from collections.abc import Iterator
from datetime import UTC, datetime, timedelta, timezone

from injection.testing import test_singleton

from hundred.services.datetime import DateTimeService


@test_singleton(on=DateTimeService, inject=False, mode="fallback")
class SequentialDateTimeService(DateTimeService):
    __slots__ = ("__sequence",)

    def __init__(self) -> None:
        self.reset()

    def now(self, tz: timezone | None = None, /) -> datetime:
        value = next(self.__sequence)
        return value.astimezone(tz)

    def reset(
        self,
        start_date: datetime = datetime(year=2012, month=12, day=12, tzinfo=UTC),
        delta: timedelta = timedelta(seconds=1),
    ) -> None:
        self.__sequence = self.__new_sequence(start_date, delta)

    @staticmethod
    def __new_sequence(start_date: datetime, delta: timedelta) -> Iterator[datetime]:
        next_value = start_date

        while True:
            yield next_value
            next_value += delta
