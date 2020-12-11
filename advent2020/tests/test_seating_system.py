import pytest

from advent2020.questions.seating_system import (
    SeatingGrid,
    SeatTransitionRule,
    AdjacentSeatTransitionRule,
    FirstInSightSeatTransitionRule,
)

"""
Subject: SeatTransitionRule.determine_next_state
"""
def test__SeatTransitionRule_determine_next_state__raises_NotImplementedError():
    with pytest.raises(NotImplementedError):
        grid = SeatingGrid([["."]])
        SeatTransitionRule().determine_next_state(grid, 0, 0)


"""
Subject: AdjacentSeatTransitionRule.determine_next_state
"""
def test__AdjacentSeatTransitionRule_determine_next_state__happy_path():
    grid = SeatingGrid([
        ["L", "#", ".", "L"],
        ["L", "#", ".", "L"],
        ["#", "#", "#", "."],
        ["L", "L", ".", "L"],
        ["L", "L", ".", "L"],
    ])

    rule = AdjacentSeatTransitionRule()

    # Check that an empty seat with an adjacent occupied seat doesn't become occupied
    assert rule.determine_next_state(grid, 0, 0) == "L"
    assert rule.determine_next_state(grid, 0, 1) == "L"
    assert rule.determine_next_state(grid, 3, 1) == "L"
    assert rule.determine_next_state(grid, 0, 3) == "L"
    assert rule.determine_next_state(grid, 1, 3) == "L"
    assert rule.determine_next_state(grid, 3, 3) == "L"
    # Check that an empty seat with no adjacent occupied seats becomes occupied
    assert rule.determine_next_state(grid, 3, 0) == "#"
    assert rule.determine_next_state(grid, 0, 4) == "#"
    assert rule.determine_next_state(grid, 1, 4) == "#"
    assert rule.determine_next_state(grid, 3, 4) == "#"
    # Check that occupied seats with less than 4 adjacent occupied seats stay occupied
    assert rule.determine_next_state(grid, 1, 0) == "#"
    assert rule.determine_next_state(grid, 0, 2) == "#"
    assert rule.determine_next_state(grid, 1, 2) == "#"
    assert rule.determine_next_state(grid, 2, 2) == "#"
    # Check that occupied seats with 4 adjacent occupied seats are evacuated
    assert rule.determine_next_state(grid, 1, 1) == "L"
    # Check that floor spaces don't change
    assert rule.determine_next_state(grid, 2, 0) == "."
    assert rule.determine_next_state(grid, 2, 1) == "."
    assert rule.determine_next_state(grid, 3, 2) == "."
    assert rule.determine_next_state(grid, 2, 3) == "."
    assert rule.determine_next_state(grid, 2, 4) == "."


"""
Subject: FirstInSightSeatTransitionRule.determine_next_state
"""
def test__FirstInSightSeatTransitionRule_determine_next_state__happy_path():
    grid = SeatingGrid([
        ["L", "L", ".", "L"],
        ["L", "L", ".", "#"],
        ["#", ".", "#", "."],
        ["L", ".", ".", "#"],
        ["#", "L", "#", "L"],
    ])

    rule = FirstInSightSeatTransitionRule()

    # Check that empty seats with occupied seats in sight stay empty
    assert rule.determine_next_state(grid, 3, 0) == "L"
    assert rule.determine_next_state(grid, 0, 1) == "L"
    assert rule.determine_next_state(grid, 1, 1) == "L"
    assert rule.determine_next_state(grid, 0, 3) == "L"
    assert rule.determine_next_state(grid, 1, 4) == "L"
    assert rule.determine_next_state(grid, 3, 4) == "L"

    # Check that empty seats without occupied seats in sight become occupied
    assert rule.determine_next_state(grid, 0, 0) == "#"
    assert rule.determine_next_state(grid, 1, 0) == "#"

    # Check that occupied seats with less than five occupied seats in sight stay occupied
    assert rule.determine_next_state(grid, 3, 1) == "#"
    assert rule.determine_next_state(grid, 0, 2) == "#"
    assert rule.determine_next_state(grid, 3, 3) == "#"
    assert rule.determine_next_state(grid, 0, 4) == "#"
    assert rule.determine_next_state(grid, 2, 4) == "#"

    # Check that occupied seats with five occupied seats in sight are evacuated
    assert rule.determine_next_state(grid, 2, 2) == "L"

    # Check that floor spaces remain floor spaces
    assert rule.determine_next_state(grid, 2, 0) == "."
    assert rule.determine_next_state(grid, 2, 1) == "."
    assert rule.determine_next_state(grid, 1, 2) == "."
    assert rule.determine_next_state(grid, 3, 2) == "."
    assert rule.determine_next_state(grid, 1, 3) == "."
    assert rule.determine_next_state(grid, 2, 3) == "."


"""
Subject: SeatingGrid.count_occupied_seats
"""
def test__SeatingGrid_count_occupied_seats():
    grid = SeatingGrid([
        ["L", "L", ".", "L"],
        ["L", "L", ".", "#"],
        ["#", ".", "#", "."],
        ["L", ".", ".", "#"],
        ["#", "L", "#", "L"],
    ])

    assert grid.count_occupied_seats() == 6


"""
Subject: SeatingGrid.apply_rule
"""
def test__SeatingGrid_apply_rule():
    grid = SeatingGrid([
        ["L", "#", ".", "L"],
        ["L", "#", ".", "L"],
        ["#", "#", "#", "."],
        ["L", "L", ".", "L"],
        ["L", "L", ".", "L"],
    ])
    # grid.apply_rule(AdjacentSeatTransitionRule())

    assert grid.apply_rule(AdjacentSeatTransitionRule()) == 5
    assert grid.grid == [
        ["L", "#", ".", "#"],
        ["L", "L", ".", "L"],
        ["#", "#", "#", "."],
        ["L", "L", ".", "L"],
        ["#", "#", ".", "#"],
    ]


"""
Subject: SeatingGrid.count_occupied_seats_at_equilibrium
"""
def test__SeatingGrid_count_occupied_seats_at_equilibrium():
    grid = SeatingGrid([
        ["L", ".", "L", "L", ".", "L", "L", ".", "L", "L"],
        ["L", "L", "L", "L", "L", "L", "L", ".", "L", "L"],
        ["L", ".", "L", ".", "L", ".", ".", "L", ".", "."],
        ["L", "L", "L", "L", ".", "L", "L", ".", "L", "L"],
        ["L", ".", "L", "L", ".", "L", "L", ".", "L", "L"],
        ["L", ".", "L", "L", "L", "L", "L", ".", "L", "L"],
        [".", ".", "L", ".", "L", ".", ".", ".", ".", "."],
        ["L", "L", "L", "L", "L", "L", "L", "L", "L", "L"],
        ["L", ".", "L", "L", "L", "L", "L", "L", ".", "L"],
        ["L", ".", "L", "L", "L", "L", "L", ".", "L", "L"],
    ])

    assert grid.count_occupied_seats_at_equilibrium(AdjacentSeatTransitionRule()) == 37
