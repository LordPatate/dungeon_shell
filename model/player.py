import logging
from enum import Enum, auto
from typing import List, Optional, Union

from model.creature import Creature, Stat
from model.equipment import Equipment, Weapon


class PlayerStat(Enum):
    STRENGTH = auto()
    SPEED = auto()
    PRECISION = auto()
    MENTAL = auto()


class Qualifier:
    STRONG = 'strong'
    FAST = 'fast'
    SHARP = 'sharp'
    SMART = 'smart'
    LUCKY = 'lucky'

    def __init__(self, name, effect) -> None:
        self.name: str = name
        self.effect: str = effect

    def __str__(self) -> str:
        return f'{self.name} {f"({self.effect})" if self.effect else ""}'


class Player(Creature):
    """A playable character.

    Starts with 10 health.
    Playable characters have 4 other stats:
    * Strength
    * Speed
    * Precision
    * Mental
    A qualifier should be given to them.
    They can wield weapons, wear equipment and carry consumables.
    They can get an expertise and a signature.
    """
    def __init__(self,
                 name:      str,
                 strength:  int,
                 speed:     int,
                 precision: int,
                 mental:    int
                 ) -> None:
        super().__init__(name)
        self.heath = Stat(10)

        self.strength = Stat(strength)
        self.speed = Stat(speed)
        self.precision = Stat(precision)
        self.mental = Stat(mental)

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
        """Equip the player with <weapon> if possible.

        Raises an Exception if the player's hands are full.
        """
        hands_required = 2 if weapon.two_handed else 1
        if self._free_hands < hands_required:
            raise Exception("This player cannot hold this weapon !"
                            "Use 'unequip' to ditch one of your weapons.")
        self._free_hands -= hands_required
        self.weapons.append(weapon)

    def unequip(self, weapon: Union[Weapon, int, str]) -> Optional[Weapon]:
        """Remove the specified weapon from the player's hands.

        Returns the weapon that was removed if such a weapon was in this
        player's hands.
        Warning: the returned weapon should be retrieved by the caller, else
        the object reference would be lost.
        """
        def remove_weapon() -> Weapon:
            if isinstance(weapon, Weapon):
                if weapon not in self.weapons:
                    raise Exception('This player is not wielding this weapon.')
                self.weapons.remove(weapon)
                return weapon
            elif isinstance(weapon, int):
                return self.weapons.pop(weapon)
            elif isinstance(weapon, str):
                for item in self.weapons:
                    if item.name is weapon:
                        self.weapons.remove(item)
                        return item
                raise Exception('This player is not wielding any weapon with'
                                'that name.')
        removed_weapon = remove_weapon()

        self._free_hands += 2 if removed_weapon.two_handed else 1
        return removed_weapon

    def wear(self, equipment: Optional[Equipment]) -> Optional[Equipment]:
        """Put on the specified equipment if possible.

        Replace the previous equipment which is returned.
        Passing None effectively removes any worn equipment.
        """
        old = self.equipment
        self.equipment = equipment
        logging.info(f'Warning: now wearing {equipment} instead of {old}.')
        return old

    def get_health(self) -> Stat:
        return self.heath

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
            Qualifier.STRONG: self.strength,
            Qualifier.FAST: self.speed,
            Qualifier.SHARP: self.precision,
            Qualifier.SMART: self.mental
        }
        if self._qualifier is not None and \
           self._qualifier.name in corresponding_stat.keys():
            corresponding_stat[self._qualifier.name].max -= 2
        if value is not None and value.name in corresponding_stat.keys():
            corresponding_stat[value.name].max += 2
        self._qualifier = value
