from pathlib import Path

from hundred.exceptions import HundredError


class ComparisonError[T](AssertionError, HundredError):
    __slots__ = ("current", "previous")

    def __init__(self, current: T, previous: T) -> None:
        self.current = current
        self.previous = previous

    def __str__(self) -> str:
        return (
            "Data mismatch\n"
            f"・Current: `{self.current}`\n"
            f"・Previous: `{self.previous}`"
        )


class FileComparisonError(ComparisonError[Path]): ...
