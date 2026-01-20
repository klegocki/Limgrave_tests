import pytest
from equipment.item import Item


@pytest.fixture
def item():
    return Item("Blade", 5)


def test_equipment_str(item):
    assert str(item) == f"Blade (Value: 5)"