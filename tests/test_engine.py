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
    return AI('medium')

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

# Sprawdź czy prawidłowo wykonano ruch
#
def test_make_valid_move(game):
    # Sprawdź początkową ilość pionków
    initial_black_count = sum(row.count(1) for row in game.board)
    initial_white_count = sum(row.count(2) for row in game.board)

    # Dokonaj ruchu
    assert game.make_move(2, 3, 1)

    # Sprawdź czy pionek został postawiony
    assert game.board[2][3] == 1

    # Sprawdź ilość pionków, po ruchu
    final_black_count = sum(row.count(1) for row in game.board)
    final_white_count = sum(row.count(2) for row in game.board)

    assert final_black_count > initial_black_count
    assert final_white_count < initial_white_count

# Sprawdź nieprawidłowy ruch
#
def test_make_invalid_move(game):
    board_before = [row[:] for row in game.board]  # Deep copy

    # Wykonaj nieprawidłowy ruch
    assert not game.make_move(0, 0, 1)

    # Plansza nie powinna ulec zmianie
    assert game.board == board_before

# Sprawdź czy pionek zostanie zamieniony
#
def test_flip_pieces_in_direction(game):
    # Postaw pionek na (2,3)
    game.make_move(2, 3, 1)

    # Sprawdź czy biały pion na (3,3) został zamieniony na czarny
    assert game.board[3][3] == 1

# Sprawdź restart gry
#
def test_game_reset(game):
    game.make_move(2, 3, 1)
    game.current_player = 2

    game.reset_game()

    assert game.current_player == 1
    assert not game.game_over
    assert game.winner is None
    assert game.board[3][3] == 2
    assert game.board[3][4] == 1
    assert game.board[4][3] == 1
    assert game.board[4][4] == 2

# Sprawdź sytuację kiedy gracz nie ma dozwolonych ruchów
#
def test_no_valid_moves_scenario(game):
    # Wypełnij planszę
    for i in range(8):
        for j in range(8):
            if (i, j) not in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                game.board[i][j] = 2

    game.board[0][0] = 0
    game.board[0][1] = 0
    game.board[1][0] = 0
    game.board[1][1] = 1

    valid_moves = game.get_valid_moves(1)
    assert len(valid_moves) == 0