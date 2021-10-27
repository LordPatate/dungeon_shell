from consumables import Bomb, Consumable, Potion
from equipment import Equipment, Weapon
from factories import Factory
from npc import NPC

npc_factory = Factory(NPC.RESOURCE_FILE, NPC)
weapon_factory = Factory(Weapon.RESOURCE_FILE, Weapon)
equipment_factory = Factory(Equipment.RESOURCE_FILE, Equipment)
potion_factory = Factory(Consumable.RESOURCE_FILE, Potion)
bomb_factory = Factory(Consumable.RESOURCE_FILE, Bomb)
