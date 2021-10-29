import json
import random

from typing import Dict

from factories.factory import GenericFactory
from model.consumables import Consumable


class BombFactory(GenericFactory):
    RESOURCE_FILE = Consumable.RESOURCE_FILE
    CATEGORY_NAME = 'bombs'

    def __init__(self):
        super().__init__(BombFactory.RESOURCE_FILE, Consumable)

    def from_name(self, name: str, _ = None) -> Consumable:
        return super().from_name(name, BombFactory.CATEGORY_NAME)

    def random(self):
        return super().random(category=BombFactory.CATEGORY_NAME)


class ScrollFactory():
    RESOURCE_FILE = '../resources/magic.json'
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
        magic_type = random.choice(self.magic_types.keys())

        return self.from_magic_type(magic_type)
