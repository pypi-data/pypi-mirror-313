from collections.abc import Iterator
from uuid import UUID

from faker import Faker
from injection.testing import test_singleton

from hundred.services.uuid import UUIDGenerator


@test_singleton(on=(UUIDGenerator, Iterator[UUID]), mode="fallback")
class FakeUUID4Generator(UUIDGenerator):
    __slots__ = ("__fake",)

    def __init__(self, fake: Faker) -> None:
        self.__fake = fake

    def __next__(self) -> UUID:
        return self.__fake.uuid4(cast_to=None)  # type: ignore[return-value]
