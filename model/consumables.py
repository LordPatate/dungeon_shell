import json
from enum import Enum, auto

from creature import Creature
from model.npc import NPCFactory
from npc import NPC
from player import MAGIC_TYPES, Player


class Consumable:
    def __init__(self):
        self.depleted = False

    def __str__(self) -> str:
        raise NotImplementedError()

    def use(self) -> None:
        if self.depleted:
            raise Exception('This item is depleted and cannot be used.')
        self.depletes()

    def depletes(self):
        self.depleted = True


class PotionType(Enum):
    SPECIAL = 0
    STRENGTH = auto()
    SPEED = auto()
    PRECISION = auto()
    MENTAL = auto()


class Potion(Consumable):
    HEAL_AMOUNT = 6

    def __init__(self, kind: PotionType, effect: str = None):
        super().__init__()
        if kind is PotionType.SPECIAL:
            if effect is None:
                raise ValueError(f'You must specify an effect for {PotionType.SPECIAL.name} potions.')
        else:
            if effect is not None:
                raise ValueError(f'Only {PotionType.SPECIAL.name} potions can have an effect.')
        self.kind = kind
        self.effect = effect

    def __str__(self) -> str:
        name = self.kind.name
        if self.kind is PotionType.SPECIAL:
            return f'{name.capitalize()} potion: {self.effect}'
        else:
            return f'{name.capitalize()} potion (restores up to {Potion.HEAL_AMOUNT} {name})'

    def use(self, target: Creature = None) -> None:
        super().use()
        if target is None:
            raise ValueError("'target' argument required for potions")
        if isinstance(target, Player):
            target.get_stat(self.kind.name.lower()).cur += Potion.HEAL_AMOUNT
        else:
            target.heal(Potion.HEAL_AMOUNT)


class Bomb(Consumable):
    def __init__(self, kind: str, effect: str):
        super().__init__()
        self.kind = kind
        self.effect = effect

    def __str__(self) -> str:
        return '{kind} bomb: {effect}'.format(**self.__dict__)


class Scroll(Consumable):
    POWER_LEVEL = 4

    def __init__(self, magic_type: str) -> None:
        super().__init__()
        self.magic_type = magic_type

    def __str__(self) -> str:
        return f'{self.magic_type} scroll: \
            {MAGIC_TYPES[self.magic_type].replace("X", str(Scroll.POWER_LEVEL))}'


class SummonningStone(Consumable):
    def __init__(self, creature: NPC):
        super().__init__()
        self.creature = creature
        self.creature.add_on_death_listener(self.depletes)

    def __str__(self) -> str:
        return f'summons: {self.creature}'

    def use(self) -> None:
        if self.depleted:
            raise Exception(f"This stone's {self.creature.name} is dead and cannot be summoned again.")


class ConsumableFactory:
    @staticmethod
    def potion_from_json(src: str) -> Potion:
        obj = json.loads(src)
        return Potion(PotionType.SPECIAL, obj["effect"])

    @staticmethod
    def bomb_from_json(src: str) -> Bomb:
        obj = json.loads(src)
        return Bomb(**obj)

    @staticmethod
    def summoning_stone_from_json(src: str) -> SummonningStone:
        obj = json.loads(src)
        return SummonningStone(NPCFactory.from_json(**obj))
