import yaml
import random


class GenericFactory:
    def __init__(self, resource_file: str, target_class: type):
        with open(resource_file, encoding="utf-8") as f:
            self._root: dict = yaml.safe_load(f)
        self.target_class = target_class

    def from_name(self, name: str, category: str):
        details: dict = self._root[category][name]

        return self.target_class(name, details)

    def random(self, category: str | None = None):
        if category is None:
            category = random.choice(list(self._root))
        name = random.choice(list(self._root[category]))

        return self.target_class(name, self._root[name])
