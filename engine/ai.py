import random


class AI:
    def __init__(self):
        pass

    # Wykonaj ruch
    #
    def get_move(self, game):
        valid_moves = game.get_valid_moves(2)

        if not valid_moves:
            return None

        return random.choice(valid_moves)