# Test fixtures
import pytest

from engine.ai import AI
from engine.core import Core


# Instancja dla Core
#
@pytest.fixture
def game():
    return Core()

# Instancja dla AI
#
@pytest.fixture
def ai():
    return AI('medium')

# Sprawdź czy ustawiono poziom trudności
#
def test_ai_initialization(ai):
    assert ai.difficulty == 'medium'

# Sprawdź czy ruch na łatwym poziomie jest możliwy
#
def test_ai_easy_move(game):
    ai = AI('easy')
    move = ai.get_move(game)

    assert move is not None
    assert move in game.get_valid_moves(2)

# Sprawdź czy ruch na średnim poziomie jest możliwy
#
def test_ai_medium_move(game, ai):
    game.current_player = 2
    move = ai.get_move(game)

    assert move is not None
    assert move in game.get_valid_moves(2)

# Sprawdź czy ruch na trudnym poziomie jest możliwy
#
def test_ai_hard_move(game):
    ai = AI('hard')
    game.current_player = 2
    move = ai.get_move(game)

    assert move is not None
    assert move in game.get_valid_moves(2)


# Sprawdź zachowanie AI kiedy nie ma możliwych ruchów
#
def test_ai_no_valid_moves(game, ai):
    # Brak ruchów dla AI
    for i in range(8):
        for j in range(8):
            game.board[i][j] = 1 # Jeden pion gracza

    move = ai.get_move(game)
    assert move is None

# Sprawdź zachowanie AI na poziomie średnim preferuje narożniki
#
def test_ai_prefers_corners(game, ai):
    # Plansza gdzie możliwy jest ruch do narożnika
    game.board = [[0 for _ in range(8)] for _ in range(8)]
    game.board[0][1] = 1
    game.board[1][0] = 1
    game.board[1][1] = 2

    game.current_player = 2

    valid_moves = game.get_valid_moves(2)
    if (0, 0) in valid_moves:
        # Wykonaj kilka razy dla weryfikacji
        corner_chosen = 0
        for _ in range(10):
            move = ai.get_move(game)
            if move == (0, 0):
                corner_chosen += 1

        # Powinien preferować narożniki
        assert corner_chosen > 5