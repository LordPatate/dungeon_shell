from typing import Dict, List, Optional, Union

from creature import Creature, Stat
from equipment import Equipment, Weapon


class Qualifier():
    def __init__(self, name, effect) -> None:
        self.name: str = name
        self.effect: str = effect

    def __str__(self) -> str:
        return f'{self.name} {f"({self.effect})" if self.effect else ""}'


QUALIFIER_STRONG = Qualifier('strong', '+2 strength')
QUALIFIER_FAST = Qualifier('fast', '+2 speed')
QUALIFIER_SHARP = Qualifier('sharp', '+2 precision')
QUALIFIER_SMART = Qualifier('smart', '+2 mental')
QUALIFIER_LUCKY = Qualifier('lucky', '+1 luck token')

MAGIC_TYPES: Dict[str, str] = {
    'raw': 'deals X damages to a target',
    'heal': 'restores 2*X strength to a target',
    'fire': 'burns a target dealing X/2 damage for 3 turns',
    'frost': 'freezes a target of level lower or equal to X',
    'wind': 'knocks back all targets of level lower or equal to X',
    'lightning': 'deals 2*X damage to the nearest target',
    'force field': 'barrier that absorbs up to 2*X damage',
    'telekinesis': 'move around freely a target of level lower or equal to X/2',
}


class Player(Creature):
    def __init__(self,
                 name:      str,
                 strength:  int,
                 speed:     int,
                 precision: int,
                 mental:    int
                 ) -> None:
        super().__init__()

        self.name: str = name

        self.strength:  Stat = Stat(strength)
        self.speed:     Stat = Stat(speed)
        self.precision: Stat = Stat(precision)
        self.mental:    Stat = Stat(mental)

        self._qualifier: Optional[Qualifier] = None
        self.expertise: Optional[str] = None
        self.signature: Optional[str] = None

        self.weapons: List[Weapon] = []
        self._free_hands = 2
        self.equipment: Optional[Equipment] = None
        self.props: List[Equipment] = []

    def __str__(self) -> str:
        return '{name} ({strength} • {speed} • {precision} • {mental})'\
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
        Wields: {"""
          • """ + """;
          • """.join(map(str, self.weapons)) if self.weapons else "nothing"}
        Wears: {self.equipment if self.equipment else 'nothing'}
        Props: {"""
          • """ + """;
          • """.join(map(str, self.props)) if self.props else 'none'}
        {f'Signature move: {self.signature}' if self.signature else ''}
        ============
        '''

    def equip(self, weapon: Weapon) -> None:
        hands_required = 2 if weapon.two_handed else 1
        if self._free_hands < hands_required:
            raise Exception("This player cannot hold this weapon !"
                            "Use 'unequip' to ditch one of your weapons.")
        self._free_hands -= hands_required
        self.weapons.append(weapon)

    def unequip(self, weapon: Union[Weapon, int, str]) -> Optional[Weapon]:
        removed_weapon = None
        if isinstance(weapon, Weapon):
            if weapon not in self.weapons:
                raise Exception('This player is not wielding this weapon.')
            self.weapons.remove(weapon)
            removed_weapon = weapon
        elif isinstance(weapon, int):
            removed_weapon = self.weapons.pop(weapon)
        elif isinstance(weapon, str):
            for item in self.weapons:
                if item.name is weapon:
                    self.weapons.remove(item)
                    removed_weapon = item
            raise Exception('This player is not wielding any weapon with'
                            'that name.')

        self._free_hands += 2 if removed_weapon.two_handed else 1
        return removed_weapon

    def wear(self, equipment: Optional[Equipment]) -> Optional[Equipment]:
        if equipment is not None and equipment.is_prop:
            self.props.append(equipment)
            return None
        else:
            old = self.equipment
            self.equipment = equipment
            print(f'Warning: now wearing {equipment} instead of {old}.')
            return old

    def get_health(self) -> Stat:
        return self.strength

    def get_armor(self) -> int:
        total = 0
        if self.equipment is not None:
            total += self.equipment.armor
        for piece in self.props:
            total += piece.armor

        return total

    def get_stat(self, name: str) -> Stat:
        return self.__dict__[name]

    @property
    def qualifier(self) -> Optional[Qualifier]:
        return self._qualifier

    @qualifier.setter
    def qualifier(self, value: Optional[Qualifier]) -> None:
        corresponding_stat = {
            QUALIFIER_STRONG: self.strength,
            QUALIFIER_FAST: self.speed,
            QUALIFIER_SHARP: self.precision,
            QUALIFIER_SMART: self.mental
        }
        if self._qualifier is not None and \
           self._qualifier in corresponding_stat.keys():
            corresponding_stat[self._qualifier].max -= 2
        if value is not None and value in corresponding_stat.keys():
            corresponding_stat[value].max += 2
        self._qualifier = value
