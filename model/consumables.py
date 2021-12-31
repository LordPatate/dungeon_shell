from model.creature import Creature
from model.npc import NPC


class Consumable:
    RESOURCE_FILE = './resources/consumables.json'

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


class HealingPotion(Consumable):
    HEAL_AMOUNT = 6

    def __init__(self):
        name = 'Healing potion'
        effect = f'restores up to {HealingPotion.HEAL_AMOUNT} health'
        super().__init__(name, effect)

    def use(self, target: Creature = None) -> str:
        super().use()
        if target is None:
            raise ValueError("'target' argument required for potions")

        target.heal(HealingPotion.HEAL_AMOUNT)
        return f'Healed {target.name} for {HealingPotion.HEAL_AMOUNT} health.'


class SummoningStone(Consumable):
    DEPLETION_CRITERIA = "The creature can be called back and summoned again as long as it's not killed."

    def __init__(self, creature: NPC):
        self.creature = creature
        self.creature.add_on_death_listener(self.depletes)

        name = 'Summoning stone'
        effect = f'summons {creature}. {SummoningStone.DEPLETION_CRITERIA}'
        super().__init__(name, effect)

    def use(self) -> str:
        if self.depleted:
            raise Exception(f"This stone's {self.creature.name} is dead and cannot be summoned again.")
        return f'Summoned {self.creature}. {SummoningStone.DEPLETION_CRITERIA}'
