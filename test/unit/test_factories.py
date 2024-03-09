import pytest
import yaml

from factories import (
    npc_factory, weapon_factory, equipment_factory, consumable_factory,
    potion_factory, bomb_factory, scroll_factory, summoning_stone_factory,
)

resource_files = {
    npc_factory: 'npcs.yaml',
    weapon_factory: 'weapons.yaml',
    equipment_factory: 'equipment.yaml',
    consumable_factory: 'consumables.yaml',
    potion_factory: 'consumables.yaml',
    bomb_factory: 'consumables.yaml',
    scroll_factory: 'consumables.yaml',
    summoning_stone_factory: 'consumables.yaml',
}
factories = list(resource_files.keys())


@pytest.mark.parametrize('factory', factories[:4])
def test_from_name(factory):
    file = f'./resources/{resource_files[factory]}'
    with open(file, encoding="utf-8") as f:
        root = yaml.safe_load(f)
    for category in root:
        for name in root[category]:
            assert factory.from_name(name, category)


def test_special_potions_from_name():
    for name in potion_factory.get_special_names():
        assert potion_factory.from_name(name)


def test_bombs_from_name():
    for name in bomb_factory.get_bomb_names():
        assert bomb_factory.from_name(name)
