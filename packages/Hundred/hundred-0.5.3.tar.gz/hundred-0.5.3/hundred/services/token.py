import secrets
from abc import abstractmethod
from typing import Protocol, runtime_checkable

from injection import injectable


@runtime_checkable
class TokenService(Protocol):
    __slots__ = ()

    @abstractmethod
    def generate(self, nbytes: int = ...) -> str:
        raise NotImplementedError


@injectable(on=TokenService, inject=False, mode="fallback")
class SecretTokenService(TokenService):
    __slots__ = ()

    def generate(self, nbytes: int = 16) -> str:
        return secrets.token_urlsafe(nbytes)
