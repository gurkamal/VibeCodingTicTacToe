from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room
import eventlet

eventlet.monkey_patch()  # Ensures compatibility with eventlet WebSockets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Game state
games = {}  # Stores active games { room_id: { 'board': [...], 'turn': 'X' } }


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    print("A user connected")


@socketio.on('disconnect')
def handle_disconnect():
    print("A user disconnected")


@socketio.on('join')
def handle_join(data):
    """ Handles player joining a game room """
    room = data['room']
    join_room(room)
    
    if room not in games:
        games[room] = {'board': [''] * 9, 'turn': 'X'}
    
    emit('update_board', games[room], room=room)


@socketio.on('play')
def handle_play(data):
    """ Handles a player's move """
    room = data['room']
    index = data['index']
    player = data['player']

    if room not in games:
        return

    game = games[room]

    # Enforce turn-based play
    if game['turn'] != player or game['board'][index] != '':
        return

    # Make move
    game['board'][index] = player
    game['turn'] = 'O' if player == 'X' else 'X'

    # Check for win or draw
    result = check_winner(game['board'])
    if result:
        emit('game_over', {'winner': result}, room=room)
        games.pop(room)  # Reset game on win
    else:
        emit('update_board', game, room=room)


def check_winner(board):
    """ Checks if there's a winner """
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)  # Diagonals
    ]

    for a, b, c in winning_combinations:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]  # Winner ('X' or 'O')

    if "" not in board:
        return "draw"

    return None


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)  # Explicitly use eventlet
