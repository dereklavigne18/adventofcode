from typing import List, Optional


FRONT_CHAR = "F"
BACK_CHAR = "B"
LEFT_CHAR = "L"
RIGHT_CHAR = "R"


def calculate_decimal_value(value: str, set_char: str, unset_char: str) -> int:
    """
    Takes a string of bits, which can have alternative values representing 1s and 0s and converts it to a decimal
    integer.
    :param value: The value that is being converted to decimal
    :param set_char: The character that represents a set bit
    :param unset_char: The character that represents an unset bit
    :return: A decimal int
    """
    if len(set_char) != 1 or len(unset_char) != 1:
        raise ValueError()

    # To convert from binary to decimal the formula looks like
    # `decimal = R0*2^6 + R1*2^5 + R2*2^4 + R3*2^3 + R4*2^2 + R5*2^1 + R6*2^0` for a string of length 7, where RX is the
    # value of the bit at position X. Obviously, the value can be of variable length, so starting at the back and moving
    # to the front will allow us to deal with strings of any length.
    row_val = 0
    for row_index, row_dir in enumerate(value[::-1]):
        if row_dir == set_char:
            # According to the formula we only care about the set bits. Unset bits will not change the result
            row_val += 2 ** row_index
        elif row_dir != unset_char:
            # If it's not the set char and it's not the unset char then it's bad input
            raise ValueError()

    return row_val


def seat_id_from_line(line: str) -> int:
    if len(line) != 10:
        raise ValueError()

    row_dirs = line[:7]
    col_dirs = line[7:]

    row_value = calculate_decimal_value(row_dirs, BACK_CHAR, FRONT_CHAR)
    col_value = calculate_decimal_value(col_dirs, RIGHT_CHAR, LEFT_CHAR)

    # Below is the formula for calculating the final seat id. This should come out to the same value as if we replaced
    # all the right chars with back chars and left chars with front chars. Which, would've effectively treated value as
    # a single larger binary number
    return (row_value * 8) + col_value


def calculate_seat_ids_from_input_file() -> List[int]:
    seat_ids = []
    with open("/app/advent2020/inputs/binary_boarding.txt", "r") as input_file:
        for line in input_file:
            try:
                seat_ids.append(seat_id_from_line(line.strip()))
            except ValueError:
                # If a ValueError is thrown the line was invalid, so skip it
                pass

    return seat_ids


def scan_for_missing_seat(seat_ids: List[int]) -> Optional[int]:
    sorted_seats = sorted(seat_ids)

    # Iterating from the front up to half and back to half at the same time.
    for index in range(0, int(len(seat_ids) / 2)):
        back_index = -index - 1

        front_seat = sorted_seats[index]
        back_seat = sorted_seats[back_index]

        expected_next_front = front_seat + 1
        expected_next_back = back_seat - 1

        if sorted_seats[index + 1] != expected_next_front:
            return expected_next_front
        elif sorted_seats[back_index - 1] != expected_next_back:
            return expected_next_back

    return None



if __name__ == "__main__":
    seat_ids = calculate_seat_ids_from_input_file()
    print("Highest Seat Id:", max(seat_ids))

    missing_seat_id = scan_for_missing_seat(seat_ids)
    if missing_seat_id:
        print("Your Seat Id:", missing_seat_id)
    else:
        print("Could not find your seat")