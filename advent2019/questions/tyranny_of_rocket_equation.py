from typing import List


def calculate_fuel_for_module_mass(module_mass: int) -> int:
    fuel = (module_mass // 3) - 2
    return max([fuel, 0])


def calculate_cumulative_fuel_needed_for_module_masses(module_masses: List[int]) -> int:
    return sum([calculate_fuel_for_module_mass(module_mass) for module_mass in module_masses])


def calculate_fuel_needed_for_mass_after_adding_fuel_mass(mass: int) -> int:
    fuel = calculate_fuel_for_module_mass(mass)
    additional_fuel = fuel

    while True:
        additional_fuel = calculate_fuel_for_module_mass(additional_fuel)
        if additional_fuel < 1:
            return fuel

        fuel += additional_fuel


def calculate_fuel_needed_all_masses_after_adding_fuel_mass(masses: List[int]) -> int:
    return sum([calculate_fuel_needed_for_mass_after_adding_fuel_mass(mass) for mass in masses])


def parse_input_file() -> List[int]:
    """
    :return: All the module masses in the file as integers
    """
    with open("/app/advent2019/inputs/tyranny_of_rocket_equation.txt", "r") as input_file:
        return [int(line) for line in input_file]


if __name__ == "__main__":
    module_masses = parse_input_file()
    fuel_needed_for_mass = calculate_cumulative_fuel_needed_for_module_masses(module_masses)
    fuel_needed_for_mass_and_fuel = calculate_fuel_needed_all_masses_after_adding_fuel_mass(module_masses)

    print("Total Fuel Needed (module masses only):", fuel_needed_for_mass)
    print("Total Fuel Needed (accounting for mass of fuel):", fuel_needed_for_mass_and_fuel)
