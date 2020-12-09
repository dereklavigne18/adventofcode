from typing import List, Optional, Tuple

import pytest

from advent2020.questions.encoding_error import find_first_encoding_error, find_contiguous_set_summing_to_target


# Subject: find_first_encoding_error
def find_first_encoding_error_provider() -> List[Tuple[List[int], int, Optional[int]]]:
    return [
        (
            [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576],
            5,
            127
        ),
        (  # Make sure we're checking the first non-preamble value
            [35, 20, 15, 25, 47, 61, 40, 72],
            5,
            61
        ),
        (  # Make sure we're checking the last value
            [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 219, 375],
            5,
            375
        ),
        (  # None return when everything is correct
            [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 219],
            5,
            None
        )
    ]


@pytest.mark.parametrize("encoded_data,preamble_length,expected", find_first_encoding_error_provider())
def test__find_first_encoding_error__happy_path(encoded_data, preamble_length, expected):
    assert find_first_encoding_error(encoded_data, preamble_length) == expected


def test__find_first_encoding_error__raises_ValueError_when_encoded_not_longer_than_preamble():
    with pytest.raises(ValueError):
        find_first_encoding_error([1, 2, 3, 4, 5], 5)


# Subject: find_contiguous_set_summing_to_target
def find_contiguous_set_summing_to_target_provider() -> List[Tuple[List[int], int, Optional[List[int]]]]:
    return [
        (
            [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576],
            127,
            [15, 25, 47, 40]
        ),
        (  # Ignores single values equaling the sum
            [35, 20, 127, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 219, 299, 277, 309, 576],
            127,
            [15, 25, 47, 40]
        ),
        (
            [35, 20, 15, 25, 47, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576],
            127,
            None
        ),
    ]


@pytest.mark.parametrize("encoded_data,target_sum,expected", find_contiguous_set_summing_to_target_provider())
def test__find_contiguous_set_summing_to_target__happy_path(encoded_data, target_sum, expected):
    assert find_contiguous_set_summing_to_target(encoded_data, target_sum) == expected
