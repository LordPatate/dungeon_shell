from factories import Factory
from model.consumables import Consumable
from npc import NPC
from equipment import Weapon, Equipment
from consumables import Potion, Bomb

npc_factory = Factory(NPC.RESOURCE_FILE, NPC)
weapon_factory = Factory(Weapon.RESOURCE_FILE, Weapon)
equipment_factory = Factory(Equipment.RESOURCE_FILE, Equipment)
potion_factory = Factory(Consumable.RESOURCE_FILE, Potion)
bomb_factory = Factory(Consumable.RESOURCE_FILE, Bomb)
