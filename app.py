from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)


def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != "":
            return board[combo[0]]

    if all(cell != "" for cell in board):
        return "draw"

    return None


def computer_move(board):
    empty_cells = [i for i in range(9) if board[i] == ""]
    if empty_cells:
        return random.choice(empty_cells)
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    board = data['board']

    winner = check_winner(board)
    if winner:
        return jsonify({'winner': winner, 'board': board})

    comp_move = computer_move(board)
    if comp_move is not None:
        board[comp_move] = 'O'

    winner = check_winner(board)
    return jsonify({'winner': winner, 'board': board})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    try:
        app.run(host="0.0.0.0", port=port, debug=False)
    except SystemExit:
        print("Flask app failed to start. Check environment settings and port availability.")