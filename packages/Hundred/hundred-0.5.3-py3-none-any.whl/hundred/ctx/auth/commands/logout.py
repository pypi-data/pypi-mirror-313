from uuid import UUID

from cq import Command, command_handler

from hundred.ctx.auth.ports import SessionRepository
from hundred.ctx.auth.services import SessionService
from hundred.exceptions import Forbidden


class LogoutCommand(Command):
    application_id: UUID
    claimant_id: UUID


@command_handler(LogoutCommand)
class LogoutHandler:
    __slots__ = ("session_repository", "session_service")

    def __init__(
        self,
        session_repository: SessionRepository,
        session_service: SessionService,
    ) -> None:
        self.session_repository = session_repository
        self.session_service = session_service

    async def handle(self, command: LogoutCommand) -> None:
        application_id = command.application_id
        session = await self.session_repository.get(application_id)

        if session is not None and session.is_owner(command.claimant_id):
            await self.session_service.logout(application_id)
            return

        raise Forbidden()
