from typing import Tuple

import pytest

from factories import equipment_factory, potion_factory, weapon_factory
from model import Player, Qualifier


@pytest.mark.parametrize(
    "name, left_weapon_name, right_weapon_name, equipment_name, stats_order",
    [
        ("Joe", "dagger", "dagger", "traveller cloak", ("mental", "precision", "movement", "strength")),
        ("Jack", "bow", "wooden shield", "leather jerkin", ("precision", "mental", "strength", "movement")),
        ("William", "sword", "wooden shield", "leather jerkin", ("movement", "strength", "mental", "precision")),
        ("Averell", "wooden shield", "wand", "light clothes", ("strength", "movement", "precision", "mental")),
    ]
)
def test_player_creation_scenario(
        name: str,
        left_weapon_name: str,
        right_weapon_name: str,
        equipment_name: str,
        stats_order: Tuple[str, str, str, str],
):
    weapon_category_name = "starting weapons"
    equipment_category_name = "basic equipment"
    expected_elements = {
        name, left_weapon_name, right_weapon_name, equipment_name, Qualifier.STRONG, "Healing potion"
    }

    player = Player(name, *stats_order)
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
    assert player.get_stat(stats_order[0]).max == 17 if stats_order[0] == "strength" else 15
    assert player.get_stat(stats_order[3]).max == 8 if stats_order[3] == "strength" else 6
