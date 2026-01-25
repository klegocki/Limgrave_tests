import pytest

from characters.player import Player
from equipment.potion import Potion


@pytest.fixture
def potion():
    return Potion("Heal flask", 1, 30)


def test_use_potion(mocker, potion, capsys):
    mock_player = mocker.Mock(spec=Player)

    potion.use_potion(mock_player)
    captured = capsys.readouterr()

    assert captured.out.strip() == "> Drank Heal flask. Healed 30 HP."
    mock_player.heal.assert_called_once_with(30)


def test_to_dict(potion):
    result = potion.to_dict()

    assert isinstance(result, dict)
    assert {"type": "Potion", "name": "Heal flask", "rarity": 1, "heal_amount": 30} == result