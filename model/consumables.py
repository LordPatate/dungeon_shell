from enum import Enum, auto
from typing import Dict, List

from creature import Creature
from model.npc import NPC
from model.player import MAGIC_TYPES
from player import Player


class Consumable:
    def __init__(self):
        self.depleted = False

    def __str__(self) -> str:
        raise NotImplementedError()

    def use(self) -> None:
        if self.depleted:
            raise Exception('This item is depleted and cannot be used.')
        self.depleted = True


class PotionType(Enum):
    STRENGTH = auto()
    SPEED = auto()
    PRECISION = auto()
    MENTAL = auto()


class Potion(Consumable):
    HEAL_AMOUNT = 6

    def __init__(self, kind: PotionType):
        super().__init__()
        self.kind = kind

    def __str__(self) -> str:
        stat = self.kind.name
        return f'{stat.capitalize()} potion (restores up to {Potion.HEAL_AMOUNT} {stat})'

    def use(self, target: Creature = None) -> None:
        super().use()
        if target is None:
            raise ValueError("'target' argument required for potions")
        if isinstance(target, Player):
            target.__dict__[self.kind.name.lower()] += Potion.HEAL_AMOUNT
        else:
            target.heal(Potion.HEAL_AMOUNT)


class Bomb(Consumable):
    STANDARD_KINDS: Dict[str, str] = {
        'classic': 'explodes dealing 8 damage at point of impact '
                   'and 4 in a small area ; causes minor destruction',
        'shrapnel': 'shatter into plenty of small sharp pieces of glass and metal, '
                    'dealing 6 damage to all creatures in a large radius',
        'smoke': 'produce a thick smoke screen big enough to fill a small room',
        'flash': 'emits a flash of brilliant light, '
                 'blinding for several seconds anyone looking at it',
        'poison': 'liberates a toxic cloud gas that dissipates quickly, '
                  'poisoning all creatures in a large radius',
        'flame': 'spill ignated flammable oil all targets within a small radius, '
                 'dealing them 4 damage each turn',
    }

    def __init__(self, kind: str, effect: str):
        self.kind = kind
        self.effect = effect

    def __str__(self) -> str:
        return '{kind} bomb: {effect}'.format(**self.__dict__)


class Scroll(Consumable):
    POWER_LEVEL = 4

    def __init__(self, magic_type: str) -> None:
        self.magic_type = magic_type

    def __str__(self) -> str:
        return f'{self.magic_type} scroll: \
            {MAGIC_TYPES[self.magic_type].replace("X", str(Scroll.POWER_LEVEL))}'


class SummonningStone(Consumable):
    STANDARD_CREATURES: List[NPC] = [
        NPC('fairy', level=1, damage=0, abilities='heal (2)'),
        NPC('imp', level=2, damage=5, health=3),
        NPC('phoenix', level=3),
        NPC('elemental', level=4),
        NPC('undead knight', level=5, health=12, armor=3),
        NPC('golem', level=6, health=10, armor=10),
    ]

    def __init__(self, creature: NPC):
        self.creature = creature

    def __str__(self) -> str:
        return f'summons: {self.creature}'

    def use(self) -> None:
        if self.depleted:
            raise Exception(f"This stone's {self.creature.name} is dead and cannot be summoned again.")
