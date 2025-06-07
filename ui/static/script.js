let gameState = null;
let previousBoard = null;
let isAITurn = false;

async function initGame() {
    try {
        const response = await fetch('/api/game/state');
        gameState = await response.json();
        updateUI();
    } catch (error) {
        console.error('Error:', error);
    }
}

function updateUI() {
    if (!gameState) return;

    updateBoard();
    updateScores()
    updateCurrentTurn();
    updateDifficultyControl()

    if (gameState.game_over) {
        showGameOver();
    } else if (gameState.current_player === 2 && !isAITurn) {
        setTimeout(makeAIMove, 1000);
    }
}

function updateBoard() {
    const board = document.getElementById('board');
    board.innerHTML = '';

    const newBoard = gameState.board;

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.row = row;
            cell.dataset.col = col;

            let moved = false;

            cell.addEventListener('touchstart', (e) => {
                moved = true;
                e.preventDefault();
                makeMove(row, col);
            }, { passive: false });

            cell.addEventListener('click', () => {
                if (moved) {
                    moved = false;
                    return;
                }
                makeMove(row, col);
            });

            const newPiece = newBoard[row][col];
            const oldPiece = previousBoard ? previousBoard[row][col] : null;

            if (newPiece > 0) {
                const pieceDiv = document.createElement('div');
                pieceDiv.className = `piece player${newPiece}`;

                if (!previousBoard || newPiece !== oldPiece) {
                    pieceDiv.classList.add('piece-animated');
                }

                cell.appendChild(pieceDiv);
            }

            if (gameState.current_player === 1 && !gameState.game_over) {
                const isValidMove = gameState.valid_moves.some(
                    move => move[0] === row && move[1] === col
                );
                if (isValidMove) {
                    cell.classList.add('valid-move');
                }
            }

            board.appendChild(cell);
        }
    }
    previousBoard = JSON.parse(JSON.stringify(newBoard));
}

async function makeMove(row, col) {
     if (gameState.game_over || gameState.current_player !== 1 || isAITurn) {
         return;
     }

     try {
         const response = await fetch('/api/game/move', {
             method: 'POST',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify({ row, col })
         });

         if (response.ok) {
             gameState = await response.json();
             updateUI();
         } else {
             const error = await response.json();
             console.error('Error:', error.error);
         }
     } catch (error) {
         console.error('Error:', error);
     }
}

async function makeAIMove() {
    if (gameState.game_over || isAITurn) return;

    isAITurn = true;

    try {
        const response = await fetch('/api/game/ai-move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
            gameState = await response.json();
            isAITurn = false;
            updateUI();
        } else {
            console.error('Ruch AI nie powiódł się!');
            isAITurn = false;
        }
    } catch (error) {
        console.error('Error:', error);
        isAITurn = false;
    }
}

async function setDifficulty() {
    const difficulty = document.getElementById('difficulty').value;

    try {
        const response = await fetch('/api/game/difficulty', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ difficulty })
        });

        if (response.ok) {
            console.log(`Poziom trudności: ${difficulty}`);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function updateDifficultyControl() {
    const player1Score = gameState.scores.player1;
    const player2Score = gameState.scores.player2;
    const difficultySelect = document.getElementById('difficulty');

    if (player1Score !== 2 || player2Score !== 2) {
        difficultySelect.disabled = true;
    } else {
        difficultySelect.disabled = false;
    }
}

function updateScores() {
    document.getElementById('player1-score').textContent = gameState.scores.player1;
    document.getElementById('player2-score').textContent = gameState.scores.player2;
}

function updateCurrentTurn() {
    const turnElement = document.getElementById('current-turn');

    if (gameState.game_over) {
        turnElement.textContent = 'Koniec Gry!';
        return;
    }

    if (gameState.current_player === 1) {
        turnElement.textContent = 'Twój Ruch (Czarne)';
    } else {
        turnElement.textContent = 'Ruch AI (Białe)';
    }
}

function showGameOver() {
    const gameOverDiv = document.getElementById('game-over-message');
    const winnerText = document.getElementById('winner-text');

    let message = '';
    if (gameState.winner === 0) {
        message = "Remis! 🤝";
    } else if (gameState.winner === 1) {
        message = "Wygrałeś! 🎉";
    } else {
        message = "Wygrało AI! 🤖";
    }

    winnerText.textContent = message;
    gameOverDiv.style.display = 'block';
}

async function resetGame() {
    try {
        const response = await fetch('/api/game/reset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
            gameState = await response.json();
            isAITurn = false;

            updateUI();
            document.getElementById('game-over-message').style.display = 'none';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function changeTheme() {
    const theme = document.getElementById('theme').value;
    document.body.className = theme;

    const playerPieces = document.querySelectorAll('.player-piece');
    setTimeout(() => {
        playerPieces[0].style.background = 'radial-gradient(circle at 30% 30%, var(--player1-color-gradient), var(--player1-color))';
        playerPieces[1].style.background = 'radial-gradient(circle at 30% 30%, var(--player2-color-gradient), var(--player2-color))';
    }, 100);
}

initGame();