import os
from pathlib import Path
from typing import Any


def _file_exists(year: int, day: int, part: int, sub_part: str = "") -> bool:
    file_path: Path = (
        Path(os.environ["SUGARPLUM_BASE_PATH"])
        / f"{year}/{day:02}/test-{part}{sub_part}.in"
    )

    return file_path.exists()


def _read_file(file_path: str, cast_to: Any = str) -> Any:
    with open(os.environ["SUGARPLUM_BASE_PATH"] + "/" + file_path) as f:
        return cast_to(f.read())


def get_input(year: int, day: int) -> str:
    return _read_file(f"{year}/{day:02}/data.in")


def _get_single_test_data(
    year: int, day: int, part: int, cast_to: Any
) -> tuple[str, Any]:
    input_data: str = _read_file(f"{year}/{day:02}/test-{part}.in")
    result: Any = _read_file(f"{year}/{day:02}/test-{part}.out")

    return (input_data, cast_to(result))


def _get_multiple_test_data(year, day, part, cast_to: Any) -> list[tuple[str, Any]]:
    sub_part: str = "a"
    test_data: list[tuple[str, Any]] = []
    while _file_exists(year, day, part, sub_part):
        test_data.append(
            (
                _read_file(f"{year}/{day:02}/test-{part}{sub_part}.in"),
                cast_to(_read_file(f"{year}/{day:02}/test-{part}{sub_part}.out")),
            )
        )
        sub_part = chr(ord(sub_part) + 1)

    return test_data


def get_test_data(
    year: int, day: int, part: int, cast_to: Any = str
) -> tuple[str, Any] | list[tuple[str, Any]]:
    if _file_exists(year, day, part):
        return _get_single_test_data(year, day, part, cast_to)
    else:
        return _get_multiple_test_data(year, day, part, cast_to)
