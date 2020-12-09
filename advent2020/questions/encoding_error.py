from sys import exit
from typing import List, Optional

from advent2020.questions.report_repair import find_vals_summing_to_target


def find_first_encoding_error(encoded_data: List[int], preamble_length: int) -> Optional[int]:
    if len(encoded_data) < preamble_length + 1:
        raise ValueError()

    current_index = preamble_length
    while current_index < len(encoded_data):
        addends_start_index = current_index - preamble_length
        previous = encoded_data[addends_start_index:current_index]
        sum_target = encoded_data[current_index]

        addends = find_vals_summing_to_target(previous, 2, sum_target)
        if not addends:
            return sum_target

        current_index += 1


def find_contiguous_set_summing_to_target(encoded_data: List[int], target_sum: int) -> Optional[List[int]]:
    # Starting at the back because the process of elimination should be faster (higher numbers)
    end_index = len(encoded_data) - 1

    while end_index > -1:
        # Skip checking if the first value being checked is already bigger than the sum
        if encoded_data[end_index] >= target_sum:
            end_index -= 1
            continue

        for addend_count in range(2, len(encoded_data) - 1):
            values = encoded_data[end_index - addend_count + 1: end_index + 1]
            if sum(values) == target_sum:
                return values

        end_index -= 1

    return None


def parse_input_file() -> List[int]:
    with open("/app/advent2020/inputs/encoding_error.txt", "r") as input_file:
        return [int(line.strip()) for line in input_file.readlines()]


if __name__ == "__main__":
    encoded_data = parse_input_file()
    error_value = find_first_encoding_error(encoded_data, 25)

    if not error_value:
        print("No Encoding Errors Found")
        exit(1)

    print("First Encoding Error Value:", error_value)

    addends = find_contiguous_set_summing_to_target(encoded_data, error_value)
    print("Encryption Weakness:", min(addends) + max(addends))
