from enum import Enum, auto
from typing import List, Optional


class WeaponType(str, Enum):
    SHIELD = auto()
    MELEE = auto()
    PIERCING = auto()
    RANGED = auto()
    MAGIC = auto()


class Weapon:
    """A weapon that can be wielded by a player.

    Weapons deal determined damage.
    They can be either wielded with one hand or require both.
    They can have special abilities or critical effects. By default, they
    don't, and critical hits deal twice more damage.
    """

    RESOURCE_FILE = './resources/armory.json'

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


class Equipment:
    """A piece of equipment that can be worn by a player.

    Equipment can be armor, backpack, cloaks, etc.
    It can provide armor, enhance stats or grant special abilities.
    A player can only wear one equipment.
    """
    RESOURCE_FILE = './resources/equipment.json'

    def __init__(self,
                 name: str,
                 armor: int = 0,
                 abilities: str = None
                 ) -> None:
        self.name: str = name
        self.armor: int = armor
        self.abilities: Optional[str] = abilities

    def __str__(self) -> str:
        description: List[str] = [
            self.name
        ]
        if self.armor > 0:
            description.append(
                f'+{self.armor} armor'
            )
        if self.abilities is not None:
            description.append(self.abilities)

        return ', '.join(description)
