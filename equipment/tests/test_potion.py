import pytest

from characters.player import Player
from equipment.potion import Potion


@pytest.fixture
def potion():
    return Potion("Heal flask", 5, 30)

def test_use_potion(mocker, potion):
    mock_player = mocker.Mock(spec=Player)

    potion.use_potion(mock_player)

    mock_player.heal.assert_called_once_with(30)