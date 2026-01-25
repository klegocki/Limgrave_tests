import pytest
from equipment.item import Item


@pytest.fixture
def item():
    return Item("Blade", 5)


def test_equipment_str(item):
    assert str(item) == f"Blade (Rarity: 5)"


def test_to_dict(item):
    result = item.to_dict()

    assert isinstance(result, dict)
    assert {"type": "Item", "name": "Blade", "rarity": 5} == result