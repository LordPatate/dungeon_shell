import json
import random
from typing import Dict, Tuple


class GenericFactory:
    def __init__(self, json_file: str, target_class: type):
        with open(json_file) as f:
            self.root: Dict = json.load(f)
        self.target_class = target_class

    def from_json(self, src: str):
        obj: Dict = json.loads(src)
        return self.target_class(**obj)

    def from_name(self, name: str, category: str):
        obj: Dict = self.root[category][name]

        return self.target_class(name, **obj)

    def random(self, category: str = None):
        if category is None:
            candidates: Dict = random.choice(list(self.root.values()))
        else:
            candidates = self.root[category]

        tuple: Tuple[str, Dict] = random.choice(list(candidates.items()))
        name, obj = tuple

        return self.target_class(name, **obj)
