class Core:
    def __init__(self):
        self.board = []
    
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

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]

        for drow, dcol in directions:
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