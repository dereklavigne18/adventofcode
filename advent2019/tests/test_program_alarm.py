from typing import List, Tuple

import pytest

from advent2019.questions.program_alarm import (
    execute_intcode,
    execute_intcode_with_noun_and_verb,
    find_noun_and_verb_for_intcode_result
)


# Subject: execute_intcode
def execute_intcode_provider() -> List[Tuple[List[int], List[int]]]:
    return [
        (
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
        ),
        (  # 1 + 1 = 2
            [1, 0, 0, 0, 99],
            [2, 0, 0, 0, 99],
        ),
        (  # 3 * 2 = 6
            [2, 3, 0, 3, 99],
            [2, 3, 0, 6, 99],
        ),
        (  # 99 * 99 = 9801
            [2, 4, 4, 5, 99, 0],
            [2, 4, 4, 5, 99, 9801],
        ),
        (
            [1, 1, 1, 4, 99, 5, 6, 0, 99],
            [30, 1, 1, 4, 2, 5, 6, 0, 99],
        ),
        (
            [2, 9, 10, 0, 2, 0, 9, 1, 99, 5, 6],
            [30, 150, 10, 0, 2, 0, 9, 1, 99, 5, 6]
        )
    ]


@pytest.mark.parametrize("intcode,expected", execute_intcode_provider())
def test__execute_intcode__happy_path(intcode: List[int], expected: List[int]):
    assert execute_intcode(intcode) == expected


def test__execute_intcode__raises_ValueError_on_bad_opcode():
    with pytest.raises(ValueError):
        execute_intcode([1, 0, 0, 1, 20, 0, 0, 2, 99])


# Subject: execute_intcode_with_noun_and_verb
def execute_intcode_with_noun_and_verb_provider() -> List[Tuple[List[int], int, int, List[int]]]:
    return [
        (
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
            5,
            8,
            [5100, 5, 8, 102, 2, 3, 11, 0, 99, 30, 40, 50],
        )
    ]


@pytest.mark.parametrize("intcode,noun,verb,expected", execute_intcode_with_noun_and_verb_provider())
def test__execute_intcode_with_noun_and_verb__happy_path(intcode, noun, verb, expected):
    assert execute_intcode_with_noun_and_verb(intcode, noun, verb) == expected


# Subject: find_noun_and_verb_for_intcode_result
def find_noun_and_verb_for_intcode_result_provider() -> List[Tuple[List[int], int, Tuple[int, int]]]:
    return [
        (
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
            5100,
            (5, 8)
        )
    ]


@pytest.mark.parametrize("intcode,result,noun_verb", find_noun_and_verb_for_intcode_result_provider())
def test__find_noun_and_verb_for_intcode_result__happy_path(intcode, result, noun_verb):
    assert find_noun_and_verb_for_intcode_result(intcode, result)
