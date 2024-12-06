from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import Field, SecretStr, field_serializer

from hundred import Aggregate
from hundred.ctx.auth.domain.check_code import CheckCode
from hundred.ctx.auth.domain.session_status import SessionStatus
from hundred.ctx.auth.domain.user import User


class Session(Aggregate):
    application_id: UUID
    created_at: datetime
    last_seen: datetime
    token: SecretStr | None = Field(default=None)
    status: SessionStatus = Field(default=SessionStatus.UNVERIFIED)
    check_code: CheckCode | None = Field(default=None)
    user: User = Field(frozen=True)

    @field_serializer("token")
    def __token_serializer(self, value: SecretStr | None) -> str | None:
        if value is None:
            return None

        return value.get_secret_value()

    @property
    def check_code_id(self) -> UUID | None:
        if check_code := self.check_code:
            return check_code.id

        return None

    @property
    def is_verified(self) -> bool:
        return self.status == SessionStatus.VERIFIED

    @property
    def is_unverified(self) -> bool:
        return self.status == SessionStatus.UNVERIFIED

    @property
    def is_temporary(self) -> bool:
        return self.token is None

    @property
    def raw_token(self) -> str | None:
        if token := self.token:
            return token.get_secret_value()

        return None

    def is_owner(self, user_id: UUID) -> bool:
        return self.user.id == user_id

    def verify(self) -> Self:
        self.status = SessionStatus.VERIFIED
        return self
