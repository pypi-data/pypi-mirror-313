from uuid import UUID

from cq import Command, command_handler

from hundred.ctx.auth.factories import CheckCodeFactory
from hundred.ctx.auth.ports import (
    GeneratePinFunction,
    SessionRepository,
    TwoFactorAuthenticator,
)


class SendCheckCodeCommand(Command):
    application_id: UUID
    claimant_id: UUID


@command_handler(SendCheckCodeCommand)
class SendCheckCodeHandler:
    __slots__ = (
        "check_code_factory",
        "generate_pin",
        "provider",
        "session_repository",
    )

    def __init__(
        self,
        check_code_factory: CheckCodeFactory,
        generate_pin: GeneratePinFunction,
        provider: TwoFactorAuthenticator,
        session_repository: SessionRepository,
    ) -> None:
        self.check_code_factory = check_code_factory
        self.generate_pin = generate_pin
        self.provider = provider
        self.session_repository = session_repository

    async def handle(self, command: SendCheckCodeCommand) -> None:
        session = await self.session_repository.get(command.application_id)

        if (
            session is None
            or not session.is_owner(command.claimant_id)
            or not session.user.is_active
        ):
            return

        pin = await self.generate_pin()
        session.check_code = self.check_code_factory.build(pin)
        await self.session_repository.save(session)
        await self.provider.send_code(session.user.id, pin)
