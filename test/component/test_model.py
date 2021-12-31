from typing import Tuple

import pytest

from factories import equipment_factory, weapon_factory
from model import Player, Qualifier


@pytest.mark.parametrize(
    "name, left_weapon_name, right_weapon_name, equipment_name, stats",
    [
        ("Joe", "sword", "shield", "backpack", (15, 7, 11, 3)),
    ]
)
def test_player_creation_scenario(
        name: str,
        left_weapon_name: str,
        right_weapon_name: str,
        equipment_name: str,
        stats: Tuple[int, int, int, int],
):
    # noinspection PyPep8Naming
    WEAPON_CATEGORY_NAME = "starting weapons"
    # noinspection PyPep8Naming
    EQUIPMENT_CATEGORY_NAME = "basic equipment"

    player = Player(name, stats[0], stats[1], stats[2], stats[3])
    player.qualifier = Qualifier.STRONG
    left_weapon = weapon_factory.from_name(left_weapon_name, WEAPON_CATEGORY_NAME)
    right_weapon = weapon_factory.from_name(right_weapon_name, WEAPON_CATEGORY_NAME)
    equipment = equipment_factory.from_name(equipment_name, EQUIPMENT_CATEGORY_NAME)
    player.equip(left_weapon)
    player.equip(right_weapon)
    player.equip(equipment)
    print(player)
    print(player.details())
