from enum import Enum, auto
from typing import Optional, Union, Dict, List

from model.consumables import Consumable
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

    def __init__(self, name, effect):
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
                 ):
        super().__init__(name)
        self.heath = Stat(10)

        self.strength = Stat(strength)
        self.speed = Stat(speed)
        self.precision = Stat(precision)
        self.mental = Stat(mental)

        self._qualifier: Optional[Qualifier] = None
        self.expertise: Optional[str] = None
        self.signature: Optional[str] = None

        self.weapons: Dict[str, List[Weapon]] = dict()
        self._free_hands = 2
        self.equipment: Optional[Equipment] = None
        self.props: Dict[str, Equipment] = dict()
        self.quick_access_consumables: Dict[str, List[Consumable]] = dict()
        self.inventory: Dict[str, List[Union[Weapon, Equipment, Consumable]]] = dict()

    def __str__(self) -> str:
        return '{name} ({strength} • {speed} • {precision} • {mental})'\
            .format(**self.__dict__)

    def details(self) -> str:
        return f'''
        === {self.name} ===
        Qualifier: {self.qualifier if self.qualifier else 'TO BE DETERMINED'}
        {f"Expertise: {self.expertise}" if self.expertise else ''}
        {f"""Signature move: {self.signature}
        ------------""" if self.signature else ''}
        Strength:  {self.strength}
        Speed:     {self.speed}
        Precision: {self.precision}
        Mental:    {self.mental}
        ------------
        Wields: {"""
          • """ + """;
          • """.join([
                f'{len(category)} {name}'
                for name, category in self.weapons
            ]) if self.weapons else "nothing"}
        Wears: {self.equipment if self.equipment else 'nothing'}
        Props: {"""
          • """ + """;
          • """.join(self.props.keys()) if self.props else 'none'}
        ------------
        Consumables: {"""
          • """ + """;
          • """.join([
                f'{len(category)} {name}'
                for name, category in self.quick_access_consumables
            ]) if self.quick_access_consumables else "none"}
        Inventory: {"""
          • """ + """;
          • """.join([
                f'{len(category)} {name}'
                for name, category in self.inventory
            ]) if self.inventory else "empty"}
        ============
        '''

    def equip(self, item: Union[Weapon, Equipment]):
        """Equip the player with <item> if possible, raises an exception otherwise."""
        if isinstance(item, Equipment):
            if self.equipment is not None:
                raise Exception(f"This player is already equipped with {self.equipment}."
                                "Use 'unequip' to remove it.")
            self.equipment = item

        elif isinstance(item, Weapon):
            hands_required = 2 if item.two_handed else 1
            if self._free_hands < hands_required:
                raise Exception("This player cannot hold this weapon !"
                                "Use 'unequip' to ditch one of your weapons.")
            self._free_hands -= hands_required
            if item.name not in self.weapons:
                self.weapons[item.name] = []
            self.weapons[item.name].append(item)

    def unequip(self, item_name: str):
        """Place the specified item in this player's inventory.

        Looks for the item in this player's hands and his equipment.
        """
        if self.equipment is not None and item_name == self.equipment.name:
            removed_item = self.equipment
            self.equipment = None

        elif item_name in self.weapons:
            removed_item = self.weapons[item_name].pop()
            if self.weapons[item_name] == []:
                self.weapons.pop(item_name)

            self._free_hands += 2 if removed_item.two_handed else 1

        else:
            raise Exception('This player is not wielding any weapon'
                            'or wearing any equipment with that name.')

        if item_name not in self.inventory:
            self.inventory[item_name] = []
        self.inventory[item_name].append(removed_item)

    def use(self, consumable_name: str):
        if consumable_name not in self.quick_access_consumables:
            raise Exception('This player does not have any consumable with that name.')
        consumable = self.quick_access_consumables[consumable_name].pop()
        if self.quick_access_consumables[consumable_name] == []:
            self.quick_access_consumables.pop(consumable_name)
        consumable.use()

    def get_health(self) -> Stat:
        return self.heath

    def get_armor(self) -> int:
        total = 0
        if self.equipment is not None:
            total += self.equipment.armor
        for piece in self.props.values():
            total += piece.armor

        return total

    def get_stat(self, name: str) -> Stat:
        return self.__dict__[name]

    @property
    def qualifier(self) -> Optional[Qualifier]:
        return self._qualifier

    @qualifier.setter
    def qualifier(self, value: Optional[Qualifier]):
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
