import json


class Factory:
    def __init__(self, json_file: str, target_class: type):
        self.json_file = json_file
        self.target_class = target_class

    def from_json(self, src: str):
        obj = json.loads(src)
        return self.target_class(**obj)

    def from_name(self, category: str, name: str):
        with open(self.json_file) as f:
            root = json.load(f)

        obj = root[category][name]

        return self.target_class(name, **obj)
