from abc import abstractmethod
from typing import Protocol, runtime_checkable

from injection import should_be_injectable


@should_be_injectable
@runtime_checkable
class GeneratePinFunction(Protocol):
    __slots__ = ()

    @abstractmethod
    async def __call__(self, length: int = ...) -> str:
        raise NotImplementedError
