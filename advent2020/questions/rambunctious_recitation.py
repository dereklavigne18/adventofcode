from typing import List


def calculate_answer_at_turn(start: List[int], turn_count: int) -> int:
    if len(start) > turn_count:
        raise ValueError()

    prev_turn_value = start[-1]
    last_seen_map = {value: position for position, value in enumerate(start[:-1], start=1)}
    for turn in range(len(start) + 1, turn_count + 1):

        if prev_turn_value in last_seen_map:
            turn_value = turn - 1 - last_seen_map[prev_turn_value]
        else:
            turn_value = 0

        last_seen_map[prev_turn_value] = turn - 1
        prev_turn_value = turn_value

    return prev_turn_value


if __name__ == "__main__":
    print("2020th Turn Answer:", calculate_answer_at_turn([0, 8, 15, 2, 12, 1, 4], 2020))
    print("30000000th Turn Answer:", calculate_answer_at_turn([0, 8, 15, 2, 12, 1, 4], 30000000))
