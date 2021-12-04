from factories.consumables_factories import (
    BombFactory, ConsumableFactory, PotionFactory, ScrollFactory, SummoningStoneFactory
)
from factories.factory import GenericFactory
from model.consumables import Consumable
from model.equipment import Equipment, Weapon
from model.npc import NPC

npc_factory = GenericFactory(NPC.RESOURCE_FILE, NPC)
weapon_factory = GenericFactory(Weapon.RESOURCE_FILE, Weapon)
equipment_factory = GenericFactory(Equipment.RESOURCE_FILE, Equipment)
consumable_factory = ConsumableFactory(Consumable.RESOURCE_FILE, Consumable)
potion_factory = PotionFactory()
bomb_factory = BombFactory()
scroll_factory = ScrollFactory()
summoning_stone_factory = SummoningStoneFactory(npc_factory)
