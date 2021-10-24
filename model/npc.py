from typing import Optional
from model.creature import Stat, Creature


class NPC(Creature):
    def __init__(self,
                 name: str,
                 level: int,
                 damage: int = -1,
                 health: Stat = None,
                 armor: int = 0,
                 abilities: str = None
                 ) -> None:
        super().__init__()
        self.name: str = name
        self.level: int = level
        self.damage: int = level if damage == -1 else damage
        self.health: Stat = Stat(level * 3) if health is None else health
        self.armor: int = armor
        self.abilities: Optional[str] = abilities

    def __str__(self) -> str:
        summary = '[{level}] {name}: {health}'.format(**self.__dict__)
        details = []
        if self.damage != self.level:
            details.append(f'{self.damage} damage')
        if self.armor > 0:
            details.append(f'{self.armor} armor')

        return f'{summary} ({", ".join(details)})' if details else summary

    def get_health(self) -> Stat:
        return self.health

    def get_armor(self) -> int:
        return self.armor
