import os
from abc import ABC
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import orjson

from hundred.testing.exceptions import FileComparisonError


class HundredTestCase(ABC):
    __slots__ = ()

    __temporary_dir = TemporaryDirectory()

    @classmethod
    def assert_results_match(cls, current_result: dict[str, Any]) -> None:
        current_json_result = orjson.dumps(
            current_result,
            default=str,
            option=orjson.OPT_INDENT_2,
        )
        results_dir = cls.__get_results_dir()
        os.makedirs(results_dir, exist_ok=True)

        filename = f"{cls.__get_current_test_name()}.json"
        result_file = results_dir / filename
        previous_json_result = cls.__load_result(result_file)

        try:
            assert current_json_result == previous_json_result

        except AssertionError as exc:
            temporary_file = cls.__get_temporary_dir() / filename
            cls.__dump_result(temporary_file, current_json_result)
            raise FileComparisonError(temporary_file, result_file) from exc

    @classmethod
    def __get_temporary_dir(cls) -> Path:
        return Path(cls.__temporary_dir.name)

    @classmethod
    def __get_results_dir(cls) -> Path:
        results_dir = Path(os.environ["PYTEST_HUNDRED_DIR"]) / "results"
        subdirectories = *cls.__module__.split("."), cls.__name__

        for subdirectory in subdirectories:
            results_dir /= subdirectory

        return results_dir

    @staticmethod
    def __get_current_test_name() -> str:
        name = os.environ["PYTEST_CURRENT_TEST"]
        return name.split(":")[-1].split(" ")[0]

    @staticmethod
    def __dump_result(filepath: Path, result: bytes) -> None:
        with open(filepath, "wb") as writer:
            writer.write(result)

    @staticmethod
    def __load_result(filepath: Path) -> bytes:
        with open(filepath, "ab+") as reader:
            reader.seek(0)
            return reader.read()
