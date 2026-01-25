import pytest

from characters.player import Player
from equipment.inventory import Inventory
from equipment.potion import Potion
from equipment.spell import Spell
from game.game import Game
from equipment.weapon import Weapon


@pytest.fixture
def game():
    return Game()


@pytest.fixture
def mock_player(mocker):
    player = mocker.Mock(spec=Player)
    player.name = "hero"
    player.hp = 50
    player.max_hp = 100
    player.mp = 25
    player.max_mp = 50
    player.experience = 50
    player.inventory = mocker.Mock(spec=Inventory)
    player.inventory.items = []
    player.spells = []
    player.is_alive.return_value = True


    return player


@pytest.fixture
def game_context(mocker):
    mocker.patch('game.game.BattleSystem')
    game = Game()

    player = mocker.Mock()
    player.name = "hero"
    player.hp = 50
    player.max_hp = 100
    player.mp = 20
    player.max_mp = 50
    player.spells = []

    player.inventory = mocker.Mock()
    player.inventory.items = []

    game.player = player

    mocker.patch('time.sleep', return_value=None)

    return game


def test_start_new_game(game, mocker):

    mock_db = mocker.patch('game.game.Database')
    mock_db_instance = mock_db.return_value.__enter__.return_value
    mock_db_instance.fetch_all_save_files.return_value = []

    mocker.patch('builtins.input', side_effect=['1', 'hero', '5'])
    mocker.patch('time.sleep', return_value=None)
    mocker.patch('builtins.print', return_value=None)
    game.start()

    assert game.player is not None
    assert game.player.name == "hero"
    assert game.player.equipped_weapon.name == "Rusted Sword"
    assert game.player.inventory.items[1].name == "Flask of Crimson Tears"
    assert game.player.spells[0].name == "Fireball"


def test_start_new_game_player_exists(game, mocker, capsys):

    mock_db = mocker.patch('game.game.Database')
    mock_db_instance = mock_db.return_value.__enter__.return_value
    mock_db_instance.fetch_all_save_files.return_value = "hero"

    mocker.patch('builtins.input', side_effect=['1', 'hero', "hero_2", '5'])
    mocker.patch('time.sleep', return_value=None)

    game.start()
    captured = capsys.readouterr()

    assert "Player name is already taken." in captured.out.strip()


def test_start_new_game_unknown_command(game, mocker, capsys):

    mock_db = mocker.patch('game.game.Database')
    mock_db_instance = mock_db.return_value.__enter__.return_value
    mock_db_instance.fetch_all_save_files.return_value = "hero"

    mocker.patch('builtins.input', side_effect=['6', '1', 'hero2', '5'])

    game.start()
    captured = capsys.readouterr()

    assert "Unknown command." in captured.out.strip()



def test_start_load_game_success(game, mocker):
    fake_save_data = {
        "name": "LoadedHero",
        "hp": 80, "max_hp": 100, "mp": 20, "max_mp": 50,
        "experience": 50, "strength": 10,
        "equipped_weapon": {"name": "Rusted Sword", "damage": 6, "rarity": 1, "durability": 20},
        "inventory": [
            {"type": "Weapon", "name": "Rusted Sword", "damage": 6, "rarity": 1, "durability": 20},
            {"type": "Potion", "name": "Flask of Crimson Tears", "rarity": 1, "heal_amount": 30}
        ],
        "spells": [{"name": "Fireball", "cost": 15, "damage": 25}]
    }

    mock_db = mocker.patch('game.game.Database')
    mock_db_instance = mock_db.return_value.__enter__.return_value

    mock_db_instance.fetch_all_save_files.return_value = ["LoadedHero"]
    mock_db_instance.fetch_save_file.return_value = fake_save_data

    mocker.patch('builtins.input', side_effect=['2', '1', '5'])
    mocker.patch('time.sleep', return_value=None)
    mocker.patch('builtins.print', return_value=None)

    game.start()

    p = game.player
    assert game.player.name == "LoadedHero"
    assert game.player.hp == 80
    assert game.player.equipped_weapon.name == "Rusted Sword"
    assert len(p.spells) == 1
    assert game.player.spells[0].name == "Fireball"
    assert len(game.player.inventory.items) == 2


