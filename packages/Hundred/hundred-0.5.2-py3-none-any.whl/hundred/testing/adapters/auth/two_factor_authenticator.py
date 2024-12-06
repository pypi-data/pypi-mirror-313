from uuid import UUID

from injection.testing import test_singleton

from hundred.ctx.auth.ports import TwoFactorAuthenticator


@test_singleton(on=TwoFactorAuthenticator, inject=False, mode="fallback")
class FakeTwoFactorAuthenticator(TwoFactorAuthenticator):
    __slots__ = ()

    async def send_code(self, user_id: UUID, code: str) -> None:
        return
