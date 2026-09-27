import random

from src.constants import PLAYER_X, PLAYER_O


def check_winner_for_board(board):
    """
    Check the supplied board for a winner or draw.

    Returns:
        (winner, winning_cells)
    """

    combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    for combination in combinations:
        a, b, c = combination

        if (
            board[a] != ""
            and board[a] == board[b]
            and board[b] == board[c]
        ):
            return board[a], combination

    if "" not in board:
        return "DRAW", []

    return None, []


def minimax(board, depth, is_maximizing):
    """
    Minimax algorithm used by HARD difficulty.
    """

    result, _ = check_winner_for_board(board)

    if result == PLAYER_O:
        return 10 - depth

    if result == PLAYER_X:
        return depth - 10

    if result == "DRAW":
        return 0

    empty_cells = [
        index
        for index, value in enumerate(board)
        if value == ""
    ]

    if is_maximizing:
        best_score = -float("inf")

        for move in empty_cells:
            board[move] = PLAYER_O

            score = minimax(
                board,
                depth + 1,
                False
            )

            board[move] = ""

            best_score = max(
                best_score,
                score
            )

        return best_score

    best_score = float("inf")

    for move in empty_cells:
        board[move] = PLAYER_X

        score = minimax(
            board,
            depth + 1,
            True
        )

        board[move] = ""

        best_score = min(
            best_score,
            score
        )

    return best_score


def get_ai_move(board, difficulty):
    """
    Select a computer move based on difficulty.

    EASY:
        Random move.

    MEDIUM:
        Try to win, then block the player,
        otherwise choose randomly.

    HARD:
        Use minimax to select the best move.
    """

    empty_cells = [
        index
        for index, value in enumerate(board)
        if value == ""
    ]

    if not empty_cells:
        return None

    # EASY
    if difficulty == "EASY":
        return random.choice(empty_cells)

    # MEDIUM
    if difficulty == "MEDIUM":

        # 1. Try to win
        for move in empty_cells:
            board[move] = PLAYER_O

            result, _ = check_winner_for_board(board)

            board[move] = ""

            if result == PLAYER_O:
                return move

        # 2. Try to block player
        for move in empty_cells:
            board[move] = PLAYER_X

            result, _ = check_winner_for_board(board)

            board[move] = ""

            if result == PLAYER_X:
                return move

        # 3. Otherwise random
        return random.choice(empty_cells)

    # HARD
    best_score = -float("inf")
    best_moves = []

    for move in empty_cells:
        board[move] = PLAYER_O

        score = minimax(
            board,
            0,
            False
        )

        board[move] = ""

        if score > best_score:
            best_score = score
            best_moves = [move]

        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves)