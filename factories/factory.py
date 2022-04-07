import json
import random
from typing import Tuple


class GenericFactory:
    def __init__(self, json_file: str, target_class: type):
        with open(json_file) as f:
            self._root: dict = json.load(f)
        self.target_class = target_class

    def from_name(self, name: str, category: str):
        details: dict = self._root[category][name]

        return self.target_class(name, details)

    def random(self, category: str = None):
        if category is None:
            candidates: dict = random.choice(list(self._root.values()))
        else:
            candidates = self._root[category]

        _tuple: Tuple[str, dict] = random.choice(list(candidates.items()))
        name, details = _tuple

        return self.target_class(name, details)
