from typing import List, Optional, Union


class Weapon:
    """A weapon that can be wielded by a player.

    Weapons deal determined damage.
    They can be either wielded with one hand or require both.
    They can have special abilities or critical effects. By default, they
    don't, and critical hits deal twice more damage.
    """

    RESOURCE_FILE = './resources/armory.json'

    def __init__(self,
                 name: str,
                 damage: int,
                 two_handed: bool = False,
                 critical: Union[str, int] = None,
                 abilities: str = None
                 ) -> None:
        self.name = name
        self.two_handed = two_handed
        self.damage = damage
        self.critical = damage * 2 if critical is None else critical
        self.abilities = abilities

    def __str__(self) -> str:
        description: List[str] = [
            self.name
        ]
        if self.damage != 0:
            description.append(f'{self.damage} damage')
        if self.critical != 0:
            description.append(f' (critical: {self.critical})')
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
