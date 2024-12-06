from abc import ABC
from typing import Any, Self

from hundred.gettext import gettext as _


class HundredError(Exception, ABC): ...


class HundredStatusError(HundredError, ABC):
    __slots__ = ("status_code", "details")

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.details = details

    def dump(self) -> dict[str, Any]:
        if details := self.details:
            return details

        return {"message": str(self)}


class NotModified(HundredStatusError):
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=304)

    @classmethod
    def from_target(cls, target: str) -> Self:
        return cls(_("target_not_modified").format(target=target))


class Unauthorized(HundredStatusError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(
            message or _("unauthorized"),
            status_code=401,
        )


class Forbidden(HundredStatusError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(
            message or _("forbidden"),
            status_code=403,
        )


class NotFound(HundredStatusError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(
            message or _("not_found"),
            status_code=404,
        )

    @classmethod
    def from_target(cls, target: str) -> Self:
        return cls(_("target_not_found").format(target=target))


class Conflict(HundredStatusError):
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=409)

    @classmethod
    def from_target(cls, target: str) -> Self:
        return cls(_("target_conflict").format(target=target))


class Locked(HundredStatusError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(
            message or _("locked"),
            status_code=423,
        )
