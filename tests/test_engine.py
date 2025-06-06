import pytest

from engine.ai import AI
from engine.core import Core


# Test fixtures

# Instancja dla Core
#
@pytest.fixture
def game():
    return Core()

# Instancja dla AI
#
@pytest.fixture
def ai():
    return AI()

# Sprawdź dostępne ruchy z pozycji startowej
#
def test_valid_moves_for_initial(game):
    valid_moves = game.get_valid_moves(1)
    expected_moves = [(2, 3), (3, 2), (4, 5), (5, 4)]

    assert len(valid_moves) == 4
    for move in expected_moves:
        assert move in valid_moves

# Sprawdź nieprawidłowe ruchy na zajęte pola
#
def test_valid_move_for_occupied_square(game):
    assert not game.is_valid_move(3, 3, 1)
    assert not game.is_valid_move(4, 4, 1)

# Sprawdź nieprawidłowe ruchy na pola, które nie przejmą żadnych pionów
#
def test_valid_move_for_no_capture(game):
    assert not game.is_valid_move(0, 0, 1)
    assert not game.is_valid_move(7, 7, 1)