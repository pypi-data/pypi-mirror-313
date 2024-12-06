from uuid import UUID

from cq import Command, command_handler
from pydantic import SecretStr

from hundred.ctx.auth.ports import SessionRepository, UserRepository
from hundred.ctx.auth.services import SessionService
from hundred.exceptions import Unauthorized
from hundred.gettext import gettext as _
from hundred.services.hasher import Hasher


class ChangePasswordCommand(Command):
    application_id: UUID
    claimant_id: UUID
    current_password: SecretStr
    new_password: SecretStr

    @property
    def raw_current_password(self) -> str:
        return self.current_password.get_secret_value()

    @property
    def raw_new_password(self) -> str:
        return self.new_password.get_secret_value()


@command_handler(ChangePasswordCommand)
class ChangePasswordHandler:
    __slots__ = (
        "hasher",
        "session_repository",
        "session_service",
        "user_repository",
    )

    def __init__(
        self,
        hasher: Hasher,
        session_repository: SessionRepository,
        session_service: SessionService,
        user_repository: UserRepository,
    ) -> None:
        self.hasher = hasher
        self.session_repository = session_repository
        self.session_service = session_service
        self.user_repository = user_repository

    async def handle(self, command: ChangePasswordCommand) -> None:
        user_id = command.claimant_id
        user = await self.user_repository.get(user_id)

        if (
            user is None
            or (hashed_password := user.raw_password) is None
            or not self.hasher.verify(command.raw_current_password, hashed_password)
        ):
            raise Unauthorized(_("wrong_password"))

        user.password = SecretStr(self.hasher.hash(command.raw_new_password))
        await self.user_repository.save(user)

        await self.session_repository.delete_by_user_id(
            user_id=user_id,
            current_application_id=command.application_id,
        )
