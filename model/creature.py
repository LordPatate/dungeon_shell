class Stat:
    def __init__(self, max: int) -> None:
        self.max: int = max
        self.cur: int = max

    def __str__(self) -> str:
        return '{cur}/{max}'.format(**self.__dict__)


class Creature:
    def get_health(self) -> Stat:
        raise NotImplementedError()

    def get_armor(self) -> int:
        raise NotImplementedError()

    def hurt(self, damage: int):
        health = self.get_health()
        armor = self.get_armor()
        damage = max(0, damage - armor)
        health.cur = max(0, health.cur - damage)

    def heal(self, amount: int):
        health = self.get_health()
        health.cur = min(
            health.max,
            health.cur + amount)
