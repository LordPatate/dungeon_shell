from model.player import Stat


class Creature:
    def __init__(self,
                 name: str,
                 level: int,
                 damage: int = -1,
                 health: Stat = None,
                 armor: int = 0,
                 abilities: str = None
                 ) -> None:
        self.name: str = name
        self.level: int = level
        self.damage: int = level if damage == -1 else damage
        self.health: Stat = Stat(level * 3) if health is None else health
        self.armor: int = armor
        self.abilities: str = abilities

    def __str__(self) -> str:
        summary = '[{level}] {name}: {health}'.format(**self.__dict__)
        details = []
        if self.damage != self.level:
            details.append(f'{self.damage} damage')
        if self.armor > 0:
            details.append(f'{self.armor} armor')

        return f'{summary} ({", ".join(details)})' if details else summary

    def hurt(self, damage: int):
        damage = max(0, damage - self.armor)
        self.health.cur = max(0, self.health.cur - damage)

    def heal(self, amount: int):
        self.health.cur = min(
            self.health.max,
            self.health.cur + amount)
