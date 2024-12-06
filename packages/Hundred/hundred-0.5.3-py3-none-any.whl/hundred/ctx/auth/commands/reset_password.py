from uuid import UUID

from cq import Command, command_handler
from pydantic import SecretStr

from hundred.ctx.auth.domain import SessionStatus, User
from hundred.ctx.auth.dto import Authenticated
from hundred.ctx.auth.ports import SessionRepository, UserRepository
from hundred.ctx.auth.services import SessionService
from hundred.exceptions import NotFound
from hundred.services.hasher import Hasher


class ResetPasswordCommand(Command):
    application_id: UUID
    claimant_id: UUID
    password: SecretStr

    @property
    def raw_password(self) -> str:
        return self.password.get_secret_value()


@command_handler(ResetPasswordCommand)
class ResetPasswordHandler:
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

    async def handle(self, command: ResetPasswordCommand) -> Authenticated:
        user_id = command.claimant_id
        user = await self.user_repository.get(user_id)

        if user is None:
            raise NotFound.from_target(User.to_readable(user_id))

        user.password = SecretStr(self.hasher.hash(command.raw_password))
        await self.user_repository.save(user)

        await self.session_repository.delete_by_user_id(user_id)
        return await self.session_service.new_session(
            command.application_id,
            user,
            SessionStatus.VERIFIED,
        )
