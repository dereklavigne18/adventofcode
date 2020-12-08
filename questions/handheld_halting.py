from typing import List, Tuple


ACCUMULATE_COMMAND = 'acc'
JUMP_COMMAND = 'jmp'
NOOP_COMMAND = 'nop'


def parse_command(command: str) -> Tuple[str, int]:
    cmd_type, cmd_val_text = command.split(" ")
    return cmd_type, int(cmd_val_text)


def execute_commands(commands: List[str]) -> Tuple[int, bool, List[int]]:
    """
    Execute the commands returning the accumulated result and some metadata about the execution.
    :param commands: Just a list of commands that need to be run
    :return: (accumulated value, was cycle detected, indexes of the commands executed in the order of execution)
    """
    accumulator = 0
    cmd_index = 0
    cmd_path = []

    while cmd_index < len(commands):
        if cmd_index in cmd_path:
            return accumulator, True, cmd_path

        # Mark command as seen and execute
        cmd_path.append(cmd_index)
        cmd_type, cmd_val = parse_command(commands[cmd_index])

        if cmd_type == ACCUMULATE_COMMAND:
            accumulator += cmd_val
            cmd_index += 1
        elif cmd_type == JUMP_COMMAND:
            cmd_index += cmd_val
        elif cmd_type == NOOP_COMMAND:
            cmd_index += 1
        else:
            raise ValueError()

    return accumulator, False, cmd_path


def calculate_accumulated(commands: List[str]) -> int:
    accumulated, *_ = execute_commands(commands)
    return accumulated


def corrective_calculate_accumulated(commands: List[str]) -> int:
    result, cycle_detected, path = execute_commands(commands)

    command_transformations = {
        JUMP_COMMAND: NOOP_COMMAND,
        NOOP_COMMAND: JUMP_COMMAND,
    }

    # Starting at the back of the path (seems like later commands may be more likely to fix the problem) change nop to
    # jmp or vice versa and see if a cycle is detected. If it is move to the next nop or jmp.
    for cmd_index in path[::-1]:
        if not cycle_detected:
            return result

        # We cannot mutate the input command list (we'll need it in all iterations, so copy it)
        commands_working = commands.copy()

        cmd_type, cmd_val = parse_command(commands_working[cmd_index])
        if cmd_type not in command_transformations.keys():
            # If it's not an available transform skip the command
            continue

        commands_working[cmd_index] = f"{command_transformations[cmd_type]} {cmd_val}"
        result, cycle_detected, path = execute_commands(commands_working)

    if not cycle_detected:
        return result

    # Program is unable to be corrected with the allowed command transformations
    raise ValueError()


def parse_input_file() -> List[str]:
    with open("/app/inputs/handheld_halting.txt", "r") as input_file:
        return [line.strip() for line in input_file]


if __name__ == "__main__":
    commands = parse_input_file()
    print("Final Accumulated Value (with cycle):", calculate_accumulated(commands))
    print("Corrected Program Accumulated Value:", corrective_calculate_accumulated(commands))