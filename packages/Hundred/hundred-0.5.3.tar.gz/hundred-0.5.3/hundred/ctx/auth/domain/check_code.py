from datetime import datetime

from pydantic import SecretStr, field_serializer

from hundred import Entity


class CheckCode(Entity):
    value: SecretStr
    expiration: datetime

    @field_serializer("value")
    def __value_serializer(self, value: SecretStr) -> str:
        return value.get_secret_value()

    @property
    def raw_value(self) -> str:
        return self.value.get_secret_value()

    def has_expired(self, now: datetime) -> bool:
        return now >= self.expiration
