from uuid import UUID

from injection.testing import test_singleton

from hundred.ctx.auth.domain import User
from hundred.ctx.auth.ports import UserRepository
from hundred.testing.adapter.repository import InMemoryRepository


@test_singleton(on=UserRepository, inject=False, mode="fallback")
class InMemoryUserRepository(UserRepository):
    __slots__ = ("memory",)

    def __init__(self) -> None:
        self.memory = InMemoryRepository[User]()

    async def get(self, user_id: UUID) -> User | None:
        return await self.memory.get(user_id)

    async def get_by_identifier(self, identifier: str) -> User | None:
        uuid = UUID(identifier)
        return await self.get(uuid)

    async def save(self, user: User) -> None:
        await self.memory.save(user)
