import json
import random
from typing import Dict, Generic, Tuple, TypeVar

from consumables import Consumable
from equipment import Equipment, Weapon
from npc import NPC

T = TypeVar('T', NPC, Weapon, Equipment, Consumable)


class Factory(Generic[T]):
    def __init__(self, json_file: str, target_class: type):
        self.json_file = json_file
        self.target_class = target_class

    def from_json(self, src: str) -> T:
        obj: Dict = json.loads(src)
        return self.target_class(**obj)

    def from_name(self, category: str, name: str) -> T:
        with open(self.json_file) as f:
            root: Dict = json.load(f)

        obj: Dict = root[category][name]

        return self.target_class(name, **obj)

    def random(self, category: str = None) -> T:
        with open(self.json_file) as f:
            root: Dict = json.load(f)

        if category is None:
            candidates: Dict = random.choice(list(root.values()))
        else:
            candidates: Dict = root[category]

        tuple: Tuple[str, Dict] = random.choice(list(candidates.items()))
        name, obj = tuple

        return self.target_class(name, **obj)
