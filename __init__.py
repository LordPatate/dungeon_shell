from factories.factory import GenericFactory
from model.equipment import Equipment, Weapon
from model.npc import NPC

npc_factory = GenericFactory(NPC.RESOURCE_FILE, NPC)
weapon_factory = GenericFactory(Weapon.RESOURCE_FILE, Weapon)
equipment_factory = GenericFactory(Equipment.RESOURCE_FILE, Equipment)

