from argparse import ArgumentParser
from itertools import combinations
from math import prod
from typing import List, Optional, Tuple


INPUT_FILE_PATH = "/app/inputs/report_repair.txt"


def find_vals_summing_to_target(vals: List[int], addend_count: int, target: int) -> Optional[List[int]]:
    val_len = len(vals)
    if val_len < addend_count:
        return None

    combos = combinations(vals, addend_count)
    for combo in combos:
        if sum(combo) == target:
            return combo


def read_input() -> List[int]:
    vals = []
    with open(INPUT_FILE_PATH, "r") as input_file:
        for line in input_file:
            cleaned_line = line.strip()

            try:
                vals.append(int(cleaned_line))
            except ValueError:
                continue

    return vals


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--sum", type=int, help="The value we need the numbers to sum to")
    parser.add_argument("--addends", type=int,  help="The number of addends that need to be used to add to the sum")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    input_vals = read_input()
    result = find_vals_summing_to_target(input_vals, args.addends, args.sum)

    if result is None:
        print("Couldn't repair the report")
    else:
        print("Expense Report Value: ", prod(result))