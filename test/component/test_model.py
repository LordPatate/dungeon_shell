from typing import Tuple

import pytest

from factories import equipment_factory, potion_factory, weapon_factory
from model import Player, Qualifier


@pytest.mark.parametrize(
    "name, left_weapon_name, right_weapon_name, equipment_name, stats",
    [
        ("Joe", "dagger", "dagger", "backpack", (3, 7, 11, 15)),
        ("Jack", "sword", "shield", "leather jerkin", (7, 3, 15, 11)),
        ("William", "bow", "light crossbow", "cape", (11, 15, 3, 7)),
        ("Averell", "grimoire", "wand", "backpack", (15, 11, 7, 3)),
    ]
)
def test_player_creation_scenario(
        name: str,
        left_weapon_name: str,
        right_weapon_name: str,
        equipment_name: str,
        stats: Tuple[int, int, int, int],
):
    weapon_category_name = "starting weapons"
    equipment_category_name = "basic equipment"
    expected_elements = {
        name, left_weapon_name, right_weapon_name, equipment_name, Qualifier.STRONG, "Healing potion"
    }

    player = Player(name, stats[0], stats[1], stats[2], stats[3])
    player.qualifier = Qualifier.STRONG
    left_weapon = weapon_factory.from_name(left_weapon_name, weapon_category_name)
    right_weapon = weapon_factory.from_name(right_weapon_name, weapon_category_name)
    equipment = equipment_factory.from_name(equipment_name, equipment_category_name)
    player.equip(left_weapon)
    if left_weapon.two_handed or right_weapon.two_handed:
        with pytest.raises(Exception):
            player.equip(right_weapon)
        expected_elements.remove(right_weapon_name)
    else:
        player.equip(right_weapon)
    player.equip(equipment)
    player.quick_access_consumables.push(potion_factory.healing())

    output = player.details()
    for expected_element in expected_elements:
        assert expected_element in output
