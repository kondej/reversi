import copy
import random


class AI:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty

    # Wykonaj ruch na podstawie poziomu trudności
    #
    def get_move(self, game):
        valid_moves = game.get_valid_moves(2)

        if not valid_moves:
            return None

        if self.difficulty == 'easy':
            return random.choice(valid_moves)
        elif self.difficulty == 'medium':
            return self.get_best_move_medium(game, valid_moves)
        else:
            return self.get_best_move_hard(game, valid_moves)

    # Średni - preferuj narożniki i krawędzie
    #
    def get_best_move_medium(self, game, valid_moves):
        # Rogi
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        corner_moves = [move for move in valid_moves if move in corners]
        if corner_moves:
            return random.choice(corner_moves)

        # Krawędzie
        edges = [(0, i) for i in range(8)] + [(7, i) for i in range(8)] + \
                [(i, 0) for i in range(8)] + [(i, 7) for i in range(8)]
        edge_moves = [move for move in valid_moves if move in edges]
        if edge_moves:
            return random.choice(edge_moves)

        # W przeciwnym wypadku wykonaj najkorzystniejszy ruch
        best_move = None
        best_score = -1

        for move in valid_moves:
            test_game = copy.deepcopy(game)
            test_game.make_move(move[0], move[1], 2)
            score = sum(row.count(2) for row in test_game.board)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move or random.choice(valid_moves)

    # Trudny - algorytm minimax
    #
    def get_best_move_hard(self, game, valid_moves):
        best_move = None
        best_score = float('-inf')

        for move in valid_moves:
            test_game = copy.deepcopy(game)
            test_game.make_move(move[0], move[1], 2)
            score = self.minimax(test_game, 3, False, float('-inf'), float('inf'))

            if score > best_score:
                best_score = score
                best_move = move

        return best_move or random.choice(valid_moves)

    # Minimax alpha-beta pruning
    #
    def minimax(self, game, depth, is_maximizing, alpha, beta):
        if depth == 0 or game.check_game_over():
            return self.evaluate_board(game)

        if is_maximizing: # Ruch AI
            max_eval = float('-inf')
            valid_moves = game.get_valid_moves(2)

            if not valid_moves:
                game.current_player = 1
                return self.minimax(game, depth - 1, False, alpha, beta)

            for move in valid_moves:
                test_game = copy.deepcopy(game)
                test_game.make_move(move[0], move[1], 2)
                test_game.current_player = 1

                eval_score = self.minimax(test_game, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                if beta <= alpha:
                    break

            return max_eval
        else: # Ruch gracza
            min_eval = float('inf')
            valid_moves = game.get_valid_moves(1)

            if not valid_moves:
                game.current_player = 2
                return self.minimax(game, depth - 1, True, alpha, beta)

            for move in valid_moves:
                test_game = copy.deepcopy(game)
                test_game.make_move(move[0], move[1], 1)
                test_game.current_player = 2

                eval_score = self.minimax(test_game, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                if beta <= alpha:
                    break

            return min_eval

    def evaluate_board(self, game):
        ai_score = sum(row.count(2) for row in game.board)
        human_score = sum(row.count(1) for row in game.board)

        # Wagi pozycji
        weights = [
            [100, -20, 10, 5, 5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10, 5, 5, 10, -20, 100]
        ]

        position_score = 0
        for i in range(8):
            for j in range(8):
                if game.board[i][j] == 2:  # AI
                    position_score += weights[i][j]
                elif game.board[i][j] == 1:  # Gracz
                    position_score -= weights[i][j]

        # Liczba poprawnych ruchów
        ai_mobility = len(game.get_valid_moves(2))
        human_mobility = len(game.get_valid_moves(1))

        return (ai_score - human_score) + position_score * 0.1 + (ai_mobility - human_mobility) * 2