from typing import Dict, List

from model.equipment import Weapon, Equipment


class Stat:
    def __init__(self, max: int) -> None:
        self.max: int = max
        self.cur: int = max

    def __str__(self) -> str:
        return '{cur}/{max}'.format(**self.__dict__)


class Player:
    def __init__(self,
                 name:      str,
                 strength:  int,
                 speed:     int,
                 precision: int,
                 mental:    int
                 ) -> None:
        self.name: str = name

        self.strength:  Stat = Stat(strength)
        self.speed:     Stat = Stat(speed)
        self.precision: Stat = Stat(precision)
        self.mental:    Stat = Stat(mental)

        self.weapons: Dict[Weapon] = {}
        self.equipment: Equipment = None
        self.props: List[Equipment] = []

    def __str__(self) -> str:
        return '{name} ({strength}•{speed}•{precision}•{mental})'\
            .format(**self.__dict__)

    def details(self) -> str:
        return f'''
        === {self.name} ===
        Strength:  {self.strength}
        Speed:     {self.speed}
        Precision: {self.precision}
        Mental:    {self.mental}
        ------------
        Wields: {',\n'.join(self.weapons)}
        Wears: {self.equipment}
        {',\n'.join(self.props) if self.props else ''}
        ============
        '''  # noqa E999

    def hurt(self, damage: int) -> None:
        if self.equipment is not None:
            damage -= self.equipment.armor
        total = self.strength.cur - damage
        self.strength.cur = max(0, total)

    def heal(self, amount: int) -> None:
        total = self.strength.cur + amount
        self.strength.cur = min(self.strength.max, total)


