import json
import random

from typing import Dict

from factories.factory import GenericFactory
from model.consumables import Consumable, HealingPotion, SummoningStone
from model.player import PlayerStat


class ConsumableFactory(GenericFactory):
    def random(self, _=None):
        pass  # TODO


class PotionFactory(GenericFactory):
    CATEGORY_SPECIAL = 'special potions'

    def __init__(self):
        super().__init__(Consumable.RESOURCE_FILE, Consumable)

    # noinspection PyMethodMayBeStatic
    def healing(self) -> HealingPotion:
        return HealingPotion()

    def from_name(self, name: str, _=None) -> Consumable:
        return super().from_name(name, PotionFactory.CATEGORY_SPECIAL)

    def get_special_names(self):
        return self._root[PotionFactory.CATEGORY_SPECIAL].keys()

    def random_special(self) -> Consumable:
        return super().random(category=PotionFactory.CATEGORY_SPECIAL)


class BombFactory(GenericFactory):
    CATEGORY_BOMBS = 'bombs'

    def __init__(self):
        super().__init__(Consumable.RESOURCE_FILE, Consumable)

    def from_name(self, name: str, _=None) -> Consumable:
        return super().from_name(name, BombFactory.CATEGORY_BOMBS)

    def get_bomb_names(self):
        return self._root[BombFactory.CATEGORY_BOMBS].keys()

    def random(self, _=None):
        return super().random(category=BombFactory.CATEGORY_BOMBS)


class ScrollFactory:
    RESOURCE_FILE = './resources/magic.json'
    POWER_LEVEL = 4

    def __init__(self) -> None:
        with open(ScrollFactory.RESOURCE_FILE) as f:
            self.magic_types: Dict[str, str] = json.load(f)

    def from_magic_type(self, magic_type: str):
        name = f'{magic_type} scroll'
        effect = self.magic_types[magic_type]\
            .replace("X", str(ScrollFactory.POWER_LEVEL))

        return Consumable(name, effect)

    def random(self):
        magic_type = random.choice(list(self.magic_types.keys()))

        return self.from_magic_type(magic_type)


class SummoningStoneFactory:
    CATEGORY_SUMMONABLES = 'summonables'

    def __init__(self, npc_factory: GenericFactory):
        self._npc_factory = npc_factory

    def from_creature_name(self, creature_name: str):
        creature = self._npc_factory.from_name(
            creature_name,
            SummoningStoneFactory.CATEGORY_SUMMONABLES
        )
        return SummoningStone(creature)
