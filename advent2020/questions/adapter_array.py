from typing import Any, List, Tuple


def organize_adapters(adapter_ratings: List[int]) -> List[int]:
    return [0] + sorted(adapter_ratings) + [max(adapter_ratings) + 3]


def count_jolt_adaptations(sorted_adapter_ratings: List[int]) -> Tuple[int, int, int]:
    if not sorted_adapter_ratings:
        raise ValueError()

    rating_step_counts = [0, 0, 0]

    for rating_index in range(len(sorted_adapter_ratings) - 1):
        rating_step = sorted_adapter_ratings[rating_index + 1] - sorted_adapter_ratings[rating_index]
        if rating_step > 3:
            raise ValueError()

        rating_step_counts[rating_step - 1] += 1

    return rating_step_counts[0], rating_step_counts[1], rating_step_counts[2]


def count_working_adapter_sequences(sorted_adapter_ratings: List[int]) -> int:
    if not sorted_adapter_ratings:
        raise ValueError()

    # Key is the number where the subsequence starts, Value is the count of valid sequences
    sequence_counts = {}
    for adapter_index in range(len(sorted_adapter_ratings) - 1, -1, -1):
        if adapter_index == len(sorted_adapter_ratings) - 1:
            sequence_counts[sorted_adapter_ratings[adapter_index]] = 1
            continue

        count = 0
        for look_ahead in range(1, 4):
            if adapter_index + look_ahead < len(sorted_adapter_ratings) \
                    and sorted_adapter_ratings[adapter_index + look_ahead] - sorted_adapter_ratings[adapter_index] <= 3:
                count += sequence_counts[sorted_adapter_ratings[adapter_index + look_ahead]]

        sequence_counts[sorted_adapter_ratings[adapter_index]] = count

    return sequence_counts[sorted_adapter_ratings[0]]


def parse_input_file() -> List[int]:
    with open("/app/advent2020/inputs/adapter_array.txt", "r") as input_file:
        return [int(line) for line in input_file.readlines()]


if __name__ == "__main__":
    adapter_ratings = parse_input_file()
    one_step_count, two_step_count, three_step_count = count_jolt_adaptations(organize_adapters(adapter_ratings))
    sequence_count = count_working_adapter_sequences(organize_adapters(adapter_ratings))

    print("Step Count Aggregation:", one_step_count * three_step_count)
    print("Working Adapter Sequences:", sequence_count)
