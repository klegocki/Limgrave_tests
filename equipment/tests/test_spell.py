import pytest

from characters.enemy import Enemy
from characters.player import Player
from equipment.spell import Spell


@pytest.fixture
def spell():
    return Spell("lightning bolt", 20, 25)


def test_cast_success(mocker, spell, capsys):

    mock_caster = mocker.Mock(spec=Player)
    mock_caster.name = "player"
    mock_caster.mp = 20

    mock_enemy = mocker.Mock(spec=Enemy)
    mocker.patch('random.randint', return_value=25)

    result = spell.cast(mock_caster, mock_enemy)
    captured = capsys.readouterr()

    assert result == True
    assert mock_caster.mp == 0
    assert captured.out.strip() == "*** player casts lightning bolt! (Dmg: 25) ***"
    mock_enemy.take_damage.assert_called_once_with(25)


def test_cast_failure(mocker, spell, capsys):

    mock_caster = mocker.Mock(spec=Player)
    mock_caster.name = "player"
    mock_caster.mp = 19

    mock_enemy = mocker.Mock(spec=Enemy)

    result = spell.cast(mock_caster, mock_enemy)
    captured = capsys.readouterr()

    assert result == False
    assert mock_caster.mp < spell.cost
    assert captured.out.strip() == "! Not enough MP for lightning bolt! (Cost: 20, You have: 19)"


def test_to_dict(spell):

    result = spell.to_dict()

    assert isinstance(result, dict)
    assert {"name": "lightning bolt", "cost": 20, "damage": 25} == result