from uuid import UUID

from cq import Command, command_handler
from pydantic import SecretStr

from hundred.ctx.auth.dto import Authenticated
from hundred.ctx.auth.ports import SessionRepository
from hundred.ctx.auth.services import SessionService
from hundred.exceptions import Unauthorized
from hundred.gettext import gettext as _
from hundred.services.datetime import DateTimeService
from hundred.services.hasher import Hasher


class VerifyCheckCodeCommand(Command):
    application_id: UUID
    claimant_id: UUID
    code: SecretStr

    @property
    def raw_code(self) -> str:
        return self.code.get_secret_value()


@command_handler(VerifyCheckCodeCommand)
class VerifyCheckCodeHandler:
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

    async def handle(self, command: VerifyCheckCodeCommand) -> Authenticated:
        session = await self.session_repository.get(command.application_id)
        now = self.datetime_service.utcnow()

        if (
            session is None
            or not session.is_owner(command.claimant_id)
            or not session.user.is_active
            or (check_code := session.check_code) is None
            or check_code.has_expired(now)
            or not self.hasher.verify(command.raw_code, check_code.raw_value)
        ):
            raise Unauthorized(_("invalid_check_code"))

        session.check_code = None
        session.last_seen = now

        if not session.is_verified:
            session.verify()

        if session.is_temporary:
            await self.session_service.logout(session.application_id)
        else:
            await self.session_repository.save(session)

        access_token = self.session_service.new_access_token(
            session=session,
            is_trusted=True,
        )
        return Authenticated(access_token=SecretStr(access_token))
