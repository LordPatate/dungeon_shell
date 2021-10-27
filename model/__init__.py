from equipment import Equipment, Weapon
from factories import Factory
from npc import NPC

npc_factory = Factory[NPC](NPC.RESOURCE_FILE, NPC)
weapon_factory = Factory[Weapon](Weapon.RESOURCE_FILE, Weapon)
equipment_factory = Factory[Equipment](Equipment.RESOURCE_FILE, Equipment)
