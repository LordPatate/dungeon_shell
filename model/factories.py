import json
import random
from typing import Dict, Tuple


class Factory:
    def __init__(self, json_file: str, target_class: type):
        self.json_file = json_file
        self.target_class = target_class

    def from_json(self, src: str):
        obj: Dict = json.loads(src)
        return self.target_class(**obj)

    def from_name(self, category: str, name: str):
        with open(self.json_file) as f:
            root: Dict = json.load(f)

        obj: Dict = root[category][name]

        return self.target_class(name, **obj)

    def random(self, category: str = None):
        with open(self.json_file) as f:
            root: Dict = json.load(f)

        if category is None:
            candidates: Dict = random.choice(list(root.values()))

        tuple: Tuple[str, Dict] = random.choice(list(candidates.items()))
        name, obj = tuple

        return self.target_class(name, **obj)
