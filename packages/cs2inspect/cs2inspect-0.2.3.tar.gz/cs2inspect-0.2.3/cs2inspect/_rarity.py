__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "19.07.2024"
__email__ = "m@hler.eu"
__status__ = "Development"


from dataclasses import dataclass


@dataclass
class Rarity:
    STOCK: int = 0
    CONSUMER_GRADE: int = 1
    INDUSTRIAL_GRADE: int = 2
    MIL_SPEC_GRADE: int = 3
    RESTRICTED: int = 4
    CLASSIFIED: int = 5
    COVERT: int = 6
    CONTRABAND: int = 7
    GOLD: int = 99


class NoRarityMatchError(Exception):
    pass


def get_rarity_from_string(rarity_str):

    for name, value in Rarity.__dict__.items():
        if not name.startswith('_') and rarity_str.upper() == name:
            return value
    raise NoRarityMatchError(f"No rarity is matching the provided name [{rarity_str}]")


def parse_rarity(rarity_input: str | int) -> int:
    if isinstance(rarity_input, int):
        # Check if the integer is in the range of defined rarity values
        if rarity_input in vars(Rarity).values():
            return rarity_input
        else:
            raise NoRarityMatchError(f"Unknown rarity value {rarity_input}")
    elif isinstance(rarity_input, str):
        return get_rarity_from_string(rarity_input)
    else:
        raise NoRarityMatchError(f"Unknown rarity_input type {type(rarity_input)}")


if __name__ == '__main__':
    exit(1)
