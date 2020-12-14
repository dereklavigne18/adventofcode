from math import prod
from typing import Dict, Tuple, List, Optional


DECOMMISSIONED_BUS = "x"


def find_next_bus_after_timestamp(timestamp: int, buses: List[str]) -> Optional[Tuple[int, int]]:
    soonest_bus: Optional[int] = None
    shortest_wait_time: Optional[int] = None

    for bus in buses:
        if bus == DECOMMISSIONED_BUS:
            continue

        bus = int(bus)
        bus_wait_time = (bus - (timestamp % bus)) % bus
        if shortest_wait_time is None or bus_wait_time < shortest_wait_time:
            soonest_bus = bus
            shortest_wait_time = bus_wait_time

    if soonest_bus is None:
        return None
    else:
        return soonest_bus, shortest_wait_time


def inverse_modulo(value: int, mod: int) -> int:
    value %= mod
    for x in range(1, mod):
        if (value * x) % mod == 1:
            return x

    return 1


def find_timestamp_where_departure_sequence_is_met(departure_sequence: List[str]) -> Optional[int]:
    bus_offsets: Dict[int, int] = {}
    for offset, departure in enumerate(departure_sequence):
        if departure == DECOMMISSIONED_BUS:
            continue

        bus_offsets[int(departure)] = offset

    if not bus_offsets:
        return None

    product = prod(bus_offsets.keys())
    accumulator = 0
    for bus_id, bus_index in bus_offsets.items():
        floored_divisor = product // bus_id
        accumulator += bus_index * inverse_modulo(floored_divisor, bus_id) * floored_divisor

    return accumulator % product


    #
    # buses = sorted(bus_offsets.keys(), reverse=True)
    #
    # cumulative_product = 1
    # timestamp = buses[0] - (bus_offsets[buses[0]] % buses[0])
    # for bus_index, bus in enumerate(buses[:-1]):
    #     cumulative_product *= 1
    #
    #     next_bus_id = buses[bus_index + 1]
    #     next_remainder = next_bus_id - (bus_offsets[next_bus_id] % next_bus_id)
    #     print("NR", next_remainder)
    #     while timestamp % next_bus_id != next_remainder:
    #         timestamp += cumulative_product
    #
    # return timestamp

    ### Attempt 1

    # step_size = buses[0]
    # step_num = 1
    # while True:
    #     timestamp = step_num * step_size - bus_offsets[step_size]
    #
    #     fits_sequence = True
    #     for bus_id in buses[1:]:
    #         if not (timestamp + bus_offsets[bus_id]) % bus_id == 0:
    #             fits_sequence = False
    #             break
    #
    #     if not fits_sequence:
    #         step_num += 1
    #         continue
    #
    #     return timestamp


def parse_input_file() -> Tuple[int, List[str]]:
    with open("/app/advent2020/inputs/shuttle_search.txt", "r") as input_file:
        return (
            int(input_file.readline()),
            input_file.readline().split(",")
        )


if __name__ == "__main__":
    timestamp, buses = parse_input_file()
    bus, wait_time = find_next_bus_after_timestamp(timestamp, buses)
    sequence_timestamp = find_timestamp_where_departure_sequence_is_met(buses)

    print("Bus x Wait Time =", bus * wait_time)
    print("Sequence Timestamp:", sequence_timestamp)
