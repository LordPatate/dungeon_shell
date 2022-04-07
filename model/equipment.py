from typing import List, Optional


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
