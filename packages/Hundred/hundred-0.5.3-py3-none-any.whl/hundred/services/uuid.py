from collections.abc import Iterator
from typing import Protocol, runtime_checkable
from uuid import UUID

from injection import injectable
from ulid import ULID

from hundred.services.datetime import DateTimeService


@runtime_checkable
class UUIDGenerator(Iterator[UUID], Protocol):
    __slots__ = ()


@injectable(on=(UUIDGenerator, Iterator[UUID]), mode="fallback")
class ULIDGenerator(UUIDGenerator):
    __slots__ = ("__datetime_service",)

    def __init__(self, datetime_service: DateTimeService) -> None:
        self.__datetime_service = datetime_service

    def __next__(self) -> UUID:
        now = self.__datetime_service.utcnow()
        return ULID.from_datetime(now).to_uuid()
