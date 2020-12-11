from __future__ import annotations

from copy import deepcopy
from typing import List, Optional

EMPTY_SEAT = "L"
OCCUPIED_SEAT = "#"
FLOOR = "."


class SeatTransitionRule:
    def determine_next_state(self, grid: SeatingGrid, x: int, y: int) -> str:
        raise NotImplementedError()


class AdjacentSeatTransitionRule(SeatTransitionRule):
    def determine_next_state(self, grid: SeatingGrid, x: int, y: int) -> str:
        cell = grid.get_cell(x, y)
        if cell == FLOOR:
            return FLOOR

        adjacent_occupied_seat_count = AdjacentSeatTransitionRule._count_adjacent_occupied_seats(grid, x, y)
        if cell == EMPTY_SEAT and adjacent_occupied_seat_count == 0:
            return OCCUPIED_SEAT
        elif cell == OCCUPIED_SEAT and adjacent_occupied_seat_count >= 4:
            return EMPTY_SEAT

        return cell

    @staticmethod
    def _count_adjacent_occupied_seats(grid: SeatingGrid, x: int, y: int) -> int:
        adjacent_spaces = [
            grid.get_cell(x - 1, y - 1),
            grid.get_cell(x, y - 1),
            grid.get_cell(x + 1, y - 1),
            grid.get_cell(x - 1, y),
            grid.get_cell(x + 1, y),
            grid.get_cell(x - 1, y + 1),
            grid.get_cell(x, y + 1),
            grid.get_cell(x + 1, y + 1)
        ]

        # Filter down to only the spaces that are occupied and return the length
        return len(list(filter(lambda space: space == OCCUPIED_SEAT, adjacent_spaces)))


class FirstInSightSeatTransitionRule(SeatTransitionRule):
    def determine_next_state(self, grid: SeatingGrid, x: int, y: int) -> str:
        cell = grid.get_cell(x, y)
        if cell == FLOOR:
            return FLOOR

        diagonal_occupied_seat_count = FirstInSightSeatTransitionRule._count_first_in_sight_occupied_seats(grid, x, y)
        if cell == EMPTY_SEAT and diagonal_occupied_seat_count == 0:
            return OCCUPIED_SEAT
        elif cell == OCCUPIED_SEAT and diagonal_occupied_seat_count >= 5:
            return EMPTY_SEAT

        return cell

    @staticmethod
    def _count_first_in_sight_occupied_seats(grid: SeatingGrid, x: int, y: int) -> int:
        first_seats_in_sight = [
            FirstInSightSeatTransitionRule._find_first_seat_in_sight(grid, x - 1, y - 1, -1, -1),
            FirstInSightSeatTransitionRule._find_first_seat_in_sight(grid, x, y - 1, 0, -1),
            FirstInSightSeatTransitionRule._find_first_seat_in_sight(grid, x + 1, y - 1, 1, -1),
            FirstInSightSeatTransitionRule._find_first_seat_in_sight(grid, x - 1, y, -1, 0),
            FirstInSightSeatTransitionRule._find_first_seat_in_sight(grid, x + 1, y, 1, 0),
            FirstInSightSeatTransitionRule._find_first_seat_in_sight(grid, x - 1, y + 1, -1, 1),
            FirstInSightSeatTransitionRule._find_first_seat_in_sight(grid, x, y + 1, 0, 1),
            FirstInSightSeatTransitionRule._find_first_seat_in_sight(grid, x + 1, y + 1, 1, 1),
        ]

        # Filter down to only the spaces that are occupied and return the length
        return len(list(filter(lambda space: space == OCCUPIED_SEAT, first_seats_in_sight)))

    @staticmethod
    def _find_first_seat_in_sight(grid: SeatingGrid, x: int, y: int, x_dir: int, y_dir: int) -> str:
        cell = grid.get_cell(x, y)
        if cell != FLOOR:
            return cell

        return FirstInSightSeatTransitionRule._find_first_seat_in_sight(grid, x + x_dir, y + y_dir, x_dir, y_dir)


class SeatingGrid:
    def __init__(self, grid: List[List[str]]):
        if not SeatingGrid._validate_grid(grid):
            raise ValueError()

        self.grid = grid

    def __str__(self):
        return "\n".join(["".join([cell for cell in row]) for row in self.grid])

    def get_height(self) -> int:
        return len(self.grid)

    def get_width(self) -> int:
        return len(self.grid[0])

    @staticmethod
    def _validate_grid(grid: List[List[str]]) -> bool:
        if len(grid) < 1:
            return False

        width = len(grid[0])
        if width < 1:
            return False

        for row in grid:
            if len(row) != width:
                return False

            for cell in row:
                if cell not in [EMPTY_SEAT, OCCUPIED_SEAT, FLOOR]:
                    return False

        return True

    def get_cell(self, x: int, y: int) -> Optional[str]:
        """
        Safely tries to access a grid cell. If it doesn't exist return None
        """
        if x < 0 or x >= self.get_width() or y < 0 or y >= self.get_height():
            return None

        return self.grid[y][x]

    def apply_rule(self, rule: SeatTransitionRule) -> int:
        """
        Applies a rule to transform the grid. Returns the number of changes made
        """
        change_count = 0
        working_grid = deepcopy(self.grid)
        for y in range(self.get_height()):
            for x in range(self.get_width()):
                state = self.get_cell(x, y)
                next_state = rule.determine_next_state(self, x, y)

                working_grid[y][x] = next_state
                if state != next_state:
                    change_count += 1

        self.grid = working_grid

        return change_count

    def count_occupied_seats(self) -> int:
        count = 0
        for row in self.grid:
            for cell in row:
                count += int(cell == OCCUPIED_SEAT)

        return count

    def count_occupied_seats_at_equilibrium(self, rule: SeatTransitionRule) -> int:
        """
        Apply the rules continuously until an equilibrium is met and return the number of occupied seats
        """
        # Continuously apply the rules until an equilibrium is reached
        while self.apply_rule(rule) != 0:
            pass

        return self.count_occupied_seats()


def parse_input_file() -> List[List[str]]:
    with open("/app/advent2020/inputs/seating_system.txt", "r") as input_file:
        return [[char for char in line.strip()] for line in input_file.readlines()]


if __name__ == "__main__":
    input_data = parse_input_file()
    grid_one = SeatingGrid(input_data)
    grid_two = SeatingGrid(input_data)

    print("(Immediately Adjacent Rule) Occupied Seats at Equilibrium:",
          grid_one.count_occupied_seats_at_equilibrium(AdjacentSeatTransitionRule()))
    print("(First In Sight Rule) Occupied Seats at Equilibrium:",
          grid_two.count_occupied_seats_at_equilibrium(FirstInSightSeatTransitionRule()))
