from typing import Dict, List, Optional


class DecoderChipSimulator:
    MASK_ASSIGNEE = "mask"
    MEMORY_ASSIGNEE = "mem"

    def __init__(self):
        self._memory: Dict[int, int] = {}

    def get_memory(self) -> Dict[int, int]:
        return self._memory

    def execute_instruction(self, instruction: str) -> Dict[int, int]:
        raise NotImplementedError()


class DecoderChipSimulatorVersion1(DecoderChipSimulator):
    MASK_IGNORE_VALUE = "X"

    def __init__(self):
        DecoderChipSimulator.__init__(self)
        self._mask: Optional[Dict[int, int]] = None

    def execute_instruction(self, instruction: str) -> Dict[int, int]:
        assignee, value = instruction.split("=")

        if assignee[:len(DecoderChipSimulator.MASK_ASSIGNEE)] == DecoderChipSimulator.MASK_ASSIGNEE:
            self._mask = self._raw_bitmask_to_dict(value.strip())
        elif assignee[:len(DecoderChipSimulator.MEMORY_ASSIGNEE)] == DecoderChipSimulator.MEMORY_ASSIGNEE and self._mask:
            address = int(assignee.strip()[len(DecoderChipSimulator.MEMORY_ASSIGNEE) + 1: -1])
            self._memory[address] = self._apply_bitmask(int(value.strip()), self._mask)
        else:
            raise ValueError()

        return self._memory

    def _raw_bitmask_to_dict(self, bitmask: str) -> Dict[int, int]:
        """
        :return: The bitmask represented as a dictionary where the key is the position of a value to be set or unset and the
                 value is 1 for bits to be set and 0 for those to be unset.
        """
        result = {}
        for i, mask_val in enumerate(bitmask):
            if mask_val != DecoderChipSimulatorVersion1.MASK_IGNORE_VALUE:
                # Least significant bits are on the right
                result[len(bitmask) - 1 - i] = int(mask_val)

        return result

    def _apply_bitmask(self, value: int, mask: Dict[int, int]) -> int:
        for bit_index, is_mask_bit_set in mask.items():
            value_of_bit = 2 ** bit_index

            # This is formula gets the value of the bit at position `bit_index` where the least significant figure is at
            # `bit_index` 0 and the index increments as we move toward the most significant bit
            is_bit_set = (value // value_of_bit) % 2

            if is_bit_set == is_mask_bit_set:
                # If they're equal we don't need to change the value
                continue
            elif is_bit_set:
                # Unset the bit using subtraction
                value -= value_of_bit
            elif not is_bit_set:
                # Set the bit using addition
                value += value_of_bit

        return value


class DecoderChipSimulatorVersion2(DecoderChipSimulator):
    STAY_BIT = "0"
    SWITCH_BIT = "1"
    FLOATING_BIT = "X"

    def __init__(self):
        DecoderChipSimulator.__init__(self)
        self._mask: Optional[str] = None

    def execute_instruction(self, instruction: str) -> Dict[int, int]:
        assignee, value = instruction.split("=")

        if assignee[:len(DecoderChipSimulator.MASK_ASSIGNEE)] == DecoderChipSimulator.MASK_ASSIGNEE:
            self._mask = value.strip()
        elif assignee[:len(DecoderChipSimulator.MEMORY_ASSIGNEE)] == DecoderChipSimulator.MEMORY_ASSIGNEE and self._mask:
            int_value = int(value.strip())
            for address in self._calculate_addresses(int(assignee.strip()[len(DecoderChipSimulator.MEMORY_ASSIGNEE) + 1: -1])):
                self._memory[address] = int_value
        else:
            raise ValueError()

        return self._memory

    def _calculate_addresses(self, original_address: int) -> List[int]:
        return self._calculate_addresses_recursively(original_address, self._mask, [0], 0)

    def _calculate_addresses_recursively(
            self,
            original_address: int,
            mask: str,
            wip_addresses: List[int],
            position: int
    ) -> List[int]:
        if not mask:
            return wip_addresses

        mask_bit = mask[-1]
        mask_rest = mask[:-1]

        new_addresses = []
        for address in wip_addresses:
            set_bit_value = address + 1 * 2**position
            if mask_bit == DecoderChipSimulatorVersion2.STAY_BIT:
                is_bit_set = (original_address // 2** position) % 2
                new_addresses.append(address if not is_bit_set else set_bit_value)
            elif mask_bit == DecoderChipSimulatorVersion2.SWITCH_BIT:
                new_addresses.append(set_bit_value)
            elif mask_bit == DecoderChipSimulatorVersion2.FLOATING_BIT:
                new_addresses.append(address)
                new_addresses.append(set_bit_value)

        return self._calculate_addresses_recursively(original_address, mask_rest, new_addresses, position + 1)


def parse_input_file() -> List[str]:
    with open("/app/advent2020/inputs/docking_data.txt", "r") as input_file:
        return input_file.readlines()


if __name__ == "__main__":
    v1_simulator = DecoderChipSimulatorVersion1()
    v2_simulator = DecoderChipSimulatorVersion2()
    for instruction in parse_input_file():
        v1_simulator.execute_instruction(instruction)
        v2_simulator.execute_instruction(instruction)

    print("Sum of Memory Values (V1):", sum(v1_simulator.get_memory().values()))
    print("Sum of Memory Values (V2):", sum(v2_simulator.get_memory().values()))
