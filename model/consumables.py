import json
from typing import Dict

from creature import Creature
from npc import NPC
from player import Player, PlayerStat


class Consumable:
    RESOURCE_FILE = '../resources/consumables.json'

    def __init__(self):
        self.depleted = False

    def __str__(self) -> str:
        raise NotImplementedError()

    def use(self) -> str:
        if self.depleted:
            raise Exception('This item is depleted and cannot be used.')
        self.depletes()
        return NotImplemented

    def depletes(self):
        self.depleted = True


class Potion(Consumable):
    HEAL_AMOUNT = 6

    def __init__(self, kind: str, effect: str = None):
        super().__init__()
        self.kind = kind
        if self.is_basic():
            if effect is not None:
                raise ValueError('Only non-basic potions can have a special effect.')
        else:
            if effect is None:
                raise ValueError('You must specify an effect for non-basic potions.')
        self.effect = effect

    def __str__(self) -> str:
        if self.is_basic():
            return f'{self.kind.capitalize()} potion (restores up to {Potion.HEAL_AMOUNT} {self.kind})'
        else:
            return f'{self.kind.capitalize()} potion: {self.effect}'

    def use(self, target: Creature = None) -> str:
        super().use()
        if self.is_basic():
            if target is None:
                raise ValueError("'target' argument required for potions")
            if isinstance(target, Player):
                target.get_stat(self.kind).cur += Potion.HEAL_AMOUNT
                return f'Restored {Potion.HEAL_AMOUNT} {self.kind} to {target.name}'
            else:
                target.heal(Potion.HEAL_AMOUNT)
                return f'Healed {target.name} for {Potion.HEAL_AMOUNT} HP.'
        else:
            return self.effect  # type: ignore[return-value]

    def is_basic(self):
        return self.kind in PlayerStat.__members__.keys()


class Bomb(Consumable):
    def __init__(self, kind: str, effect: str):
        super().__init__()
        self.kind = kind
        self.effect = effect

    def __str__(self) -> str:
        return f'{self.kind.capitalize()} bomb: {self.effect}'


class Scroll(Consumable):
    POWER_LEVEL = 4
    RESOURCE_FILE = '../resources/magic.json'
    with open(RESOURCE_FILE) as f:
        MAGIC_TYPES: Dict[str, str] = json.load(f)

    def __init__(self, magic_type: str) -> None:
        super().__init__()
        self.magic_type = magic_type

    def __str__(self) -> str:
        return f'{self.magic_type} scroll: \
            {Scroll.MAGIC_TYPES[self.magic_type].replace("X", str(Scroll.POWER_LEVEL))}'


class SummonningStone(Consumable):
    def __init__(self, creature: NPC):
        super().__init__()
        self.creature = creature
        self.creature.add_on_death_listener(self.depletes)

    def __str__(self) -> str:
        return f'Summoning stone: summons {self.creature}'

    def use(self) -> str:
        if self.depleted:
            raise Exception(f"This stone's {self.creature.name} is dead and cannot be summoned again.")
        return f'Summonned {self.creature}'
