import pytest

from equipment.inventory import Inventory
from equipment.item import Item
from equipment.weapon import Weapon


@pytest.fixture
def inventory():
    return Inventory()

def test_add_item(inventory, mocker, capsys):

    mock_item = mocker.Mock(spec=Item)
    mock_item.name = "Mana potion"

    inventory.add_item(mock_item)
    captured = capsys.readouterr()

    assert inventory.items[0] == mock_item
    assert captured.out.strip() == "+ Added to inventory: Mana potion"

def test_add_item_copy(inventory, mocker, capsys):
    mock_item = mocker.Mock(spec=Item)
    mock_item.name = "Mana potion"

    inventory.items.append(mock_item)
    inventory.add_item(mock_item)
    captured = capsys.readouterr()

    assert len(inventory.items) == 1
    assert captured.out.strip() == "Item Mana potion is already in your inventory"

def test_remove_existing_item(inventory, mocker):

    mock_item = mocker.Mock(spec=Item)
    mock_item.name = "Mana potion"

    inventory.items.append(mock_item)

    inventory.remove_item(mock_item)

    assert not inventory.items

def test_remove_non_existing_item(inventory, mocker,capsys):

    mock_item_in_inv = mocker.Mock(spec=Item)
    mock_item_in_inv.name = "Mana potion"

    mock_item_not_in_inv = mocker.Mock(spec=Item)
    mock_item_not_in_inv.name = "Health potion"

    inventory.items.append(mock_item_in_inv)
    inventory.remove_item(mock_item_not_in_inv)

    captured = capsys.readouterr()

    assert len(inventory.items) == 1
    assert inventory.items[0] == mock_item_in_inv
    assert captured.out.strip() == "There is no Health potion in your inventory"

def test_get_any_weapon(inventory, mocker):

    mock_weapon = mocker.Mock(spec=Weapon)
    mock_weapon.durability = 1

    inventory.items.append(mock_weapon)

    result = inventory.get_any_weapon()

    assert result == mock_weapon

def test_get_any_weapon_without_weapon(inventory, mocker):

    mock_item = mocker.Mock(spec=Item)
    mock_item.name = "Mana potion"

    inventory.items.append(mock_item)

    result = inventory.get_any_weapon()

    assert result is None

def test_get_any_weapon_no_durability(inventory, mocker):

    mock_weapon = mocker.Mock(spec=Weapon)
    mock_weapon.durability = 0

    inventory.items.append(mock_weapon)

    result = inventory.get_any_weapon()

    assert result is None

def test_show_empty_inventory(inventory, capsys):

    inventory.items = []
    inventory.show()

    captured = capsys.readouterr()


    assert captured.out.strip() == "[Inventory is empty]"


def test_show_inventory_with_items(inventory, capsys):

    inventory.items = ["Sword", "Shield"]
    inventory.show()

    captured = capsys.readouterr()

    assert "--- Inventory ---" in captured.out
    assert "1. Sword" in captured.out
    assert "2. Shield" in captured.out
