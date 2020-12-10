from typing import List, Tuple

import pytest

from advent2020.questions.adapter_array import (
    count_jolt_adaptations,
    count_working_adapter_sequences,
    organize_adapters
)


# Subject: count_jolt_adaptations
def count_jolt_adaptations_happy_path_provider() -> List[Tuple[List[int], Tuple[int, int, int]]]:
    return [
        (
            [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4],
            (7, 0, 5)
        ),
        (
            [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2,
             34, 10, 3],
            (22, 0, 10)
        ),
        (
            [2],
            (0, 1, 1)
        ),
    ]


@pytest.mark.parametrize("adapter_ratings,expected", count_jolt_adaptations_happy_path_provider())
def test__count_jolt_adaptations__happy_path(adapter_ratings: List[int], expected: List[int]):
    assert count_jolt_adaptations(organize_adapters(adapter_ratings)) == expected


def count_jolt_adaptations_invalid_input_provider() -> List[List[int]]:
    return [
        [],
        [3, 7, 1, 9]
    ]


@pytest.mark.parametrize("adapter_ratings", count_jolt_adaptations_invalid_input_provider())
def test__count_jolt_adaptations__raises_ValueError_when_provided_invalid_input(adapter_ratings: List[int]):
    with pytest.raises(ValueError):
        count_jolt_adaptations(organize_adapters(adapter_ratings))


# Subject: count_working_adapter_sequences
def count_working_adapter_sequences_provider() -> List[Tuple[List[int], int]]:
    return [
        (
            [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4],
            8
        ),
        (
            [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2,
             34, 10, 3],
            19208
        )
    ]


@pytest.mark.parametrize("adapter_ratings,expected", count_working_adapter_sequences_provider())
def test__count_working_adapter_sequences__happy_path(adapter_ratings: List[int], expected: int):
    assert count_working_adapter_sequences(organize_adapters(adapter_ratings)) == expected


def test__count_working_adapter_sequences__raises_ValueError_when_no_ratings_provided():
    with pytest.raises(ValueError):
        count_working_adapter_sequences([])
