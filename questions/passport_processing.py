from dataclasses import dataclass
from typing import Dict, List, Optional

MIN_BYR = 1920
MAX_BYR = 2002

MIN_IYR = 2010
MAX_IYR = 2020

MIN_EYR = 2020
MAX_EYR = 2030

HEIGHT_UNIT_INCHES = "in"
HEIGHT_UNIT_CENTIMETERS = "cm"

MIN_HEIGHT_INCHES = 59
MAX_HEIGHT_INCHES = 76

MIN_HEIGHT_CENTIMETERS = 150
MAX_HEIGHT_CENTIMETERS = 193

HAIR_COLOR_PREFIX = "#"

EYE_COLORS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

PASSPORT_ID_LENGTH = 9

@dataclass(frozen=True)
class Passport:
    byr: str
    iyr: str
    eyr: str
    hgt: str
    hcl: str
    ecl: str
    pid: str
    cid: Optional[str] = None

    def __post_init__(self):

        int_byr = int(self.byr)
        if int_byr < MIN_BYR or MAX_BYR < int_byr:
            raise ValueError()

        int_iyr = int(self.iyr)
        if int_iyr < MIN_IYR or MAX_IYR < int_iyr:
            raise ValueError()

        int_eyr = int(self.eyr)
        if int_eyr < MIN_EYR or MAX_EYR < int_eyr:
            raise ValueError()

        hgt_val = int(self.hgt[:-2])
        hgt_unit = self.hgt[-2:]

        valid_inches = hgt_unit == HEIGHT_UNIT_INCHES and MIN_HEIGHT_INCHES <= hgt_val <= MAX_HEIGHT_INCHES
        valid_centimeters = hgt_unit == HEIGHT_UNIT_CENTIMETERS and MIN_HEIGHT_CENTIMETERS <= hgt_val <= MAX_HEIGHT_CENTIMETERS
        if not valid_inches and not valid_centimeters:
            raise ValueError()

        # Check the prefix of the hair color. Check the color value is valid by casting to hexadecimal int
        int(self.hcl[1:], 16)
        if not self.hcl[0] == HAIR_COLOR_PREFIX:
            raise ValueError()

        if self.ecl not in EYE_COLORS:
            raise ValueError()

        if not len(self.pid) == PASSPORT_ID_LENGTH or not self.pid.isdecimal():
            raise ValueError()


def build_passport(data: Dict[str, str]) -> Optional[Passport]:
    try:
        return Passport(**data)
    except TypeError:
        # If a TypeError occurs it's because we didn't meet the requirements of a passport
        return None
    except ValueError:
        # Same as TypeError
        return None


def find_valid_passports() -> List[Passport]:

    # Iterate through file and group passwords so its one per line
    passport_data = {}
    passports = []
    with open("/app/inputs/passport_processing.txt", "r") as input_file:
        for line in input_file:

            clean_line = line.strip()
            if clean_line:
                # Split the line by whitespace. Separate the key from the val and add to a dict.
                key_vals = dict(key_val.split(":") for key_val in clean_line.split())
                # Merge the active passport data with the most recently passport data
                passport_data.update(key_vals)
            elif bool(passport_data):
                passport = build_passport(passport_data)
                passport_data = {}
                if passport:
                    passports.append(passport)

    passport = build_passport(passport_data)
    if passport:
        passports.append(passport)

    return passports


if __name__ == "__main__":
    passports = find_valid_passports()
    print("# of Valid Passports Found:", len(passports))