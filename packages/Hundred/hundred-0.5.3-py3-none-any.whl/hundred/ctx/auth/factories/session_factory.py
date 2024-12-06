from uuid import UUID

from injection import injectable
from pydantic import SecretStr

from hundred.ctx.auth.domain import Session, User
from hundred.services.datetime import DateTimeService
from hundred.services.hasher import Hasher
from hundred.services.uuid import UUIDGenerator


@injectable(mode="fallback")
class SessionFactory:
    __slots__ = (
        "__datetime_service",
        "__hasher",
        "__uuid_gen",
    )

    def __init__(
        self,
        datetime_service: DateTimeService,
        hasher: Hasher,
        uuid_gen: UUIDGenerator,
    ) -> None:
        self.__datetime_service = datetime_service
        self.__hasher = hasher
        self.__uuid_gen = uuid_gen

    def build(
        self,
        application_id: UUID,
        user: User,
        token: str | None = None,
    ) -> Session:
        now = self.__datetime_service.utcnow()
        hashed_token = SecretStr(self.__hasher.hash(token)) if token else None
        return Session(
            id=next(self.__uuid_gen),
            application_id=application_id,
            created_at=now,
            last_seen=now,
            token=hashed_token,
            user=user,
        )
