from typing import List, Tuple, Optional

import pytest

from advent2020.questions.shuttle_search import (
    find_next_bus_after_timestamp,
    find_timestamp_where_departure_sequence_is_met
)


# Subject: find_next_bus_after_timestamp
def find_next_bus_after_timestamp_provider() -> List[Tuple[int, List[str], Optional[Tuple[int, int]]]]:
    return [
        (  # Question Example
            939,
            ["7", "13", "x", "x", "59", "x", "31", "19"],
            (59, 5)
        ),
        (  # All Xes
            939,
            ["x", "x", "x", "x"],
            None
        ),
        (  # Multiple buses at the same time (return first)
            10,
            ["4", "x", "5", "2", "6"],
            (5, 0)
        ),
        (
            10,
            [],
            None
        )
    ]


@pytest.mark.parametrize("timestamp,buses,expected", find_next_bus_after_timestamp_provider())
def test__find_next_bus_after_timestamp__happy_path(timestamp, buses, expected):
    assert find_next_bus_after_timestamp(timestamp, buses) == expected


def test__find_next_bus_after_timestamp__raises_ValueError_when_invalid_bus_id_provided():
    # Invalid "a"
    buses = ["4", "x", "3", "a"]

    with pytest.raises(ValueError):
        find_next_bus_after_timestamp(8, buses)


# Subject: find_timestamp_where_departure_sequence_is_met
def find_timestamp_where_departure_sequence_is_met_provider() -> List[Tuple[List[str], Optional[int]]]:
    return [
        (
            ["7", "13", "x", "x", "59", "x", "31", "19"],
            1068781
        ),
        (
            ["17", "x", "13", "19"],
            3417
        ),
        (
            ["67", "7", "59", "61"],
            754018
        ),
        (
            ["67", "x", "7", "59", "61"],
            779210
        ),
        (
            ["67", "7", "x", "59", "61"],
            1261476
        ),
        (
            ["1789", "37", "47", "1889"],
            1202161486
        ),
        (
            [],
            None
        ),
        (
            ["x", "x", "x", "x"],
            None
        ),
        (
            ["x", "5", "3", "4"],
            11
        )
    ]


@pytest.mark.parametrize("departure_sequence,expected", find_timestamp_where_departure_sequence_is_met_provider())
def test__find_timestamp_where_departure_sequence_is_met__happy_path(departure_sequence, expected):
    assert find_timestamp_where_departure_sequence_is_met(departure_sequence) == expected


def test__find_timestamp_where_departure_sequence_is_met_provider__raises_ValueError_when_invalid_bus_id_provided():
    # Invalid "a"
    buses = ["4", "x", "3", "a"]

    with pytest.raises(ValueError):
        find_timestamp_where_departure_sequence_is_met(buses)
