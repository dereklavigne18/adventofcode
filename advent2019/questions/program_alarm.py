from typing import List, Optional, Tuple

ADD_OPCODE = 1
MULT_OPCODE = 2
EXIT_OPCODE = 99

OPERATION_LENGTH = 4


def execute_intcode(intcode: List[int]) -> List[int]:
    resulting_intcode = intcode.copy()

    current_position = 0
    while current_position < len(resulting_intcode):

        opcode = resulting_intcode[current_position]
        if opcode == EXIT_OPCODE:
            return resulting_intcode

        elif opcode == ADD_OPCODE:
            addend_one_position = resulting_intcode[current_position + 1]
            addend_two_position = resulting_intcode[current_position + 2]
            sum_position = resulting_intcode[current_position + 3]

            resulting_intcode[sum_position] = resulting_intcode[addend_one_position] \
                + resulting_intcode[addend_two_position]

        elif opcode == MULT_OPCODE:
            term_one_position = resulting_intcode[current_position + 1]
            term_two_position = resulting_intcode[current_position + 2]
            product_position = resulting_intcode[current_position + 3]

            resulting_intcode[product_position] = resulting_intcode[term_one_position] \
                * resulting_intcode[term_two_position]

        else:
            # The int code was invalid and generated an unrecognized opcode
            raise ValueError()

        current_position += OPERATION_LENGTH

    return resulting_intcode


def execute_intcode_with_noun_and_verb(intcode: List[int], noun: int, verb: int) -> List[int]:
    intcode[1] = noun
    intcode[2] = verb
    return execute_intcode(intcode)


def find_noun_and_verb_for_intcode_result(intcode: List[int], result: int) -> Optional[Tuple[int, int]]:
    for noun in range(0, 100):
        for verb in range(0, 100):
            try:
                if execute_intcode_with_noun_and_verb(intcode, noun, verb)[0] == result:
                    return noun, verb
            except IndexError:
                # Weird intcode can cause exit opcodes to be missed or addresses outside the bounds of memory to occur
                pass

    return None


def parse_input_file() -> List[int]:
    with open("/app/advent2019/inputs/program_alarm.txt", "r") as input_file:
        return [int(position) for position in input_file.read().split(",")]


if __name__ == "__main__":
    intcode = parse_input_file()

    resulting_intcode = execute_intcode_with_noun_and_verb(intcode, 12, 2)
    print("IntCode Position 0:", resulting_intcode[0])

    noun, verb = find_noun_and_verb_for_intcode_result(intcode, 19690720)
    print("Result calculation (part 2):", noun * 100 + verb)
