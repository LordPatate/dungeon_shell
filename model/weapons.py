from enum import Enum
from typing import List


class WeaponType(str, Enum):
    SHIELD = "shield"
    MELEE = "melee"
    PIERCING = "piercing"
    RANGED = "ranged"
    MAGIC = "magic"


class Weapon:
    """A weapon that can be wielded by a player.

    Weapons deal determined damage.
    They can be either wielded with one hand or require both.
    They can have special abilities or critical effects. By default, they
    don't, and critical hits deal twice more damage.
    """

    RESOURCE_FILE = './resources/weapons.yaml'

    def __init__(self, name: str, details: dict):
        self.name = name
        self.type = WeaponType(details["type"])
        self.two_handed = details.get("two_handed", False)
        self.abilities = details.get("abilities")
        self.block = details.get("block", 0)
        self.damage = details.get("damage", 0)
        self.critical = details.get("critical", self.damage * 2)
        self.spell_level = details.get("spell level", 0)
        self.reload = details.get("reload", 0)

    def __str__(self) -> str:
        description: List[str] = [
            self.name,
            self.type
        ]
        if self.two_handed:
            description.append("two handed")
        stats = ("block", "damage", "critical", "spell_level", "reload", "abilities")
        for stat in stats:
            value = getattr(self, stat)
            if value:
                description.append(f"{stat}: {value}")
        if self.abilities is not None:
            description.append(self.abilities)

        return ', '.join(description)

