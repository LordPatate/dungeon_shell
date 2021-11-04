from typing import Optional, Union

from model.creature import Creature, Stat


class NPC(Creature):
    """A Non Playable Character.

    NPCs are labelled with a level that gives a general idea of their power.
    A higher level generally means the NPC can deal more damage and has more
    health. By default, its damage is equal to its level; and it has 3 times
    more health.
    """

    RESOURCE_FILE = "./resources/bestiary.json"

    def __init__(self,
                 name: str,
                 level: int,
                 damage: int = -1,
                 health: Union[Stat, int] = None,
                 armor: int = 0,
                 abilities: str = None
                 ) -> None:
        super().__init__(name)
        self.level: int = level
        self.damage: int = level if damage == -1 else damage
        if isinstance(health, int):
            health = Stat(health)
        self.health: Stat = Stat(level * 3) if health is None else health
        self.armor: int = armor
        self.abilities: Optional[str] = abilities

    def __str__(self) -> str:
        if self.health.cur == 0:
            return f'[{self.level}] {self.name}: DEAD'
        summary = f'[{self.level}] {self.name}: {self.health}'
        details = []
        if self.damage != self.level:
            details.append(f'{self.damage} damage')
        if self.armor > 0:
            details.append(f'{self.armor} armor')
        if self.abilities is not None:
            details.append(f'abilities: {self.abilities}')

        return f'{summary} ({", ".join(details)})' if details else summary

    def get_health(self) -> Stat:
        return self.health

    def get_armor(self) -> int:
        return self.armor
