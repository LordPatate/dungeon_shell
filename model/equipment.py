from typing import List, Optional, Union


class Weapon:
    RESOURCE_FILE = 'resources/armory.json'

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
    RESOURCE_FILE = 'resources/equipment.json'

    def __init__(self,
                 name: str,
                 is_prop: bool,
                 armor: int = 0,
                 capacity: int = 0,
                 abilities: str = None
                 ) -> None:
        self.name: str = name
        self.is_prop: bool = is_prop
        self.armor: int = armor
        self.capacity: int = capacity
        self.abilities: Optional[str] = abilities

    def __str__(self) -> str:
        description: List[str] = [
            self.name
        ]
        if self.armor > 0:
            description.append(
                f'+{self.armor} armor'
            )
        if self.capacity > 0:
            description.append(
                f'allows to carry {self.capacity} more items'
            )
        if self.abilities is not None:
            description.append(self.abilities)

        return ', '.join(description)
