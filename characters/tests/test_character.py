import pytest

from characters.character import Character


@pytest.fixture
def character():
    return Character("hero", 100, 50, 20)

def test_is_alive(character):
    assert character.is_alive()

def test_is_not_alive(character):
    character.hp = 0
    assert not character.is_alive()

def test_take_damage(character, capsys):
    character.take_damage(50)
    capture = capsys.readouterr()

    assert character.hp == 50
    assert capture.out.strip() == "- hero takes 50 damage! (HP: 50/100)"

def test_take_damage_exact_kill(character, capsys):
    character.take_damage(100)
    capture = capsys.readouterr()

    assert character.hp == 0
    assert capture.out.strip() == "- hero takes 100 damage! (HP: 0/100)"

def test_take_damage_overkill(character, capsys):
    character.take_damage(1000)
    capture = capsys.readouterr()

    assert character.hp == 0
    assert capture.out.strip() == "- hero takes 1000 damage! (HP: 0/100)"

def test_heal(character):
    character.hp = 20
    character.heal(50)

    assert character.hp == 70

def test_over_heal(character):
    character.hp = 50
    character.heal(1000)

    assert character.hp == 100

def test_heal_negative_value(character, capsys):
    character.hp = 50
    character.heal(-50)
    capture = capsys.readouterr()

    assert capture.out.strip() == "Critical error: cannot heal with negative value!"
    assert character.hp == 50

def test_gain_experience(character, capsys):
    character.gain_experience(50)
    capture = capsys.readouterr()

    assert character.experience == 50
    assert capture.out.strip() == "+ Gained 50 XP (Total: 50/100)"


def test_gain_experience_level_up(character, capsys):
    character.gain_experience(120)
    capture = capsys.readouterr()

    assert character.experience == 20
    assert character.max_hp == 110
    assert character.max_mp == 55
    assert character.strength == 22

    assert "+ Gained 120 XP (Total: 120/100)" in capture.out
    assert "*** LEVEL UP! hero is stronger! ***" in capture.out

