from typing import Dict, List, Tuple


class TicketValidator:
    def __init__(self):
        self._valid_values: List[int] = []
        self._field_ranges: Dict[str, List[int]] = {}

    def add_valid_value_range(self, field_name: str, min_val: int, max_val: int):
        self._valid_values.extend(range(min_val, max_val + 1))
        self._valid_values = list(set(self._valid_values))

        if field_name not in self._field_ranges:
            self._field_ranges[field_name] = list(range(min_val, max_val + 1))
        else:
            self._field_ranges[field_name].extend(range(min_val, max_val + 1))

    def validate(self, ticket: List[int]) -> List[int]:
        return [value for value in ticket if value not in self._valid_values]

    def get_field_names(self) -> List[str]:
        return list(self._field_ranges.keys())

    def validate_value_in_field_range(self, value: int, field_name: str) -> bool:
        return value in self._field_ranges[field_name]


def find_invalid_tickets_values(
        tickets: List[List[int]],
        ticket_validator: TicketValidator
) -> List[int]:
    invalid_values: List[int] = []

    for ticket in tickets:
        invalid_values.extend(ticket_validator.validate(ticket))

    return invalid_values


def identify_columns_that_are_valid_for_field(field_name: str, tickets: List[List[int]], ticket_validator: TicketValidator) -> List[int]:
    valid_cols = []

    for field_col in range(len(tickets[0])):
        field_valid_for_values = True
        for ticket in tickets:
            if not ticket_validator.validate_value_in_field_range(ticket[field_col], field_name):
                field_valid_for_values = False
                break

        if field_valid_for_values:
            valid_cols.append(field_col)

    return valid_cols


def find_order_of_ticket_fields(
    tickets: List[List[int]],
    ticket_validator: TicketValidator
) -> Dict[str, int]:
    valid_tickets = [ticket for ticket in tickets if not ticket_validator.validate(ticket)]

    # Brute force elimination of cols where there is an invalid value for a field
    options = {}
    for field_name in ticket_validator.get_field_names():
        options[field_name] = identify_columns_that_are_valid_for_field(field_name, valid_tickets, ticket_validator)

    is_one_to_one = False
    while not is_one_to_one:
        # Eliminate any columns from all fields that are the only possibility for another field
        cols_to_eliminate = [cols[0] for cols in options.values() if len(cols) == 1]
        for col_to_eliminate in cols_to_eliminate:
            for cols in options.values():
                if len(cols) > 1 and cols_to_eliminate in cols:
                    cols.remove(col_to_eliminate)

        # If any cols only appear in one field eliminate all other cols
        inverted_options = {}
        for field_name, cols in options.items():
            for col in cols:
                if col in inverted_options:
                    inverted_options[col].append(field_name)
                else:
                    inverted_options[col] = [field_name]

        for col, fields in inverted_options.items():
            if len(fields) < 2:
                options[fields[0]] = [col]

        is_one_to_one = True
        for cols in options.values():
            if len(cols) > 1:
                is_one_to_one = False

    final_options = {}
    for field_name, cols in options.items():
        final_options[field_name] = cols[0]

    return final_options


def parse_input_file() -> Tuple[List[List[int]], List[int], TicketValidator]:
    validator_rules_section = 0
    your_ticket_section = 1
    nearby_ticket_section = 2

    current_section = 0

    my_ticket = []
    nearby_tickets = []
    validator = TicketValidator()
    with open("/app/advent2020/inputs/ticket_translation.txt", "r") as input_file:
        for line in input_file:
            stripped_line = line.strip()
            if not stripped_line:
                continue
            elif stripped_line == "your ticket:":
                current_section = your_ticket_section
            elif stripped_line == "nearby tickets:":
                current_section = nearby_ticket_section
            elif current_section == validator_rules_section:
                field_name, ranges_text, *_ = stripped_line.split(":")
                ranges = ranges_text.split("or")
                for r in ranges:
                    min_val, max_val, *_ = [int(val.strip()) for val in r.split("-")]
                    validator.add_valid_value_range(field_name, min_val, max_val)
            elif current_section == your_ticket_section:
                my_ticket = [int(val.strip()) for val in stripped_line.split(",")]
            elif current_section == nearby_ticket_section:
                nearby_tickets.append([int(val.strip()) for val in stripped_line.split(",")])

    return nearby_tickets, my_ticket, validator


if __name__ == "__main__":
    tickets, my_ticket, ticket_validator = parse_input_file()
    print("Ticket Scanning Error Rate:", sum(find_invalid_tickets_values(tickets, ticket_validator)))

    product = 1
    for field_name, col_index in find_order_of_ticket_fields(tickets, ticket_validator).items():
        if field_name[slice(0, 9)] == "departure":
            product *= my_ticket[col_index]
    print("Product of Departure Field Cols:", product)