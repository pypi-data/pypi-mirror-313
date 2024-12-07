from pathlib import Path
from typing import Callable

import pytest

from sugarplum import get_input, get_test_data

YEAR: int = 2023
DAY: int = 24


@pytest.fixture(autouse=True)
def base_path(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SUGARPLUM_BASE_PATH", str(tmp_path))


@pytest.fixture(autouse=True)
def setup_dirs(tmp_path: Path) -> None:
    (tmp_path / str(YEAR)).mkdir()
    (tmp_path / f"{YEAR}/{DAY}").mkdir()


@pytest.fixture
def create_files(tmp_path: Path) -> Callable:
    def _create_files(data: list[tuple[str, str]]) -> None:
        for entry in data:
            with open(tmp_path / f"{YEAR}/{DAY}/{entry[0]}", "w") as f:
                f.write(entry[1])

    return _create_files


def create_file(path: Path, data: str) -> None:
    with open(path, "w") as f:
        f.write(data)


def test_puzzle_input_data_is_read(tmp_path: Path, create_files: Callable) -> None:
    expected: str = "North Pole"
    create_files([("data.in", expected)])

    assert get_input(YEAR, DAY) == expected


def test_puzzle_day_number_gets_zero_padded(tmp_path: Path) -> None:
    expected: str = "sleigh"
    day: int = 3
    dir_path: Path = tmp_path / f"{YEAR}/{day:02}"
    dir_path.mkdir()
    (tmp_path / f"{YEAR}/{day:02}/data.in").write_text(expected, encoding="utf-8")

    assert get_input(YEAR, day) == expected


def test_get_test_data_retrieves_input_and_output_data_for_single_test_case(
    tmp_path: Path, create_files: Callable
) -> None:
    expected_input: str = "Christmas"
    expected_output: str = "Tree"
    create_files([("test-1.in", expected_input), ("test-1.out", expected_output)])

    assert get_test_data(YEAR, DAY, 1) == (expected_input, expected_output)


def test_get_test_data_retrieves_multiple_input_and_output_data_for_multiple_test_cases(
    tmp_path: Path, create_files: Callable
) -> None:
    expected_input_a: str = "Santa"
    expected_output_a: str = "Clause"
    expected_input_b: str = "Kris"
    expected_output_b: str = "Kringle"
    create_files(
        [
            ("test-1a.in", expected_input_a),
            ("test-1a.out", expected_output_a),
            ("test-1b.in", expected_input_b),
            ("test-1b.out", expected_output_b),
        ]
    )

    assert get_test_data(YEAR, DAY, 1) == [
        (expected_input_a, expected_output_a),
        (expected_input_b, expected_output_b),
    ]


def test_get_test_data_cast_type_defaults_to_string_when_not_specified(
    create_files: Callable,
) -> None:
    data: str = "Santa"
    create_files([("test-1.in", ""), ("test-1.out", data)])

    result = get_test_data(YEAR, DAY, 1)

    assert type(result[1]) is str


def test_get_test_data_casts_for_single_test_data(create_files: Callable) -> None:
    expected: int = 42
    create_files([("test-1.in", ""), ("test-1.out", str(expected))])

    data, result = get_test_data(YEAR, DAY, 1, cast_to=int)

    assert type(result) is int


def test_get_test_data_casts_for_multiple_test_data(create_files: Callable) -> None:
    expected_a: int = 24
    expected_b: int = 25
    create_files(
        [
            ("test-1a.in", ""),
            ("test-1a.out", str(expected_a)),
            ("test-1b.in", ""),
            ("test-1b.out", str(expected_b)),
        ]
    )

    results = get_test_data(YEAR, DAY, 1, cast_to=int)

    assert type(results[0][1]) is int and type(results[1][1]) is int
