import json

import pytest

from factories import (
    npc_factory, weapon_factory, equipment_factory, consumable_factory,
    potion_factory, bomb_factory, scroll_factory, summoning_stone_factory,
)

resource_files = {
    npc_factory: 'bestiary.json',
    weapon_factory: 'armory.json',
    equipment_factory: 'equipment.json',
    consumable_factory: 'consumables.json',
    potion_factory: 'consumables.json',
    bomb_factory: 'consumables.json',
    scroll_factory: 'consumables.json',
    summoning_stone_factory: 'consumables.json',
}
factories = list(resource_files.keys())


@pytest.mark.parametrize('factory', factories[:4])
def test_create(factory):
    file = f'./resources/{resource_files[factory]}'
    with open(file) as f:
        root = json.load(f)
    for category in root:
        for name in root[category]:
            assert factory.from_name(name, category)
