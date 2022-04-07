import json
import random


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
            category = random.choice(list(self._root))
        name = random.choice(list(self._root[category]))

        return self.target_class(name, self._root[name])
