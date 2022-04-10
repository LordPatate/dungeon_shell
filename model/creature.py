import functools
from typing import Callable, List


@functools.total_ordering
class Stat:
    """A stat pool, with a maximum amount and a current value.

    Attributes:
    * max: The maximum amount of points in this stat
    * cur: The current 'remaining' points in this stat
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, max: int) -> None:
        self._max: int = max
        self._cur: int = max

    def __str__(self) -> str:
        return f'{self.cur}/{self.max}'

    def __bool__(self) -> bool:
        return self.cur > 0

    def __int__(self) -> int:
        return self.cur

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

    def __iadd__(self, value: int) -> "Stat":
        self.cur += value
        return self

    def __isub__(self, value: int) -> "Stat":
        return self.__iadd__(-value)

    def __eq__(self, other: int or "Stat") -> bool:
        return int(self) == other

    def __lt__(self, other: int or "Stat") -> bool:
        return int(self) < other


class Creature:
    """A creature that can be hurt, healed and killed."""

    def __init__(self, name, level):
        self.name: str = name
        self.level: int = level
        self._on_death_listeners: List[Callable] = []

    def hurt(self, damage: int):
        """Deal <damage> to this creature.

        The creature's armor is taken into account to reduce
        the damage actually inflicted.
        self.die() is called if health reaches 0.
        """
        health = self.get_health()
        armor = self.get_armor()
        damage = max(0, damage - armor)
        health.cur -= damage
        if health.cur == 0:
            self._die()

    def _die(self):
        """Call on death listeners."""
        for listener in self._on_death_listeners:
            listener()

    def heal(self, amount: int):
        """Restores <amount> health to this creature."""
        health = self.get_health()
        if health.cur == 0:
            raise Exception('Cannot heal a dead creature')
        health.cur += amount

    def add_on_death_listener(self, listener: Callable) -> None:
        """Adds <listener> to the list of on-death-listeners.

        Registers the given callable as one of those that would be called
        should this creatures die (i.e. its health reaches 0).
        """
        self._on_death_listeners.append(listener)

    def is_alive(self) -> bool:
        return self.get_health().cur > 0

    def is_hurt(self) -> bool:
        return self.is_alive() and self.get_health().cur < self.get_health().max

    def get_health(self) -> Stat:
        raise NotImplementedError()

    def get_armor(self) -> int:
        raise NotImplementedError()
