from typing import List


class Weapon:
    def __init__(self,
                 name: str,
                 damage: int,
                 critical: str = None,
                 abilities: str = None
                 ) -> None:
        self.name = name
        self.damage = damage
        self.critical = damage * 2 if critical is None else critical
        self.abilities = abilities

    def __str__(self) -> str:
        description: List[str] = [
            self.name,
            f'{self.damage} damage (critical: {self.critical})'
        ]
        if self.abilities is not None:
            description.append(self.abilities)

        return ', '.join(description)


class Equipment:
    def __init__(self,
                 name: str,
                 prop: bool,
                 armor: int = 0,
                 capacity: int = 0,
                 abilities: str = None
                 ) -> None:
        self.name: str = name
        self.prop: bool = prop
        self.armor: int = armor
        self.capacity: int = capacity
        self.abilities: str = abilities

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
