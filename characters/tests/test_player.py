from string import capwords

import pytest

from characters.enemy import Enemy
from characters.player import Player
from equipment.potion import Potion
from equipment.spell import Spell
from equipment.weapon import Weapon


@pytest.fixture
def player():
    return Player("hero")


def test_equip(player, mocker, capsys):

    mock_weapon = mocker.Mock(spec=Weapon)
    mock_weapon.name = "sword"

    player.inventory.add_item(mock_weapon)
    player.equip(mock_weapon)

    captured = capsys.readouterr()

    assert "> Equipped: sword" in captured.out
    assert player.equipped_weapon == mock_weapon


def test_equip_wrong_instance(player, mocker):

    mock_potion = mocker.Mock(spec=Potion)

    result = player.equip(mock_potion)

    assert result is None


def test_learn_spell(player, mocker, capsys):

    mock_spell = mocker.Mock(spec=Spell)
    mock_spell.name = "lightning bolt"

    player.learn_spell(mock_spell)
    captured = capsys.readouterr()

    assert "+ Learned spell: lightning bolt" in captured.out
    assert mock_spell in player.spells


def test_learn_taught_spell(player, mocker, capsys):

    mock_spell = mocker.Mock(spec=Spell)
    mock_spell.name = "lightning bolt"

    player.spells.append(mock_spell)
    player.learn_spell(mock_spell)
    captured = capsys.readouterr()

    assert "> Spell already taught: lightning bolt" in captured.out
    assert player.spells.count(mock_spell) == 1


def test_show_spells_empty(player, capsys):

    player.show_spells()
    captured = capsys.readouterr()

    assert "[Spellbook is empty]" in captured.out.strip()


def test_show_spells(player, mocker, capsys):

    mock_spell1 = mocker.Mock(spec=Spell)
    mock_spell2 = mocker.Mock(spec=Spell)

    mock_spell1.name = "lightning bolt"
    mock_spell2.name = "fireball"

    mock_spell1.cost = 20
    mock_spell2.cost = 25

    mock_spell1.damage = 20
    mock_spell2.damage = 25

    player.spells.append(mock_spell1)
    player.spells.append(mock_spell2)
    player.show_spells()
    captured = capsys.readouterr()

    assert "--- Spellbook ---" in captured.out.strip()
    assert "1. lightning bolt (Cost: 20 MP, Dmg: ~20)" in captured.out.strip()
    assert "2. fireball (Cost: 25 MP, Dmg: ~25)" in captured.out.strip()


def test_check_weapon_status(player, mocker, capsys):

    mock_weapon = mocker.Mock(spec=Weapon)
    mock_weapon.durability = 20

    player.equipped_weapon = mock_weapon
    result = player.check_weapon_status()

    assert result is None


def test_check_weapon_status_unequipped(player, mocker, capsys):

    mock_weapon = mocker.Mock(spec=Weapon)
    mock_weapon.durability = 20

    result = player.check_weapon_status()

    assert result is None


def test_check_weapon_status_no_durability(player, mocker, capsys):

    mock_weapon = mocker.Mock(spec=Weapon)
    mock_weapon.name = "bow"
    mock_weapon.durability = 0

    mock_weapon_in_inv = mocker.Mock(spec=Weapon)
    mock_weapon_in_inv.name = "sword"
    mock_weapon_in_inv.durability = 20
    mock_weapon_in_inv.damage = 20

    player.inventory.items.append(mock_weapon)
    player.equipped_weapon = mock_weapon

    player.inventory.items.append(mock_weapon_in_inv)

    player.check_weapon_status()
    captured = capsys.readouterr()

    assert player.equipped_weapon == mock_weapon_in_inv
    assert "> Equipped: sword" in captured.out.strip()


def test_check_weapon_status_no_durability_and_weapon(player, mocker, capsys):

    mock_weapon = mocker.Mock(spec=Weapon)
    mock_weapon.name = "bow"
    mock_weapon.durability = 0

    player.inventory.items.append(mock_weapon)
    player.equipped_weapon = mock_weapon

    player.check_weapon_status()
    captured = capsys.readouterr()

    assert player.equipped_weapon.name == "Rusted Sword"
    assert player.equipped_weapon.durability == 20
    assert player.equipped_weapon.damage == 6
    assert player.equipped_weapon.rarity == 1

    assert "> You have no weapons left! You found a backup Rusted Sword." in captured.out.strip()
    assert "+ Added to inventory: Rusted Sword" in captured.out.strip()
    assert "> Equipped: Rusted Sword" in captured.out.strip()


def test_attack(player, mocker, capsys):

    mocker.patch("random.randint", return_value=5)

    mock_target = mocker.Mock(spec=Enemy)
    mock_target.name = "knight"
    mock_target.hp = 50

    mock_weapon = mocker.Mock(spec=Weapon)
    mock_weapon.durability = 20
    mock_weapon.damage = 20
    mock_weapon.name = "sword"

    player.mp = 45
    player.inventory.items.append(mock_weapon)
    player.equipped_weapon = mock_weapon

    player.attack(mock_target)
    captured = capsys.readouterr()

    assert "> You attack knight for 25 damage!" in captured.out.strip()
    assert player.mp == 50
    mock_target.take_damage.assert_called_once_with(25)


def test_attack_no_durability(player, mocker, capsys):

    mocker.patch("random.randint", return_value=5)

    mock_target = mocker.Mock(spec=Enemy)
    mock_target.name = "knight"
    mock_target.hp = 50

    mock_weapon = mocker.Mock(spec=Weapon)
    mock_weapon.durability = 0
    mock_weapon.damage = 20
    mock_weapon.name = "sword"

    player.mp = 45
    player.inventory.items.append(mock_weapon)
    player.equipped_weapon = mock_weapon

    player.attack(mock_target)
    captured = capsys.readouterr()

    assert "! Your sword is broken and useless!" in captured.out.strip()
    assert "> You attack knight for 5 damage!" in captured.out.strip()
    assert player.mp == 50
    mock_target.take_damage.assert_called_once_with(5)
