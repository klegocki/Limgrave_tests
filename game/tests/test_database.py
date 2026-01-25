import pytest
import os

from characters.player import Player
from game.database import Database

@pytest.fixture
def player():
    return Player("hero")


@pytest.fixture
def database():
    test_db_name = "test_game.db"
    database = Database(test_db_name)

    with database as db:
        db.create_table()

    yield database

    if os.path.exists(test_db_name):
        os.remove(test_db_name)


def test_create_table(database):
    with database as db:
        db.create_table()
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='players'")
        result = db.cursor.fetchone()

    assert result is not None
    assert result[0] == "players"


def test_save_the_game(database, player):

    with database as db:
        db.save_the_game(player)
        db.cursor.execute("SELECT name FROM players WHERE name='hero'")
        result = db.cursor.fetchone()

    assert result is not None
    assert result[0] == "hero"


def test_delete_save_file(database, player):
    with database as db:
        db.save_the_game(player)
        db.delete_save_file(player.name)
        db.cursor.execute("SELECT name FROM players WHERE name='hero'")

        result = db.cursor.fetchone()

    assert result is None


def test_delete_save_file_no_player(database, player):
    with database as db:
        db.delete_save_file(player.name)
        db.cursor.execute("SELECT name FROM players WHERE name='hero'")
        result = db.cursor.fetchone()

    assert result is None


def test_fetch_save_file_success(database, player):
    with database as db:
        db.save_the_game(player)
        result = db.fetch_save_file(player.name)

    assert result is not None
    assert isinstance(result, dict)
    assert result["hp"] == 100
    assert result["mp"] == 50
    assert result["strength"] == 10
    assert result["max_mp"] == 50
    assert result["max_hp"] == 100
    assert result["name"] == 'hero'
    assert result["experience"] == 0


def test_fetch_save_file_not_found(database):
    with database as d:
        result = d.fetch_save_file("UnknownHero")

    assert result is None


def test_fetch_all_save_files(database, player):
    with database as db:
        db.save_the_game(player)
        player.name = "swordsman"
        db.save_the_game(player)
        result = db.fetch_all_save_files()

    assert len(result) == 2
    assert "hero" in result
    assert "swordsman" in result


def test_fetch_all_save_files_file_not_found(database):
    with database as db:
        result = db.fetch_all_save_files()

    assert result == []