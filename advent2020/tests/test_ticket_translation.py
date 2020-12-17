from typing import List, Tuple

import pytest

from advent2020.questions.ticket_translation import (
    TicketValidator,
    find_invalid_tickets_values
)


def ticket_validator_provider() -> TicketValidator:
    ticket_validator = TicketValidator()
    ticket_validator.add_valid_value_range("a", 1, 3)
    ticket_validator.add_valid_value_range("b", 5, 7)
    ticket_validator.add_valid_value_range("c", 6, 11)
    ticket_validator.add_valid_value_range("d", 33, 44)
    ticket_validator.add_valid_value_range("e", 13, 40)
    ticket_validator.add_valid_value_range("f", 45, 50)

    return ticket_validator


# Subject TicketValidator.validate
def validate_provider() -> List[Tuple[List[int], TicketValidator, List[int]]]:
    return [
        ([7, 3, 47], ticket_validator_provider(), []),
        ([40, 4, 50], ticket_validator_provider(), [4]),
        ([55, 2, 20], ticket_validator_provider(), [55]),
        ([38, 6, 12], ticket_validator_provider(), [12]),
    ]


@pytest.mark.parametrize("ticket,ticket_validator,expected", validate_provider())
def test_TicketValidator_validate_happy_path(ticket, ticket_validator, expected):
    assert ticket_validator.validate(ticket) == expected


# Subject: find_invalid_tickets_values
def find_invalid_tickets_values_provider() -> List[Tuple[
    List[List[int]],
    TicketValidator,
    List[int]
]]:
    return [
        (
            [[7, 3, 47], [40, 4, 50], [55, 2, 20], [38, 6, 12]],
            ticket_validator_provider(),
            [4, 55, 12]
        ),
    ]


@pytest.mark.parametrize("tickets,fields,expected", find_invalid_tickets_values_provider())
def test__find_invalid_tickets_values__happy_path(tickets, fields, expected):
    assert find_invalid_tickets_values(tickets, fields) == expected
