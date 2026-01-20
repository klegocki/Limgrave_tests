import pytest

from characters.enemy import Enemy
from characters.player import Player
from equipment.spell import Spell


@pytest.fixture
def spell():
    return Spell("lightning bolt", 20, 25)

def test_cast_success(mocker, spell):

    mock_caster = mocker.Mock(spec=Player)
    mock_caster.name = "player"
    mock_caster.mp = 20

    mock_enemy = mocker.Mock(spec=Enemy)
    mocker.patch('random.randint', return_value=25)

    result = spell.cast(mock_caster, mock_enemy)

    assert result == True
    assert mock_caster.mp == 0
    mock_enemy.take_damage.assert_called_once_with(25)

def test_cast_failure(mocker, spell):

    mock_caster = mocker.Mock(spec=Player)
    mock_caster.name = "player"
    mock_caster.mp = 19

    mock_enemy = mocker.Mock(spec=Enemy)

    result = spell.cast(mock_caster, mock_enemy)

    assert result == False
    assert mock_caster.mp < spell.cost