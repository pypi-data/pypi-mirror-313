from uuid import UUID

from pydantic import Field, SecretStr, field_serializer

from hundred import Aggregate
from hundred.ctx.auth.domain.user_status import UserStatus
from hundred.gettext import gettext as _


class User(Aggregate):
    password: SecretStr | None = Field(default=None)
    status: UserStatus = Field(default=UserStatus.ACTIVE)

    @field_serializer("password")
    def __password_serializer(self, value: SecretStr | None) -> str | None:
        if value is None:
            return None

        return value.get_secret_value()

    @property
    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE

    @property
    def readable(self) -> str:
        return self.to_readable(self.id)

    @property
    def raw_password(self) -> str | None:
        if password := self.password:
            return password.get_secret_value()

        return None

    @staticmethod
    def to_readable(user_id: UUID) -> str:
        return _("user").format(user_id=user_id)
