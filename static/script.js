const socket = io();
let currentTurn = "X"; // Initial turn
const board = document.getElementById("board");

// Initialize board
for (let i = 0; i < 9; i++) {
    const cell = document.createElement("div");
    cell.classList.add("cell");
    cell.dataset.index = i;
    cell.addEventListener("click", () => makeMove(i));
    board.appendChild(cell);
}

// Join room
socket.emit("join", { room });

// Handle board updates
socket.on("update_board", (game) => {
    currentTurn = game.turn;
    document.querySelectorAll(".cell").forEach((cell, i) => {
        cell.textContent = game.board[i];
        cell.classList.toggle("taken", game.board[i] !== '');
    });
});

// Handle game over
socket.on("game_over", (data) => {
    alert(data.winner === "draw" ? "It's a draw!" : `${data.winner} wins!`);
    location.reload();
});

// Send move
function makeMove(index) {
    if (currentTurn !== player) return;  // Prevent playing out of turn
    socket.emit("play", { room, index, player });
}
