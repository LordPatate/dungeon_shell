from typing import Callable, List


class Stat:
    def __init__(self, max: int) -> None:
        self._max: int = max
        self._cur: int = max

    def __str__(self) -> str:
        return f'{self.cur}/{self.max}'

    @property
    def cur(self) -> int:
        return self._cur

    @cur.setter
    def cur(self, value: int) -> None:
        self._cur = max(0, min(self._max, value))

    @property
    def max(self) -> int:
        return self._max

    @max.setter
    def max(self, value: int) -> None:
        if value > self._max:
            self._cur += (value - self._max)
        elif value < self._cur:
            self._cur = value

        self._max = max(0, value)


class Creature:
    def __init__(self):
        self._on_death_listeners: List[Callable] = []

    def hurt(self, damage: int):
        health = self.get_health()
        armor = self.get_armor()
        damage = max(0, damage - armor)
        health.cur -= damage
        if health.cur == 0:
            self.die()

    def die(self):
        for listener in self._on_death_listeners:
            listener()

    def heal(self, amount: int):
        health = self.get_health()
        health.cur += amount

    def add_on_death_listener(self, listener: Callable) -> None:
        self._on_death_listeners.append(listener)

    def get_health(self) -> Stat:
        raise NotImplementedError()

    def get_armor(self) -> int:
        raise NotImplementedError()
