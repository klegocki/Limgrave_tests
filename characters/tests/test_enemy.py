from unittest import expectedFailure

import pytest

from characters.enemy import Enemy
from characters.player import Player


@pytest.fixture
def enemy():
    return Enemy('knight', 20, 10, 10)


def test_perform_action(enemy, mocker, capsys):

    mock_player = mocker.Mock(spec=Player)

    mocker.patch("random.randint", return_value=5)
    enemy.perform_action(mock_player)

    captured = capsys.readouterr()

    assert "! knight attacks you for 5 damage!" in captured.out.strip()
    mock_player.take_damage.assert_called_once_with(5)