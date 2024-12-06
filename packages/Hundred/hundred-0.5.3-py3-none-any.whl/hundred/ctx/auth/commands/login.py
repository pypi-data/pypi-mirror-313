from uuid import UUID

from cq import Command, command_handler
from pydantic import SecretStr

from hundred.ctx.auth.dto import Authenticated
from hundred.ctx.auth.ports import UserRepository
from hundred.ctx.auth.services import SessionService
from hundred.exceptions import Unauthorized
from hundred.gettext import gettext as _
from hundred.services.hasher import Hasher


class LoginCommand(Command):
    application_id: UUID
    identifier: str
    password: SecretStr

    @property
    def raw_password(self) -> str:
        return self.password.get_secret_value()


@command_handler(LoginCommand)
class LoginHandler:
    __slots__ = (
        "hasher",
        "session_service",
        "user_repository",
    )

    def __init__(
        self,
        hasher: Hasher,
        session_service: SessionService,
        user_repository: UserRepository,
    ) -> None:
        self.hasher = hasher
        self.session_service = session_service
        self.user_repository = user_repository

    async def handle(self, command: LoginCommand) -> Authenticated:
        user = await self.user_repository.get_by_identifier(command.identifier)
        password = command.raw_password

        if (
            user is None
            or not user.is_active
            or (hashed_password := user.raw_password) is None
            or not self.hasher.verify(password, hashed_password)
        ):
            raise Unauthorized(_("bad_credentials"))

        if self.hasher.needs_rehash(hashed_password):
            user.password = SecretStr(self.hasher.hash(password))
            await self.user_repository.save(user)

        application_id = command.application_id
        await self.session_service.ensure_session_can_be_created(application_id)
        return await self.session_service.new_session(application_id, user)
