from uuid import UUID

from cq import Command, command_handler
from pydantic import SecretStr

from hundred.ctx.auth.dto import Authenticated
from hundred.ctx.auth.ports import SessionRepository
from hundred.ctx.auth.services import SessionService
from hundred.exceptions import Unauthorized
from hundred.services.datetime import DateTimeService
from hundred.services.hasher import Hasher


class RefreshCommand(Command):
    application_id: UUID
    session_token: SecretStr

    @property
    def raw_session_token(self) -> str:
        return self.session_token.get_secret_value()


@command_handler(RefreshCommand)
class RefreshHandler:
    __slots__ = (
        "datetime_service",
        "hasher",
        "session_repository",
        "session_service",
    )

    def __init__(
        self,
        datetime_service: DateTimeService,
        hasher: Hasher,
        session_repository: SessionRepository,
        session_service: SessionService,
    ) -> None:
        self.datetime_service = datetime_service
        self.hasher = hasher
        self.session_repository = session_repository
        self.session_service = session_service

    async def handle(self, command: RefreshCommand) -> Authenticated:
        session = await self.session_repository.get(command.application_id)
        token = command.raw_session_token

        if (
            session is None
            or not session.user.is_active
            or (hashed_token := session.raw_token) is None
            or not self.hasher.verify(token, hashed_token)
        ):
            raise Unauthorized()

        if self.hasher.needs_rehash(hashed_token):
            session.token = SecretStr(self.hasher.hash(token))

        session.last_seen = self.datetime_service.utcnow()
        await self.session_repository.save(session)

        access_token = self.session_service.new_access_token(session=session)
        return Authenticated(access_token=SecretStr(access_token))
