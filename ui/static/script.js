let gameState = null;
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
}

function updateBoard() {
    const board = document.getElementById('board');
    board.innerHTML = '';

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.row = row;
            cell.dataset.col = col;
            cell.onclick = () => makeMove(row, col);

            const piece = gameState.board[row][col];
            if (piece > 0) {
                const pieceDiv = document.createElement('div');
                pieceDiv.className = `piece player${piece}`;
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

             animateFlippedPieces();

             if (gameState.current_player === 2 && !gameState.game_over) {
                 setTimeout(makeAIMove, 1000);
             }
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

            animateFlippedPieces();
        } else {
            console.error('Ruch AI nie powiódł się!');
            isAITurn = false;
        }
    } catch (error) {
        console.error('Error:', error);
        isAITurn = false;
    }
}

function animateFlippedPieces() {
    const pieces = document.querySelectorAll('.piece');
    pieces.forEach(piece => {
        if (Math.random() < 0.3) {
            piece.classList.add('animate-flip');
            setTimeout(() => {
                piece.classList.remove('animate-flip');
                }, 600);
        }
    });
}

initGame();