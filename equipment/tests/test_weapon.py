import pytest

from equipment.weapon import Weapon


@pytest.fixture
def weapon():
    return Weapon("Sword", 5, 10, 10)


def test_weapon_str(weapon):
    assert str(weapon) == "Sword [Dmg: 10, Durability: 10]"


def test_decrease_durability(weapon):
    weapon.decrease_durability()

    assert weapon.durability == 9


def test_to_dict(weapon):
    result = weapon.to_dict()

    assert isinstance(result, dict)
    assert {"type": "Weapon", "name": "Sword", "rarity": 5, "damage": 10, "durability": 10} == result
