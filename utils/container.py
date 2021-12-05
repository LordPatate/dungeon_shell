from typing import Dict, Generic, List, TypeVar

T = TypeVar('T')


class Container(Generic[T]):
    def __init__(self):
        self.holder: Dict[str, List[T]] = dict()

    def push(self, e: T):
        if e.name not in self.holder:
            self.holder[e.name] = []
        self.holder[e.name].append(e)

    def remove(self, name: str) -> T:
        e = self.holder[name].pop()
        if self.holder[name] == []:
            self.holder.pop(name)
        return e

    def details(self) -> List[str]:
        return [
            f'{len(category)} {name}'
            for name, category in self.holder.items()
        ]

    def __bool__(self):
        return bool(self.holder)

    def __iter__(self):
        return iter(self.holder)
