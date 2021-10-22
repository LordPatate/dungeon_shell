from typing import List, Optional

from model.creature import Creature, Stat
from model.equipment import Equipment, Weapon


class Player(Creature):
    def __init__(self,
                 name:      str,
                 strength:  int,
                 speed:     int,
                 precision: int,
                 mental:    int
                 ) -> None:
        self.name: str = name

        self.expertise: Optional[str] = None
        self.signature: Optional[str] = None

        self.strength:  Stat = Stat(strength)
        self.speed:     Stat = Stat(speed)
        self.precision: Stat = Stat(precision)
        self.mental:    Stat = Stat(mental)

        self.weapons: List[Weapon] = []
        self.equipment: Equipment = None
        self.props: List[Equipment] = []

    def __str__(self) -> str:
        return '{name} ({strength}•{speed}•{precision}•{mental})'\
            .format(**self.__dict__)

    def details(self) -> str:
        return f'''
        === {self.name} ===
        {f"""Expertise: {self.expertise}
        ------------""" if self.expertise else ''}
        Strength:  {self.strength}
        Speed:     {self.speed}
        Precision: {self.precision}
        Mental:    {self.mental}
        ------------
        Wields: {""",
        """.join(self.weapons)}
        Wears: {self.equipment if self.equipment else "nothing"}
        {""",
        """.join(self.props) if self.props else ''}
        {f"Signature move: {self.signature}" if self.signature else ''}
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
