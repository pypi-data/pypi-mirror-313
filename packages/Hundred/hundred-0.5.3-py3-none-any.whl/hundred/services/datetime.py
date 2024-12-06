from abc import abstractmethod
from datetime import UTC, datetime, timezone
from typing import Protocol, runtime_checkable

from injection import injectable


@runtime_checkable
class DateTimeService(Protocol):
    __slots__ = ()

    @abstractmethod
    def now(self, tz: timezone = ..., /) -> datetime:
        raise NotImplementedError

    def utcnow(self) -> datetime:
        return self.now(UTC)


@injectable(on=DateTimeService, inject=False, mode="fallback")
class DefaultDateTimeService(DateTimeService):
    __slots__ = ()

    def now(self, tz: timezone | None = None, /) -> datetime:
        return datetime.now(tz)
