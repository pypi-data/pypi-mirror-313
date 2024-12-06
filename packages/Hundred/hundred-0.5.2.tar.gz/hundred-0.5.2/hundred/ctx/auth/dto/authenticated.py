from cq import DTO
from pydantic import Field, SecretStr, field_serializer


class Authenticated(DTO):
    access_token: SecretStr
    session_token: SecretStr | None = Field(default=None)

    @field_serializer("access_token")
    def __access_token_serializer(self, value: SecretStr) -> str:
        return value.get_secret_value()

    @field_serializer("session_token")
    def __session_token_serializer(self, value: SecretStr | None) -> str | None:
        if value is None:
            return None

        return value.get_secret_value()
