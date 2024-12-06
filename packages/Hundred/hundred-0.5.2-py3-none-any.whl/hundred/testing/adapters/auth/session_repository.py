from uuid import UUID

from injection.testing import test_singleton

from hundred.ctx.auth.domain import Session
from hundred.ctx.auth.ports import SessionRepository, UserRepository
from hundred.testing.adapter.repository import InMemoryRepository


@test_singleton(on=SessionRepository, mode="fallback")
class InMemorySessionRepository(SessionRepository):
    __slots__ = ("memory", "__user_repository")

    def __init__(self, user_repository: UserRepository) -> None:
        self.memory = InMemoryRepository[Session](self.__post_processor)
        self.__user_repository = user_repository

    async def get(self, application_id: UUID) -> Session | None:
        return await self.memory.get_first(
            lambda session: session.application_id == application_id,
        )

    async def save(self, session: Session) -> None:
        await self.memory.save(session)

    async def delete(self, application_id: UUID) -> None:
        await self.memory.delete_by(
            lambda session: session.application_id == application_id
        )

    async def delete_by_user_id(
        self,
        user_id: UUID,
        current_application_id: UUID | None = None,
    ) -> None:
        await self.memory.delete_by(
            lambda session: session.user.id == user_id
            and session.application_id != current_application_id
        )

    async def __post_processor(self, session: Session) -> Session:
        user = await self.__user_repository.get(session.user.id)
        return session.model_copy(update={"user": user})
