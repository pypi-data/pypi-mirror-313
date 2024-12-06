from abc import abstractmethod
from typing import Protocol, runtime_checkable
from uuid import UUID

from injection import should_be_injectable


@should_be_injectable
@runtime_checkable
class TwoFactorAuthenticator(Protocol):
    __slots__ = ()

    @abstractmethod
    async def send_code(self, user_id: UUID, code: str) -> None:
        raise NotImplementedError
