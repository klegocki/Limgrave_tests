import pytest

from characters.enemy import Enemy
from characters.player import Player
from equipment.inventory import Inventory
from equipment.spell import Spell
from game.battle_system import BattleSystem


@pytest.fixture
def battle_system():
    return BattleSystem()


@pytest.fixture
def mock_player(mocker):

    mock_player = mocker.Mock(spec=Player)
    mock_player.inventory = Inventory()
    mock_player.name = "hero"
    mock_player.hp = 50
    mock_player.max_hp = 50
    mock_player.mp = 30
    mock_player.max_mp = 30

    return mock_player


@pytest.fixture
def mock_enemy(mocker):
    mock_enemy = mocker.Mock(spec=Enemy)
    mock_enemy.name = "enemy"
    mock_enemy.hp = 50
    mock_enemy.exp_reward = 50

    return mock_enemy


def test_start_battle_victory_by_attack(battle_system, mocker, capsys, mock_player, mock_enemy):
    mock_enemy.hp = 1

    mocker.patch('builtins.input', side_effect=['1'])
    mocker.patch('time.sleep', return_value=None)

    mock_enemy.is_alive.side_effect = [True, False]

    result = battle_system.start_battle(mock_player, mock_enemy)
    captured = capsys.readouterr()

    assert result is True
    assert "*** VICTORY! You defeated enemy! ***" in captured.out.strip()
    mock_player.attack.assert_called_once_with(mock_enemy)
    mock_player.gain_experience.assert_called_with(50)


def test_start_battle_defeat_delete_save_file(battle_system, mocker, capsys, mock_player, mock_enemy):
    mocker.patch('builtins.input', side_effect=['1'])
    mocker.patch('time.sleep', return_value=None)

    mock_player.is_alive.side_effect = [True, False]

    mock_db_class = mocker.patch('game.battle_system.Database')
    mock_db_instance = mock_db_class.return_value.__enter__.return_value

    mocker.patch('builtins.input', side_effect=['1'])
    mocker.patch('time.sleep', return_value=None)

    result = battle_system.start_battle(mock_player, mock_enemy)
    captured = capsys.readouterr()

    assert result is False
    assert "*** YOU DIED ***" in captured.out.strip()
    mock_db_instance.delete_save_file.assert_called_once_with("hero")


def test_start_battle_no_spells(battle_system, mocker, capsys, mock_player, mock_enemy):
    mock_player.spells = []

    mocker.patch('builtins.input', side_effect=['2'])
    mocker.patch('time.sleep', return_value=None)

    mock_enemy.is_alive.side_effect = [True, False]
    battle_system.start_battle(mock_player, mock_enemy)
    captured = capsys.readouterr()

    assert "You don't know any spells!" in captured.out


def test_start_battle_invalid_command(battle_system, mocker, capsys, mock_player, mock_enemy):
    mocker.patch('builtins.input', side_effect=['3'])
    mocker.patch('time.sleep', return_value=None)

    mock_enemy.is_alive.side_effect = [True, False]
    battle_system.start_battle(mock_player, mock_enemy)
    captured = capsys.readouterr()

    assert "Invalid command." in captured.out


def test_start_battle_spell_cast(battle_system, mocker, mock_player, mock_enemy):
    mock_player.spells = []
    spell = mocker.Mock(spec=Spell)
    mock_player.spells.append(spell)

    mocker.patch('builtins.input', side_effect=['2', '1'])
    mocker.patch('builtins.print', return_value=None)
    mocker.patch('time.sleep', return_value=None)

    mock_enemy.is_alive.side_effect = [True, False]
    battle_system.start_battle(mock_player, mock_enemy)

    mock_player.spells[0].cast.assert_called_once_with(mock_player, mock_enemy)


def test_start_battle_wrong_spell_selection(battle_system, mocker, capsys, mock_player, mock_enemy):
    mock_player.spells = []
    spell = mocker.Mock(spec=Spell)
    mock_player.spells.append(spell)

    mocker.patch('builtins.input', side_effect=['2','abc', '2', '0'])
    mocker.patch('time.sleep', return_value=None)

    mock_enemy.is_alive.side_effect = [True, False]
    battle_system.start_battle(mock_player, mock_enemy)
    captured = capsys.readouterr()

    assert "Invalid number! Choose between available spells." in captured.out.strip()
    assert "Selection cancelled." in captured.out.strip()
    assert "Invalid selection." in captured.out.strip()


def test_start_battle_enemy_turn(battle_system, mocker, mock_player, mock_enemy):
    mocker.patch('builtins.input', side_effect=['1'])
    mocker.patch('time.sleep', return_value=None)

    mock_enemy.is_alive.side_effect = [True, True]
    mocker.patch('builtins.print', return_value=None)
    mock_player.is_alive.side_effect = [True, False]
    battle_system.start_battle(mock_player, mock_enemy)

    mock_enemy.perform_action.assert_called_once_with(mock_player)