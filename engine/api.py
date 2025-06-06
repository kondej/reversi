from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

from engine.ai import AI
from engine.core import Core

game = Core()
ai = AI()

app = Flask(__name__, template_folder='../ui/templates', static_folder='../ui/static')
CORS(app)

def run():
    app.run(debug=True, host='0.0.0.0')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/game/state')
def get_game_state():
    return jsonify(game.get_board_state())

@app.route('/api/game/reset', methods=['POST'])
def reset_game():
    game.reset_game()
    return jsonify(game.get_board_state())

@app.route('/api/game/move', methods=['POST'])
def make_move():
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')

    if game.game_over:
        return jsonify({'error': 'Koniec gry!'}), 400

    if game.current_player != 1:
        return jsonify({'error': 'To nie jest twój ruch!'}), 400

    if not game.make_move(row, col, 1):
        return jsonify({'error': 'Nieprawidłowy ruch!'}), 400

    # Ruch AI
    game.current_player = 2

    # Sprawdź czy koniec gry
    if game.check_game_over():
        return jsonify(game.get_board_state())

    # Sprawdź czy AI może wykonać ruch
    if not game.get_valid_moves(2):
        game.current_player = 1  # Pomiń ruch AI

    return jsonify(game.get_board_state())

@app.route('/api/game/ai-move', methods=['POST'])
def make_ai_move():
    if game.game_over:
        return jsonify({'error': 'Koniec gry!'}), 400

    if game.current_player != 2:
        return jsonify({'error': 'To nie jest ruch AI!'}), 400

    move = ai.get_move(game)
    if move:
        game.make_move(move[0], move[1], 2)

    # Ruch gracza
    game.current_player = 1

    # Sprawdź czy koniec gry
    if game.check_game_over():
        return jsonify(game.get_board_state())

    # Sprawdź czy gracz może wykonać ruch
    if not game.get_valid_moves(1):
        game.current_player = 2  # Pomiń ruch gracza

    return jsonify(game.get_board_state())