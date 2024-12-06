from uuid import UUID

from cq import Command, command_handler

from hundred.ctx.auth.factories import UserFactory
from hundred.ctx.auth.ports import UserRepository


class NewUserCommand(Command): ...


@command_handler(NewUserCommand)
class NewUserHandler:
    __slots__ = ("user_factory", "user_repository")

    def __init__(
        self,
        user_factory: UserFactory,
        user_repository: UserRepository,
    ) -> None:
        self.user_factory = user_factory
        self.user_repository = user_repository

    async def handle(self, command: NewUserCommand) -> UUID:
        user = self.user_factory.build()
        await self.user_repository.save(user)
        return user.id
