DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
              (0, 1), (1, -1), (1, 0), (1, 1)]

class Core:
    def __init__(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.current_player = 1  # 1 = czarne, 2 = białe
        self.game_over = False
        self.winner = None
        self.reset_game()

    # Reset gry, planszy i ustawienie pionków na pozycjach startowych
    #
    def reset_game(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        # Ustawienie planszy na start
        self.board[3][3] = 2  # Biały
        self.board[3][4] = 1  # Czarny
        self.board[4][3] = 1  # Czarny
        self.board[4][4] = 2  # Biały
        self.current_player = 1
        self.game_over = False
        self.winner = None
    
    # Znajdź wszystkie możliwe ruchy danego gracza
    #
    def get_valid_moves(self, player):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    # Sprawdź czy ruch jest możliwy
    #
    def is_valid_move(self, row, col, player):
        if self.board[row][col] != 0:
            return False



        for drow, dcol in DIRECTIONS:
            if self.would_flip_in_direction(row, col, drow, dcol, player):
                return True
        return False

    # Sprawdź, czy postawienie pionka, obróci pionki w danym kierunku
    #
    def would_flip_in_direction(self, row, col, drow, dcol, player):
        opponent = 3 - player # Wyliczenie kto jest przeciwnikiem
        r = row + drow
        c = col + dcol
        found_opponent = False

        while 0 <= r < 8 and 0 <= c < 8:
            if self.board[r][c] == opponent:
                found_opponent = True
            elif self.board[r][c] == player and found_opponent:
                return True
            else:
                break
            r = r + drow
            c = c + dcol
        return False

    # Obróć pionki w danym kierunku
    #
    def flip_pieces_in_direction(self, row, col, drow, dcol, player):
        opponent = 3 - player
        r = row + drow
        c = col + dcol
        pieces_to_flip = []

        while 0 <= r < 8 and 0 <= c < 8:
            if self.board[r][c] == opponent:
                pieces_to_flip.append((r, c))
            elif self.board[r][c] == player:
                for flip_r, flip_c in pieces_to_flip:
                    self.board[flip_r][flip_c] = player
                break
            else:
                break
            r = r + drow
            c = c + dcol

    # Wykonaj ruch i obróć pionki
    #
    def make_move(self, row, col, player):
        if not self.is_valid_move(row, col, player):
            return False

        self.board[row][col] = player

        for drow, dcol in DIRECTIONS:
            if self.would_flip_in_direction(row, col, drow, dcol, player):
                self.flip_pieces_in_direction(row, col, drow, dcol, player)

        return True

    # Sprawdź czy gra się skończyła
    #
    def check_game_over(self):
        player1_moves = len(self.get_valid_moves(1))
        player2_moves = len(self.get_valid_moves(2))

        if player1_moves == 0 and player2_moves == 0:
            self.game_over = True
            player1_count = sum(row.count(1) for row in self.board)
            player2_count = sum(row.count(2) for row in self.board)

            if player1_count > player2_count:
                self.winner = 1
            elif player2_count > player1_count:
                self.winner = 2
            else:
                self.winner = 0

        return self.game_over

    # Zwróć obecny stan gry
    #
    def get_board_state(self):
        player1_count = sum(row.count(1) for row in self.board)
        player2_count = sum(row.count(2) for row in self.board)

        return {
            'board': self.board,
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner,
            'scores': {'player1': player1_count, 'player2': player2_count},
            'valid_moves': self.get_valid_moves(self.current_player)
        }