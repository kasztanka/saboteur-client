from enum import Enum


class Blockade(Enum):
    LAMP = 1
    PICKAXE = 2
    TRUCK = 3
    LAMP_PICKAXE = 4
    LAMP_TRUCK = 5
    PICKAXE_TRUCK = 6

    @classmethod
    def get_matching_blockades(cls, blockade):
        return list(filter(lambda b: b.name in blockade.name, list(cls)))