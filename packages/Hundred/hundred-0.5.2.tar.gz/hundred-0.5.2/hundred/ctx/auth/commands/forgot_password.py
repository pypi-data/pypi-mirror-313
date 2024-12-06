from uuid import UUID

from cq import Command, command_handler

from hundred.ctx.auth.dto import Authenticated
from hundred.ctx.auth.ports import UserRepository
from hundred.ctx.auth.services import SessionService


class ForgotPasswordCommand(Command):
    application_id: UUID
    identifier: str


@command_handler(ForgotPasswordCommand)
class ForgotPasswordHandler:
    __slots__ = ("session_service", "user_repository")

    def __init__(
        self,
        session_service: SessionService,
        user_repository: UserRepository,
    ) -> None:
        self.session_service = session_service
        self.user_repository = user_repository

    async def handle(self, command: ForgotPasswordCommand) -> Authenticated:
        user = await self.user_repository.get_by_identifier(command.identifier)

        if user is None or not user.is_active:
            return await self.session_service.new_fake_temporary_session()

        application_id = command.application_id
        await self.session_service.ensure_session_can_be_created(application_id)
        return await self.session_service.new_temporary_session(application_id, user)
