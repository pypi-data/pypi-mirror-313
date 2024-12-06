from abc import abstractmethod
from typing import Protocol, runtime_checkable

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from injection import injectable


@runtime_checkable
class Hasher(Protocol):
    __slots__ = ()

    @abstractmethod
    def hash(self, value: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify(self, value: str, hash: str) -> bool:
        raise NotImplementedError

    def needs_rehash(self, hash: str) -> bool:
        return False


@injectable(on=Hasher, inject=False, mode="fallback")
class Argon2Hasher(Hasher):
    __slots__ = ("__internal_hasher",)

    def __init__(self) -> None:
        self.__internal_hasher = PasswordHasher()

    def hash(self, value: str) -> str:
        return self.__internal_hasher.hash(value)

    def verify(self, value: str, hash: str) -> bool:
        try:
            return self.__internal_hasher.verify(hash, value)
        except (InvalidHashError, VerificationError):
            return False

    def needs_rehash(self, hash: str) -> bool:
        return self.__internal_hasher.check_needs_rehash(hash)
