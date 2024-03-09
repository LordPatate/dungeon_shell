from typing import Optional, Union

from model.creature import Creature, Stat


class NPC(Creature):
    """A Non Playable Character.

    NPCs are labelled with a level that gives a general idea of their power.
    A higher level generally means the NPC can deal more damage and has more
    health. By default, its damage is equal to its level; and it has 3 times
    more health.
    """

    RESOURCE_FILE = "./resources/npcs.yaml"

    def __init__(self, name: str, details: dict):
        level = details["level"]
        super().__init__(name, level)
        self.damage = details.get("damage", level)
        self.health = Stat(details.get("health", level * 3))
        self.armor = details.get("armor", 0)
        self.abilities = details.get("abilities")

    def __str__(self) -> str:
        health = self.health or "DEAD"
        description = [
            f"[{self.level}] {self.name}: {health}",
        ]
        for stat in ("damage", "armor",):
            value = getattr(self, stat)
            if value:
                description.append(f"{stat}: {value}")
        if self.abilities is not None:
            description.append(self.abilities)

        return ", ".join(description)

    def get_health(self) -> Stat:
        return self.health

    def get_armor(self) -> int:
        return self.armor
