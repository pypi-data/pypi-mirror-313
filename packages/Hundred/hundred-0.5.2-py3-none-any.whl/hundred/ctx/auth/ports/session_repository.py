from abc import abstractmethod
from typing import Protocol, runtime_checkable
from uuid import UUID

from injection import should_be_injectable

from hundred.ctx.auth.domain import Session


@should_be_injectable
@runtime_checkable
class SessionRepository(Protocol):
    __slots__ = ()

    @abstractmethod
    async def get(self, application_id: UUID) -> Session | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, session: Session) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, application_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_user_id(
        self,
        user_id: UUID,
        current_application_id: UUID | None = ...,
    ) -> None:
        raise NotImplementedError
