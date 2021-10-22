class Stat:
    def __init__(self, max: int) -> None:
        self.max: int = max
        self._cur: int = max

    def __str__(self) -> str:
        return '{cur}/{max}'.format(**self.__dict__)

    @property
    def cur(self) -> int:
        return self._cur

    @cur.setter
    def cur(self, value: int) -> None:
        self._cur = max(0, min(self.max, value))


class Creature:
    def get_health(self) -> Stat:
        raise NotImplementedError()

    def get_armor(self) -> int:
        raise NotImplementedError()

    def hurt(self, damage: int):
        health = self.get_health()
        armor = self.get_armor()
        damage = max(0, damage - armor)
        health.cur -= damage

    def heal(self, amount: int):
        health = self.get_health()
        health.cur += amount
