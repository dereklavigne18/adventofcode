from typing import List, Tuple


ALPHABET = "abcdefghijklmnopqrstuvwxyz"

# Generates a dict where the key is a letter in the alphabet and the value is an int 0-25, which will be used to map
# between letters and list indexes later
alphabet_map = {letter: index for index, letter in enumerate(ALPHABET)}


def get_group_answers_where_at_least_one_was_yes(answer_string: str) -> List[int]:
    # a is the 0th index, z is the 25th. The rest of the alphabet is in between. If a question is answered yes, the
    # value of the corresponding index is changed to 1.
    answers = [0] * 26
    for answer in answer_string:
        index = alphabet_map[answer]
        answers[index] = 1

    return answers


def get_group_answers_where_all_were_yes(answer_string: str, group_size: int) -> List[int]:
    # a is the 0th index, z is the 25th. The rest of the alphabet is in between. If a question is answered yes, the
    # value of the corresponding index is incremented.
    yes_counts = [0] * 26
    for answer in answer_string:
        index = alphabet_map[answer]
        yes_counts[index] += 1

    # Now that we know how many times each question was answered yes, we need to check if the count is equal to the
    # group size.
    answers_all_were_yes = [0] * 26
    for index, answer_count in enumerate(yes_counts):
        answers_all_were_yes[index] = int(answer_count == group_size)

    return answers_all_were_yes


def get_all_groups_answers() -> Tuple[List[List[int]], List[List[int]]]:
    at_least_one_yes_group_answers = []
    all_yes_group_answers = []

    with open("/app/inputs/custom_customs.txt", "r") as input_file:

        group_size = 0
        group_answers_input = ""
        for line in input_file:
            clean_line = line.strip()

            if clean_line:
                group_size += 1
                group_answers_input += clean_line
                continue

            # If the line is empty, but the input isn't
            if group_answers_input:
                try:
                    at_least_one_yes_group_answers.append(get_group_answers_where_at_least_one_was_yes(group_answers_input))
                    all_yes_group_answers.append(get_group_answers_where_all_were_yes(group_answers_input, group_size))
                except KeyError:
                    # If there's a KeyError it's because the input has an invalid char
                    pass

                group_size = 0
                group_answers_input = ""

    # If the last line wasn't blank then we still need to process the last record
    if group_answers_input:
        try:
            at_least_one_yes_group_answers.append(get_group_answers_where_at_least_one_was_yes(group_answers_input))
            all_yes_group_answers.append(get_group_answers_where_all_were_yes(group_answers_input, group_size))
        except KeyError:
            # If there's a KeyError it's because the input has an invalid char
            pass

    return at_least_one_yes_group_answers, all_yes_group_answers


if __name__ == "__main__":
    at_least_one_yes_group_answers, all_yes_group_answers = get_all_groups_answers()

    at_least_one_yes_count = sum([sum(group_answers) for group_answers in at_least_one_yes_group_answers])
    print("Group Answer (at least one) Yes Count: ", at_least_one_yes_count)

    all_yes_group_count = sum([sum(group_answers) for group_answers in all_yes_group_answers])
    print("Group Answer (every) Yes Count:", all_yes_group_count)
