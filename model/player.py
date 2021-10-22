from typing import List, Optional

from model.creature import Creature, Stat
from model.equipment import Equipment, Weapon


class Qualifier():
    def __init__(self, name, effect) -> None:
        self.name: str = name
        self.effect: str = effect
    
    def __str__(self) -> str:
        return f'{self.name} {f"({self.effect})" if self.effect else ""}'

STRONG = Qualifier('strong', '+2 strength')
FAST = Qualifier('fast', '+2 speed')
SHARP = Qualifier('sharp', '+2 precision')
SMART = Qualifier('smart', '+2 mental')
LUCKY = Qualifier('lucky', '+1 luck token')


class Player(Creature):
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

        self._qualifier: Optional[Qualifier] = None
        self.expertise: Optional[str] = None
        self.signature: Optional[str] = None

        self.weapons: List[Weapon] = []
        self.equipment: Optional[Equipment] = None
        self.props: List[Equipment] = []

    def __str__(self) -> str:
        return '{name} ({strength}•{speed}•{precision}•{mental})'\
            .format(**self.__dict__)

    def details(self) -> str:
        return f'''
        === {self.name} ===
        Qualifier: {self.qualifier if self.qualifier else 'TO BE DETERMINED'}
        {f"""Expertise: {self.expertise}
        ------------""" if self.expertise else ''}
        Strength:  {self.strength}
        Speed:     {self.speed}
        Precision: {self.precision}
        Mental:    {self.mental}
        ------------
        Wields: {""",
        """.join(self.weapons)}
        Wears: {self.equipment if self.equipment else 'nothing'}
        {""",
        """.join(self.props) if self.props else ''}
        {f'Signature move: {self.signature}' if self.signature else ''}
        ============
        '''

    def get_health(self) -> Stat:
        return self.strength

    def get_armor(self) -> int:
        total = 0
        if self.equipment is not None:
            total += self.equipment.armor
        for piece in self.props:
            total += piece.armor

        return total

    @property
    def qualifier(self) -> Optional[Qualifier]:
        return self._qualifier
    
    @qualifier.setter
    def qualifier(self, value: Optional[Qualifier]) -> None:
        corresponding_stat = {
            STRONG: self.strength,
            FAST: self.speed,
            SHARP: self.precision,
            SMART: self.mental
        }
        if self._qualifier is not None and self._qualifier in corresponding_stat.keys():
            corresponding_stat[self._qualifier].max -= 2
        if value is not None and value in corresponding_stat.keys():
            corresponding_stat[value].max += 2
        self._qualifier = value
