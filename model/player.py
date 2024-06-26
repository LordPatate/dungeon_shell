from enum import Enum, auto
from typing import Dict, Optional, Tuple, Union

from model.consumables import Consumable
from model.creature import Creature, Stat
from model.equipment import Equipment
from model.weapons import Weapon
from utils import Container


class PlayerStat(str, Enum):
    STRENGTH = "strength"
    MOVEMENT = "movement"
    PRECISION = "precision"
    MENTAL = "mental"
    HEALTH = "health"


class Qualifier:
    _BUFF_AMOUNT = 2

    STRONG = "strong"
    AGILE = "agile"
    SHARP = "sharp"
    SMART = "smart"
    HEALTHY = "healthy"
    LUCKY = "lucky"

    corresponding_stat = {
        STRONG: PlayerStat.STRENGTH,
        AGILE: PlayerStat.MOVEMENT,
        SHARP: PlayerStat.PRECISION,
        SMART: PlayerStat.MENTAL,
        HEALTHY: PlayerStat.HEALTH,
    }

    def __init__(self, name, effect=None):
        self.name: str = name
        if effect:
            self.effect: str = effect
        else:
            if name not in Qualifier.corresponding_stat:
                raise ValueError("You must either specify an effect or use a standard qualifier name")
            self.effect = f'+{Qualifier._BUFF_AMOUNT} {Qualifier.corresponding_stat[name].name.lower()}'

    def __str__(self) -> str:
        return f'{self.name} {f"({self.effect})" if self.effect else ""}'


class Player(Creature):
    """A playable character.

    Starts with 10 health. Considered as a level 4 creature.
    Playable characters have 4 other stats:
    * Strength
    * Movement
    * Precision
    * Mental
    A qualifier should be given to them.
    They can wield weapons, wear equipment and carry consumables.
    They can get an expertise and a signature.
    """
    def __init__(self, name: str, *stat_order: Tuple[str, str, str, str]):
        super().__init__(name, level=4)

        stats: Dict[PlayerStat, Stat] = dict()
        stat_order = map(PlayerStat, stat_order)
        for stat, value in zip(stat_order, (15, 12, 9, 6)):
            stats[stat] = Stat(value)
        self.strength = stats[PlayerStat.STRENGTH]
        self.movement = stats[PlayerStat.MOVEMENT]
        self.precision = stats[PlayerStat.PRECISION]
        self.mental = stats[PlayerStat.MENTAL]

        stats[PlayerStat.HEALTH] = Stat(10)
        self.heath = stats[PlayerStat.HEALTH]

        self._qualifier: Optional[Qualifier] = None
        self.expertise: Optional[str] = None
        self.signature: Optional[str] = None

        self.weapons = Container[Weapon]()
        self._free_hands = 2
        self.equipment: Optional[Equipment] = None
        self.props: Dict[str, Equipment] = dict()
        self.quick_access_consumables = Container[Consumable]()
        self.inventory = Container[Union[Weapon, Equipment, Consumable]]()

    def __str__(self) -> str:
        return f"{self.name} ({self.strength} • {self.movement} • {self.precision} • {self.mental})"

    def details(self) -> str:
        return f'''
        === {self.name} ===
        Qualifier: {self.qualifier if self.qualifier else 'TO BE DETERMINED'}
        {f"Expertise: {self.expertise}" if self.expertise else ''}
        {f"""Signature move: {self.signature}
        ------------""" if self.signature else ''}
        Strength:  {self.strength}
        Movement:     {self.movement}
        Precision: {self.precision}
        Mental:    {self.mental}
        ------------
        Wields: {"""
          • """ + """
          • """.join(self.weapons.details()) if self.weapons else "nothing"}
        Wears: {self.equipment if self.equipment else 'nothing'}
        Props: {"""
          • """ + """
          • """.join(self.props.keys()) if self.props else 'none'}
        ------------
        Consumables: {"""
          • """ + """
          • """.join(self.quick_access_consumables.details()) if self.quick_access_consumables else "none"}
        Inventory: {"""
          • """ + """
          • """.join(self.inventory.details()) if self.inventory else "empty"}
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
            self.weapons.push(item)

    def unequip(self, item_name: str):
        """Place the specified item in this player's inventory.

        Looks for the item in this player's hands and his equipment.
        """
        if self.equipment is not None and item_name == self.equipment.name:
            removed_item = self.equipment
            self.equipment = None

        elif item_name in self.weapons:
            removed_item = self.weapons.remove(item_name)
            self._free_hands += 2 if removed_item.two_handed else 1

        else:
            raise Exception('This player is not wielding any weapon'
                            'or wearing any equipment with that name.')

        self.inventory.push(removed_item)

    def use(self, consumable_name: str):
        if consumable_name not in self.quick_access_consumables:
            raise Exception('This player does not have any consumable with that name.')
        consumable = self.quick_access_consumables.remove(consumable_name)
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

    def get_stat(self, which: PlayerStat or str) -> Stat:
        return getattr(self, which)

    @property
    def qualifier(self) -> Optional[Qualifier]:
        return self._qualifier

    @qualifier.setter
    def qualifier(self, value: Union[Qualifier, str]):
        if isinstance(value, str):
            value = Qualifier(value)
        if self._qualifier is not None and \
                self._qualifier.name in Qualifier.corresponding_stat:
            corresponding = Qualifier.corresponding_stat[self._qualifier.name]
            self.get_stat(corresponding).max -= Qualifier._BUFF_AMOUNT
        if value.name in Qualifier.corresponding_stat:
            corresponding = Qualifier.corresponding_stat[value.name]
            self.get_stat(corresponding).max += Qualifier._BUFF_AMOUNT
        self._qualifier = value
