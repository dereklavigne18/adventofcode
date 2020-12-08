from math import prod
from typing import List

SYMBOL_TREE = "#"


def count_trees_in_path(grid: List[List[str]], horizontal_velocity: int, vertical_velocity: int) -> int:
    x = 0
    y = 0
    tree_count = 0

    # There's a big assumption that all rows are the same length here
    last_col = len(grid[0]) - 1

    while y < len(grid):
        tree_count += int(grid[y][x] == SYMBOL_TREE)
        y += vertical_velocity

        # X gets funky cause the pattern repeats when we reach the boundary of the grid, so really we want to compute
        # how far into the current OR the next iteration of the pattern we are.
        x = (x + horizontal_velocity) % last_col

    return tree_count


def parse_input() -> List[List[str]]:
    with open("/app/advent2020/inputs/toboggan_trajectory.txt", "r") as input_file:
        return [list(line) for line in input_file]


if __name__ == "__main__":
    grid = parse_input()
    horizontal_velocities = [1, 3, 5, 7]
    tree_counts = [count_trees_in_path(grid, hv, 1) for hv in horizontal_velocities]
    tree_counts.append(count_trees_in_path(grid, 1, 2))

    print("Part 2 Answer:", prod(tree_counts))
