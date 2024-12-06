from datetime import timedelta

from injection import injectable
from pydantic import SecretStr

from hundred.ctx.auth.aliases import CheckCodeLifespan
from hundred.ctx.auth.domain import CheckCode
from hundred.services.datetime import DateTimeService
from hundred.services.hasher import Hasher
from hundred.services.uuid import UUIDGenerator


@injectable(mode="fallback")
class CheckCodeFactory:
    __slots__ = (
        "__datetime_service",
        "__check_code_lifespan",
        "__hasher",
        "__uuid_gen",
    )

    def __init__(
        self,
        *,
        datetime_service: DateTimeService,
        check_code_lifespan: CheckCodeLifespan = timedelta(minutes=5),
        hasher: Hasher,
        uuid_gen: UUIDGenerator,
    ) -> None:
        self.__datetime_service = datetime_service
        self.__check_code_lifespan = check_code_lifespan
        self.__hasher = hasher
        self.__uuid_gen = uuid_gen

    def build(self, code: str) -> CheckCode:
        expiration = self.__datetime_service.utcnow() + self.__check_code_lifespan
        return CheckCode(
            id=next(self.__uuid_gen),
            value=SecretStr(self.__hasher.hash(code)),
            expiration=expiration,
        )
