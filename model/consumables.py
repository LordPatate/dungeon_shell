from model.creature import Creature
from model.npc import NPC
from model.player import Player, PlayerStat


class Consumable:
    RESOURCE_FILE = '../resources/consumables.json'

    def __init__(self, name: str, effect: str):
        self.depleted = False
        self.name = name
        self.effect = effect

    def __str__(self) -> str:
        return f'{self.name}: {self.effect}'

    def use(self) -> str:
        if self.depleted:
            raise Exception('This item is depleted and cannot be used.')

        self.depletes()
        return f'Used {self}'

    def depletes(self):
        self.depleted = True


class Potion(Consumable):
    HEAL_AMOUNT = 6

    def __init__(self, kind: str, effect: str = None):
        self.kind = kind
        if self.is_basic():
            if effect is not None:
                raise ValueError('Only non-basic potions can have a special effect.')

            effect = f'restores up to {Potion.HEAL_AMOUNT} {self.kind}'
        else:
            if effect is None:
                raise ValueError('You must specify an effect for non-basic potions.')

        name = f'{kind} potion'
        super().__init__(name, effect)

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
            return f'Apply effect "{self.effect}" to {target}'  # type: ignore[return-value]

    def is_basic(self):
        return self.kind in PlayerStat.__members__.keys()


class SummonningStone(Consumable):
    DEPLETION_CRETERIA = "The creature can be called back and summunned again as long as it's not killed."

    def __init__(self, creature: NPC):
        self.creature = creature
        self.creature.add_on_death_listener(self.depletes)

        name = 'Summonning stone'
        effect = f'summons {creature}. {SummonningStone.DEPLETION_CRETERIA}'
        super().__init__(name, effect)

    def use(self) -> str:
        if self.depleted:
            raise Exception(f"This stone's {self.creature.name} is dead and cannot be summoned again.")
        return f'Summonned {self.creature}. {SummonningStone.DEPLETION_CRETERIA}'