def test_start_load_game_failure(game, capsys, mocker):
    mock_db = mocker.patch('game.game.Database')
    mock_db_instance = mock_db.return_value.__enter__.return_value
    mock_db_instance.fetch_all_save_files.return_value = []

    mocker.patch('builtins.input', side_effect=['2', '1', "hero_2", '5'])
    mocker.patch('time.sleep', return_value=None)

    game.start()
    captured = capsys.readouterr()

    assert "You don't have any saved characters." in captured.out.strip()


def test_main_menu_explore(game, mocker):
    mock_explore = mocker.patch.object(game, 'explore')
    mocker.patch('builtins.input', return_value='1')
    mocker.patch('builtins.print', return_value=None)

    game.main_menu()

    mock_explore.assert_called_once()


def test_main_menu_manage_inventory(game, mocker):
    mock_manage_inventory= mocker.patch.object(game, 'manage_inventory')
    mocker.patch('builtins.input', return_value='2')
    mocker.patch('builtins.print', return_value=None)

    game.main_menu()

    mock_manage_inventory.assert_called_once()


def test_main_show_spells(game, mocker, mock_player):
    game.player = mock_player
    mock_show_spells = mocker.patch.object(game.player, 'show_spells')
    mocker.patch('builtins.input', return_value='3')
    mocker.patch('builtins.print', return_value=None)

    game.main_menu()

    mock_show_spells.assert_called_once()


def test_main_menu_show_stats(game, mocker, capsys, mock_player):
    mocker.patch('builtins.input', return_value='4')

    mock_weapon = mocker.Mock(spec=Weapon)
    mock_weapon.name = "Rusted Sword"
    mock_player.equipped_weapon = mock_weapon

    game.player = mock_player

    game.main_menu()
    captured = capsys.readouterr()

    assert "[Name: hero]" in captured.out.strip()
    assert "[HP: 50/100]" in captured.out.strip()
    assert "[MP: 25/50]" in captured.out.strip()
    assert "[XP: 50/100]" in captured.out.strip()
    assert "[Weapon: Rusted Sword]" in captured.out.strip()


def test_main_menu_quit_and_save(game, mocker, capsys):
    mock_db = mocker.patch('game.game.Database')
    mock_db_instance = mock_db.return_value.__enter__.return_value

    mocker.patch('builtins.input', return_value='5')
    game.running = True

    game.main_menu()
    captured = capsys.readouterr()

    assert game.running is False
    assert "Farewell, Tarnished!" in captured.out
    mock_db_instance.save_the_game.assert_called_once_with(game.player)


def test_main_menu_unknown_command(game, mocker, capsys):
    mocker.patch('builtins.input', return_value='6')

    game.main_menu()
    captured = capsys.readouterr()

    assert "Unknown command." in captured.out


def test_explore_standard_enemy(game_context, mocker):
    mocker.patch('random.randint', return_value=5)
    mocker.patch('random.choice', return_value=("Wolf", 20, 3, 10))
    mocker.patch('builtins.print', return_value=None)

    mock_start_battle = mocker.patch.object(game_context.BattleSystem, 'start_battle')

    game_context.explore()

    mock_start_battle.assert_called_once()
    enemy_arg = mock_start_battle.call_args[0][1]
    assert enemy_arg.name == "Wolf"


def test_explore_boss_first_encounter(game_context, mocker):
    game_context.did_boss_appear = False

    mocker.patch('random.randint', return_value=10)
    mocker.patch('random.choice', return_value=("Bell bearing hunter (Boss)", 200, 20, 100))
    mocker.patch('builtins.print', return_value=None)

    mock_start_battle = mocker.patch.object(game_context.BattleSystem, 'start_battle')

    game_context.explore()

    enemy_arg = mock_start_battle.call_args[0][1]

    assert "Boss" in enemy_arg.name
    assert game_context.did_boss_appear is True
    mock_start_battle.assert_called_once()


