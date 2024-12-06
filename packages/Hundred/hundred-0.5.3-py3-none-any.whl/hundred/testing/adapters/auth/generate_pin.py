from typing import ClassVar

from injection.testing import test_singleton

from hundred.ctx.auth.ports import GeneratePinFunction


@test_singleton(on=GeneratePinFunction, inject=False, mode="fallback")
class FakeGeneratePinFunction(GeneratePinFunction):
    __slots__ = ()

    pin: ClassVar[str] = "123456"

    async def __call__(self, length: int = 6) -> str:
        return self.pin
