from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


NO_INNER_BAGS_TEXT = "no other"


class Bag:
    def __init__(self, name: str):
        self._name: str = name
        self._edges: List[BagEdge] = []

    def get_name(self):
        return self._name

    def get_edges(self) -> List[BagEdge]:
        return self._edges

    def add_edge(self, edge: BagEdge) -> Bag:
        if edge not in self._edges:
            self._edges.append(edge)
        return self

    def is_outermost_bag(self) -> bool:
        for edge in self._edges:
            if self == edge.inner_bag:
                return False
        return True


@dataclass(frozen=True)
class BagEdge:
    outer_bag: Bag
    inner_bag: Bag
    num_inner_bags: int


class BagLocator:
    def __init__(self):
        self._bag_map: Dict[str, Bag] = {}

    def get_bag(self, name: str) -> Optional[Bag]:
        if name not in self._bag_map.keys():
            self._bag_map[name] = Bag(name)
        return self._bag_map[name]

    def add_bag(self, name: str, bag: Bag):
        self._bag_map[name] = bag
        return self


def find_outer_bags_containing_bag(bag: Bag) -> List[Bag]:
    if bag.is_outermost_bag():
        return []

    outer_bags = []
    for edge in bag.get_edges():
        if bag == edge.inner_bag:
            # Add the outer bag of the current and add its outer bags
            outer_bags.append(edge.outer_bag)
            outer_bags.extend(find_outer_bags_containing_bag(edge.outer_bag))

    return list(set(outer_bags))


def count_number_of_bags_within_bag(bag: Bag) -> int:
    count = 0
    for edge in bag.get_edges():
        if bag == edge.outer_bag:
            count += edge.num_inner_bags * (count_number_of_bags_within_bag(edge.inner_bag) + 1)

    return count


def parse_input_line(line: str, bag_locator: BagLocator) -> None:
    # Remove trailing whitespace and period. Also, remove all references to bag or bags (we won't use them)
    clean_line = line \
        .strip() \
        .rstrip(".") \
        .replace("bags", "") \
        .replace("bag", "")

    bag_name, inner_bags_text = clean_line.split("contain")
    outer_bag = bag_locator.get_bag(bag_name.strip())

    if inner_bags_text.strip() == NO_INNER_BAGS_TEXT:
        return

    inner_bags_list = inner_bags_text.split(",")
    for inner_bag_text in inner_bags_list:
        num_bags_text, inner_bag_name = inner_bag_text.strip().split(" ", 1)

        inner_bag = bag_locator.get_bag(inner_bag_name)
        edge = BagEdge(outer_bag, inner_bag, int(num_bags_text))

        outer_bag.add_edge(edge)
        inner_bag.add_edge(edge)


def parse_input_file() -> BagLocator:
    bag_locator = BagLocator()

    with open("/app/advent2020/inputs/handy_haversacks.txt", "r") as input_file:
        for line in input_file:
            parse_input_line(line, bag_locator)

    return bag_locator


if __name__ == "__main__":
    bag_locator = parse_input_file()
    starting_bag = bag_locator.get_bag("shiny gold")
    outermost_bags = find_outer_bags_containing_bag(starting_bag)
    inner_bag_count = count_number_of_bags_within_bag(starting_bag)

    print("# of bags allowed to contain a shiny gold bag:", len(outermost_bags))
    print("# of bags needed in one shiny gold bag:", inner_bag_count)