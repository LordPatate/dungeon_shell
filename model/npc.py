import json
from typing import Optional, Union

from creature import Creature, Stat

BESTIARY_FILENAME = "resources/bestiary.json"


class NPC(Creature):
    def __init__(self,
                 name: str,
                 level: int,
                 damage: int = -1,
                 health: Union[Stat, int] = None,
                 armor: int = 0,
                 abilities: str = None
                 ) -> None:
        super().__init__()
        self.name: str = name
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

        return f'{summary} ({", ".join(details)})' if details else summary

    def get_health(self) -> Stat:
        return self.health

    def get_armor(self) -> int:
        return self.armor


class NPCFactory:
    @staticmethod
    def from_json(src: str) -> NPC:
        obj = json.loads(src)
        return NPC(**obj)

    @staticmethod
    def monster(name: str) -> NPC:
        with open(BESTIARY_FILENAME) as f:
            root = json.load(f)

        for monster in root['monsters']:
            if monster['name'] == name:
                return NPC(**monster)

        raise ValueError(f'No monster named {name} in bestiary.')
