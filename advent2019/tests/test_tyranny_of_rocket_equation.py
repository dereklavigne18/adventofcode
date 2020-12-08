from typing import Tuple, List

import pytest

from advent2019.questions.tyranny_of_rocket_equation import (
    calculate_fuel_for_module_mass,
    calculate_cumulative_fuel_needed_for_module_masses,
    calculate_fuel_needed_for_mass_after_adding_fuel_mass,
    calculate_fuel_needed_all_masses_after_adding_fuel_mass
)


# Subject: calculate_fuel_for_module_mass
def calculate_fuel_for_module_mass_provider() -> List[Tuple[int, int]]:
    """
    :return: The test input and expected results (module_mass, expected)
    """
    return [
        (12, 2),
        (14, 2),
        (1969, 654),
        (100756, 33583),
        (9, 1),
        (8, 0),
        (6, 0),
        (5, 0),
        (3, 0),
        (2, 0),
        (0, 0),
        (-1, 0)
    ]


@pytest.mark.parametrize("module_mass,expected", calculate_fuel_for_module_mass_provider())
def test__calculate_fuel_for_module_mass__happy_path(module_mass, expected):
    assert calculate_fuel_for_module_mass(module_mass) == expected


# Subject: calculate_cumulative_fuel_needed_for_module_masses
def calculate_cumulative_fuel_needed_for_module_masses_provider() -> List[Tuple[List[int], int]]:
    return [
        ([12, 14, -1, 1969, 100756, 9, 4], 34242)
    ]


@pytest.mark.parametrize("module_masses,expected", calculate_cumulative_fuel_needed_for_module_masses_provider())
def test__calculate_cumulative_fuel_needed_for_module_masses__happy_path(module_masses, expected):
    assert calculate_cumulative_fuel_needed_for_module_masses(module_masses) == expected


# Subject: calculate_fuel_needed_for_mass_after_adding_fuel_mass
def calculate_fuel_needed_for_mass_after_adding_fuel_mass_provider() -> List[Tuple[int, int]]:
    """
    :return: The test input and expected results (module_mass, expected)
    """
    return [
        (14, 2),
        (1969, 966),
        (100756, 50346)
    ]


@pytest.mark.parametrize("mass,expected", calculate_fuel_needed_for_mass_after_adding_fuel_mass_provider())
def test__calculate_fuel_needed_for_mass_after_adding_fuel_mass__happy_path(mass, expected):
    assert calculate_fuel_needed_for_mass_after_adding_fuel_mass(mass) == expected


# Subject: calculate_fuel_needed_all_masses_after_adding_fuel_mass
def calculate_fuel_needed_all_masses_after_adding_fuel_mass_provider() -> List[Tuple[List[int], int]]:
    return [
        ([14, 1969, 100756], 51314)
    ]


@pytest.mark.parametrize("masses,expected", calculate_fuel_needed_all_masses_after_adding_fuel_mass_provider())
def test__calculate_fuel_needed_all_masses_after_adding_fuel_mass__happy_path(masses, expected):
    assert calculate_fuel_needed_all_masses_after_adding_fuel_mass(masses) == expected
