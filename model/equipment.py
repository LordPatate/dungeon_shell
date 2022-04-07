from typing import List


class Equipment:
    """A piece of equipment that can be worn by a player.

    Equipment can be armor, backpack, cloaks, etc.
    It can provide armor, enhance stats or grant special abilities.
    A player can only wear one equipment.
    """
    RESOURCE_FILE = './resources/equipment.json'

    def __init__(self, name: str, details: dict):
        self.name: str = name
        self.abilities = details.get("abilities")
        self.armor = details.get("armor", 0)
        self.stealth = details.get("stealth", 0)
        self.dodge = details.get("dodge", 0)

    def __str__(self) -> str:
        description: List[str] = [
            self.name
        ]
        if self.armor > 0:
            description.append(f'armor: {self.armor}')
        stats = ("stealth", "dodge",)
        for stat in stats:
            value = getattr(self, stat)
            if value:
                description.append(f"+{value} to {stat} rolls")
        if self.abilities is not None:
            description.append(self.abilities)

        return ', '.join(description)
