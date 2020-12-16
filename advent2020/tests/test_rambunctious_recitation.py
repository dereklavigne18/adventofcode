from typing import List, Tuple

import pytest

from advent2020.questions.rambunctious_recitation import calculate_answer_at_turn


def calculate_answer_at_turn_provider() -> List[Tuple[List[int], int, int]]:
    return [
        ([0, 3, 6], 2020, 436),
        # ([0, 3, 6], 30000000, 175594),
        # ([1, 3, 2], 30000000, 2578),
        # ([2, 1, 3], 30000000, 3544142),
        # ([1, 2, 3], 30000000, 261214),
        # ([2, 3, 1], 30000000, 6895259),
        # ([3, 2, 1], 30000000, 18),
        # ([3, 1, 2], 30000000, 362),
    ]


@pytest.mark.parametrize("start,turn_count, expected", calculate_answer_at_turn_provider())
def test__calculate_answer_at_turn__happy_path(start, turn_count, expected):
    assert calculate_answer_at_turn(start, turn_count) == expected
