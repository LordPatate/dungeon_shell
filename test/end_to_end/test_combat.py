from factories import equipment_factory, npc_factory, weapon_factory
from model import Player


def test_bear_encounter():
    knight = Player("Lancelot", "strength", "mental", "precision", "speed")
    sword = weapon_factory.from_name("sword", "starting weapons")
    steel_shield = weapon_factory.from_name("steel shield", "military weapons")
    chainmail = equipment_factory.from_name("chainmail", "military equipment")
    knight.equip(sword)
    knight.equip(steel_shield)
    knight.equip(chainmail)
    winnie = npc_factory.from_name("bear", "beasts")

    # Winnie attacks
    knight.hurt(winnie.damage)
    assert knight.is_hurt()

    # Lancelot attacks with extra effort
    knight.strength -= 2
    winnie.hurt(sword.damage + 2)
    assert winnie.is_hurt()

    # Lancelot heals winnie
    winnie.heal(6)
    assert winnie.is_hurt() is False
