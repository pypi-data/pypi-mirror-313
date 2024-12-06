import os
import shutil
import time
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self

from cq import (
    CommandBus,
    EventBus,
    QueryBus,
    get_command_bus,
    get_event_bus,
    get_query_bus,
)
from injection import find_instance
from pytest import CallInfo, Collector, Config, FixtureRequest, Item, Parser, fixture

from hundred.services.datetime import DateTimeService
from hundred.services.uuid import UUIDGenerator
from hundred.testing.exceptions import FileComparisonError

__all__ = ()


def pytest_addoption(parser: Parser) -> None:
    diff_help = "Command line to open an interactive comparison. Example: `code -w -d {current} {reference}`."
    group = parser.getgroup("hundred")
    group.addoption(
        "--accept-all-diff",
        dest="accept_all_diff",
        action="store_true",
        help="Parameter for accepting new differences between results.",
        default=False,
    )
    group.addoption(
        "--diff",
        dest="diff",
        metavar="COMMAND_LINE",
        help=diff_help,
        default=None,
    )
    parser.addini(
        "diff",
        type="string",
        help=diff_help,
        default=None,
    )


def pytest_exception_interact(node: Item | Collector, call: CallInfo[Any]) -> None:
    from hundred.testing.exceptions import FileComparisonError

    exception = info.value if (info := call.excinfo) else None

    if not isinstance(exception, FileComparisonError):
        return

    diff = Diff.from_file_comparison_error(exception)
    config = HundredConfig(node.config)

    if config.accept_all_diff:
        diff.accept()

    elif command := config.diff_command:
        diff.show(command)


@fixture(scope="session", autouse=True)
def hundred_dir(request: FixtureRequest) -> Iterator[Path]:
    path = request.config.rootpath / "__pytest_hundred__"
    name = "PYTEST_HUNDRED_DIR"
    os.environ[name] = str(path)
    yield path
    del os.environ[name]


@fixture(scope="session")
def command_bus[T]() -> CommandBus[T]:
    return get_command_bus()


@fixture(scope="session")
def query_bus[T]() -> QueryBus[T]:
    return get_query_bus()


@fixture(scope="session")
def event_bus() -> EventBus:
    return get_event_bus()


@fixture(scope="function")
def datetime_service() -> DateTimeService:
    return find_instance(DateTimeService)


@fixture(scope="function")
def uuid_gen() -> UUIDGenerator:
    return find_instance(UUIDGenerator)


class HundredConfig:
    __slots__ = ("__config",)

    def __init__(self, pytest_config: Config) -> None:
        self.__config = pytest_config

    @property
    def accept_all_diff(self) -> bool:
        return self.__config.getoption("accept_all_diff")

    @property
    def diff_command(self) -> str | None:
        key = "diff"
        value = self.__config.getoption(key)

        if value is None:
            return self.__config.getini(key)

        return value


@dataclass(frozen=True, kw_only=True, slots=True)
class Diff:
    current_file: Path
    reference_file: Path

    def accept(self) -> None:
        shutil.copyfile(self.current_file, self.reference_file)

    def show(self, command: str) -> None:
        command = command.format(
            current=self.current_file,
            reference=self.reference_file,
        )
        os.system(command)
        time.sleep(1)

    @classmethod
    def from_file_comparison_error(cls, error: FileComparisonError) -> Self:
        return cls(
            current_file=error.current,
            reference_file=error.previous,
        )
