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
