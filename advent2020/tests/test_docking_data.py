from advent2020.questions.docking_data import DecoderChipSimulatorVersion1, DecoderChipSimulatorVersion2


# Subject: DecoderChipSimulatorVersion1
def test__DecoderChipSimulatorVersion1_execute_instruction():
    instructions = [
        "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
        "mem[8] = 11",
        "mem[7] = 101",
        "mem[8] = 0",
    ]

    v1 = DecoderChipSimulatorVersion1()
    for instruction in instructions:
        v1.execute_instruction(instruction)

    assert v1.get_memory() == {7: 101, 8: 64}


# Subject: DecoderChipSimulatorVersion2
def test__DecoderChipSimulatorVersion2_execute_instruction():
    instructions = [
        "mask = 000000000000000000000000000000X1001X",
        "mem[42] = 100",
        "mask = 00000000000000000000000000000000X0XX",
        "mem[26] = 1",
    ]

    v2 = DecoderChipSimulatorVersion2()
    for instruction in instructions:
        v2.execute_instruction(instruction)

    assert v2.get_memory() == {26: 1, 58: 100, 27: 1, 59: 100, 16: 1, 24: 1, 18: 1, 17: 1, 25: 1, 19: 1}
