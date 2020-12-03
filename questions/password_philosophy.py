from argparse import ArgumentParser
import sys
from typing import Any, Tuple


class LetterValueError(ValueError):
    pass


class PasswordRule:
    def check_password(self, password: str) -> bool:
        raise NotImplementedError()


class CharCountPasswordRule(PasswordRule):
    def __init__(self, char: str, min_count: int, max_count: int):
        if not is_char(char):
            raise LetterValueError()

        self._char: str = char
        self._min_count: int = min_count
        self._max_count: int = max_count

    def check_password(self, password: str) -> bool:
        match_count = 0

        for char in password:
            match_count += int(char == self._char)

        return self._min_count <= match_count <= self._max_count


class CharPositionPasswordRule(PasswordRule):
    def __init__(self, char: str, position_one: int, position_two: int):
        if not is_char(char):
            raise LetterValueError()

        self._char: str = char
        self._position_one: int = position_one
        self._position_two: int = position_two

    def check_password(self, password: str) -> bool:
        return self._check_letter_at_position(password, self._position_one) \
               != self._check_letter_at_position(password, self._position_two)

    def _check_letter_at_position(self, password: str, position: int) -> bool:
        try:
            return password[position - 1] == self._char
        except IndexError:
            return False


def is_char(text: Any) -> bool:
    return type(text) == str and len(text) == 1


def count_valid_passwords_in_input_file(password_rule_type: type) -> int:
    valid_count = 0

    with open("/app/inputs/password_philosophy.txt", "r") as input_file:
        for line in input_file:
            (num1, num2, char, password) = parse_line(line)

            if password_rule_type == CharCountPasswordRule:
                rule = CharCountPasswordRule(char, num1, num2)
            elif password_rule_type == CharPositionPasswordRule:
                rule = CharPositionPasswordRule(char, num1, num2)
            else:
                raise ValueError()

            valid_count += int(rule.check_password(password))

    return valid_count


def parse_line(line: str) -> Tuple[int, int, str, str]:
    """
    :param line: The line to parse. Format "1-3 a: fakepassword"
    :return: The parts of the line (num1, num2, char, password). Example (1, 3, a, fakepassword)
    """
    line_parts = line.split(":")
    if len(line_parts) != 2:
        raise ValueError()

    rule_string, raw_password = line_parts
    rule_parts = rule_string.split(" ")
    if len(rule_parts) != 2:
        raise ValueError()

    count_range_string, letter = rule_parts
    rule_count_parts = count_range_string.split("-")
    if len(rule_count_parts) != 2:
        raise ValueError()

    min_count, max_count = rule_count_parts

    return int(min_count), int(max_count), letter.strip(), raw_password.strip()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--check", type=str, help="The type of password rule to use. Can be CharPosition or CharCount.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.check == "CharCount":
        password_rule_type = CharCountPasswordRule
    elif args.check == "CharPosition":
        password_rule_type = CharPositionPasswordRule
    else:
        print("Invalid --check argument provided")
        sys.exit(1)

    print("Count of valid passwords:", count_valid_passwords_in_input_file(password_rule_type))
