from typing import Dict, List


FORWARD = "F"

NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"

LEFT = "L"
RIGHT = "R"


class Ship:
    def __init__(self):
        # Always starts at 0 in all directions
        self._x_position = 0
        self._y_position = 0

    def _process_instruction(self, instruction: str, value: int) -> None:
        raise NotImplementedError()

    def navigate_directions(self, directions: List[str]) -> None:
        for direction in directions:
            self.navigate_direction(direction)

    def navigate_direction(self, direction: str) -> None:
        if len(direction) < 2:
            raise ValueError()

        instruction = direction[0]
        value = int(direction[1:])

        self._process_instruction(instruction, value)

    def calculate_manhattan_distance_from_origin(self) -> int:
        return abs(self._x_position) + abs(self._y_position)


class ShipWithBasicNavigation(Ship):
    _direction_degrees = {
        0: NORTH,
        90: EAST,
        180: SOUTH,
        270: WEST,
    }

    _direction_halves = {
        NORTH: 1,
        SOUTH: -1,
        EAST: 1,
        WEST: -1
    }

    move_instructions = [
        FORWARD,
        NORTH,
        SOUTH,
        EAST,
        WEST
    ]

    turn_instructions = [
        LEFT,
        RIGHT
    ]

    def __init__(self):
        Ship.__init__(self)
        self._direction: int = 90

    def _process_instruction(self, instruction: str, value: int) -> None:
        if instruction in ShipWithBasicNavigation.move_instructions:
            self.__move_ship(instruction, value)
        elif instruction in ShipWithBasicNavigation.turn_instructions:
            self.__turn_ship(instruction, value)
        else:
            raise ValueError()

    def __move_ship(self, direction: str, distance: int) -> None:
        if direction == FORWARD:
            direction = ShipWithBasicNavigation._direction_degrees[self._direction]

        if direction in [NORTH, SOUTH]:
            self._y_position += (distance * ShipWithBasicNavigation._direction_halves[direction])
        elif direction in [EAST, WEST]:
            self._x_position += (distance * ShipWithBasicNavigation._direction_halves[direction])
        else:
            raise ValueError()

    def __turn_ship(self, direction: str, degrees: int) -> None:
        if direction == RIGHT:
            self._direction = (self._direction + degrees) % 360
        elif direction == LEFT:
            self._direction = (self._direction - degrees) % 360
            if self._direction < 0:
                self._direction = 360 - self._direction
        else:
            raise ValueError()


class ShipWithWaypointNavigation(Ship):
    _waypoint_shift_instructions = [
        NORTH,
        SOUTH,
        EAST,
        WEST,
        LEFT,
        RIGHT
    ]

    def __init__(self):
        Ship.__init__(self)
        self._waypoint_direction: Dict[str, int] = {
            "x": 10,
            "y": 1
        }

    def _process_instruction(self, instruction: str, value: int) -> None:
        if instruction == FORWARD:
            self.__move_ship(value)
        elif instruction in ShipWithWaypointNavigation._waypoint_shift_instructions:
            self.__turn_ship(instruction, value)
        else:
            raise ValueError()

    def __move_ship(self, iterations: int) -> None:
        self._x_position += iterations * self._waypoint_direction["x"]
        self._y_position += iterations * self._waypoint_direction["y"]

    def __turn_ship(self, direction: str, value: int) -> None:
        # This is the number of turns we need to do if the command is LEFT or RIGHT
        num_shifts = int((value / 360 * 4)) % 4

        if direction == NORTH:
            self._waypoint_direction["y"] += value
        elif direction == SOUTH:
            self._waypoint_direction["y"] -= value
        elif direction == EAST:
            self._waypoint_direction["x"] += value
        elif direction == WEST:
            self._waypoint_direction["x"] -= value
        elif direction == LEFT:
            # We always want to shift right, so if we're shifting left calculate how many right shifts that is
            num_shifts = 4 - num_shifts
            self.__shift_waypoint_clockwise(num_shifts)
        elif direction == RIGHT:
            self.__shift_waypoint_clockwise(num_shifts)
        else:
            raise ValueError()

    def __shift_waypoint_clockwise(self, num_shifts: int) -> None:
        # Start by handling the simple cases of either staying as is or rotating by 180 degrees
        if num_shifts == 0 or num_shifts == 4:
            return
        elif num_shifts == 2:
            self._waypoint_direction["x"] *= -1
            self._waypoint_direction["y"] *= -1
            return

        # Rotate exactly 90 degrees by making x into the previous y value and y into the previous x value, but negated.
        temp_x = self._waypoint_direction["x"]
        self._waypoint_direction["x"] = self._waypoint_direction["y"]
        self._waypoint_direction["y"] = -1 * temp_x

        # Once we've taken care of one 90 degree rotation recurse to rotate again. At most there will be one level of
        # recursion assuming num_shifts was less than 4.
        self.__shift_waypoint_clockwise(num_shifts - 1)


def parse_input_file() -> List[str]:
    with open("/app/advent2020/inputs/rain_risk.txt", "r") as input_file:
        return input_file.readlines()


if __name__ == "__main__":
    input_directions = parse_input_file()

    basic_ship = ShipWithBasicNavigation()
    basic_ship.navigate_directions(input_directions)

    waypoint_ship = ShipWithWaypointNavigation()
    waypoint_ship.navigate_directions(input_directions)

    print("Manhattan Distance From Origin (Basic Navigation):", basic_ship.calculate_manhattan_distance_from_origin())
    print("Manhattan Distance From Origin (Waypoint Navigation):", waypoint_ship.calculate_manhattan_distance_from_origin())