def test_explore_boss_already_defeated(game_context, mocker):
    game_context.did_boss_appear = True

    mocker.patch('random.randint', return_value=10)
    mocker.patch('random.choice', side_effect=[
        ("Bell bearing hunter (Boss)", 200, 20, 100),
        ("Skeleton", 25, 5, 10)
    ])
    mocker.patch('builtins.print', return_value=None)

    mock_start_battle = mocker.patch.object(game_context.BattleSystem, 'start_battle')

    game_context.explore()

    enemy_arg = mock_start_battle.call_args[0][1]
    assert enemy_arg.name == "Skeleton"


def test_explore_site_of_grace_healing_and_flask(game_context, mocker):
    mocker.patch('random.randint', side_effect=[1, 5])
    mocker.patch('builtins.print', return_value=None)

    game_context.player.hp = 10
    game_context.player.inventory.items = []

    game_context.explore()

    assert game_context.player.hp == game_context.player.max_hp
    assert game_context.player.mp == game_context.player.max_mp

    inventory_items = game_context.player.inventory.add_item.call_args_list
    added_item = inventory_items[0][0][0]

    assert isinstance(added_item, Potion)
    assert added_item.name == "Flask of Crimson Tears"


def test_explore_find_new_spell(game_context, mocker):
    mocker.patch('random.randint', side_effect=[1, 8])
    mocker.patch('builtins.print', return_value=None)

    game_context.player.spells = []

    found_spell = Spell("Black Flame", 22, 38)
    mocker.patch('random.choice', return_value=found_spell)

    game_context.explore()

    assert found_spell in game_context.player.spells


def test_explore_spellbook_full(game_context, mocker):
    mocker.patch('random.randint', side_effect=[1, 8])
    mocker.patch('builtins.print', return_value=None)

    game_context.player.spells = [mocker.Mock(spec=Spell) for _ in range(6)]

    found_spell = Spell("Black Flame", 22, 38)
    mocker.patch('random.choice', return_value=found_spell)

    game_context.explore()

    assert len(game_context.player.spells) == 6


def test_manage_inventory_use_potion(game, mocker, mock_player):
    game.player = mock_player
    mock_potion = mocker.Mock(spec=Potion)
    game.player.inventory.items = [mock_potion]
    mocker.patch('builtins.input', return_value='p')
    mocker.patch('builtins.print', return_value=None)

    game.manage_inventory()

    mock_potion.use_potion.assert_called_once_with(game.player)
    game.player.inventory.remove_item.assert_called_once_with(mock_potion)


def test_manage_inventory_no_potions(game, mocker, capsys, mock_player):
    game.player = mock_player
    mock_weapon = mocker.Mock(spec=Weapon)
    game.player.inventory.items = [mock_weapon]
    mocker.patch('builtins.input', return_value='p')

    game.manage_inventory()
    captured = capsys.readouterr()

    assert "No potions!" in captured.out
    game.player.inventory.remove_item.assert_not_called()


def test_manage_inventory_equip_weapon(game, mocker, mock_player):
    mock_weapon1 = mocker.Mock(spec=Weapon)
    mock_weapon1.name = "Old Sword"
    mock_weapon2 = mocker.Mock(spec=Weapon)
    mock_weapon2.name = "New Sword"
    mocker.patch('builtins.print', return_value=None)

    game.player = mock_player
    game.player.inventory.items = [mock_weapon1, mock_weapon2]
    game.player.equipped_weapon = mock_weapon1

    mocker.patch('builtins.input', side_effect=['e', '2'])

    game.manage_inventory()

    game.player.equip.assert_called_once_with(mock_weapon2)


def test_manage_inventory_equip_fail_already_equipped(game, mocker, capsys, mock_player):
    weapon1 = mocker.Mock(spec=Weapon)

    game.player = mock_player
    game.player.inventory.items = [weapon1]
    game.player.equipped_weapon = weapon1

    mocker.patch('builtins.input', side_effect=['e', '1'])

    game.manage_inventory()
    captured = capsys.readouterr()

    assert "You can't equip that or you already equipped.!" in captured.out
    game.player.equip.assert_not_called()


def test_manage_inventory_quit(game, mocker, mock_player):
    game.player = mock_player
    mocker.patch('builtins.input', return_value='')
    mocker.patch('builtins.print', return_value=None)

    game.manage_inventory()

    game.player.inventory.remove_item.assert_not_called()
    game.player.equip.assert_not_called()