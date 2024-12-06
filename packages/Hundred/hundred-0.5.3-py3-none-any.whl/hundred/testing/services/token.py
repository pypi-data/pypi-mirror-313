import string

from faker import Faker
from injection.testing import test_singleton

from hundred.services.token import TokenService


@test_singleton(on=TokenService, mode="fallback")
class FakeTokenService(TokenService):
    __slots__ = ("__fake",)

    def __init__(self, fake: Faker) -> None:
        self.__fake = fake

    def generate(self, nbytes: int = 16) -> str:
        return self.__fake.bothify("?" * nbytes, string.hexdigits)
