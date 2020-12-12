from typing import Dict, List, Tuple

import pytest

from advent2020.questions.rain_risk import (
    Ship,
    ShipWithBasicNavigation,
    ShipWithWaypointNavigation,
    NORTH, SOUTH, EAST, WEST
)

"""
Ship
"""


# Subject: Ship.calculate_mahattan_distance_from_origin
def Ship_calculate_manhattan_distance_from_origin_provider() -> List[Tuple[int, int, int]]:
    return [
        (  # Question example
            17,
            -8,
            25
        ),
        (
            17,
            8,
            25
        ),
        (
            -17,
            8,
            25
        ),
        (
            -17,
            -8,
            25
        ),
    ]


@pytest.mark.parametrize("x_pos,y_pos,expected", Ship_calculate_manhattan_distance_from_origin_provider())
def test__Ship_calculate_manhattan_distance_from_origin(x_pos, y_pos, expected):
    ship = Ship()

    ship._x_position = x_pos
    ship._y_position = y_pos
    assert ship.calculate_manhattan_distance_from_origin() == expected


"""
ShipWithBasicNavigation
"""


# Subject: ShipWithBasicNavigation.navigate_directions
def ShipWithBasicNavigation_navigate_directions_provider() -> List[Tuple[List[str], int, int]]:
    return [
        (  # Question example
            ["F10", "N3", "F7", "R90", "F11"],
            17,
            -8
        ),
        (
            ["F10", "N3", "F7", "R90", "F11", "R180", "F10", "W40", "R270", "F12", "E4", "S6"],
            -31,
            -4
        )
    ]


@pytest.mark.parametrize("directions,expected_x_pos,expected_y_pos", ShipWithBasicNavigation_navigate_directions_provider())
def test__ShipWithBasicNavigation_navigate_directions(directions, expected_x_pos, expected_y_pos):
    ship = ShipWithBasicNavigation()
    ship.navigate_directions(directions)

    assert ship._x_position == expected_x_pos
    assert ship._y_position == expected_y_pos


"""
ShipWithWaypointNavigation
"""


# Subject: ShipWithWaypointNavigation.navigate_directions
def ShipWithWaypointNavigation_navigate_directions_provider() -> List[Tuple[List[str], int, int]]:
    return [
        (  # Question example
            ["F10", "N3", "F7", "R90", "F11"],
            214,
            -72
        ),
        (
            ["F10", "N3", "F7", "R90", "F11", "R180", "F10", "W40", "R270", "F12", "E4", "S6"],
            54,
            -500
        )
    ]


@pytest.mark.parametrize("directions,expected_x_pos,expected_y_pos", ShipWithWaypointNavigation_navigate_directions_provider())
def test__ShipWithWaypointNavigation_navigate_directions(directions, expected_x_pos, expected_y_pos):
    ship = ShipWithWaypointNavigation()
    ship.navigate_directions(directions)

    assert ship._x_position == expected_x_pos
    assert ship._y_position == expected_y_pos
