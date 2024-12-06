from injection import injectable

from hundred.ctx.auth.domain import User
from hundred.services.uuid import UUIDGenerator


@injectable(mode="fallback")
class UserFactory:
    __slots__ = ("__uuid_gen",)

    def __init__(self, uuid_gen: UUIDGenerator) -> None:
        self.__uuid_gen = uuid_gen

    def build(self) -> User:
        return User(id=next(self.__uuid_gen))
