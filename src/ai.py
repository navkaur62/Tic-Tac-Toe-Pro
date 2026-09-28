import random

from src.constants import PLAYER_X, PLAYER_O, EMPTY


class AI:
    """Handle computer-player decisions."""

    def __init__(self, difficulty="EASY"):
        self.difficulty = difficulty.upper()

    def set_difficulty(self, difficulty):
        """Change the AI difficulty."""
        self.difficulty = difficulty.upper()

    def get_move(self, board):
        """Return the best move according to the selected difficulty."""

        if self.difficulty == "EASY":
            return self._easy_move(board)

        if self.difficulty == "MEDIUM":
            return self._medium_move(board)

        if self.difficulty == "HARD":
            return self._hard_move(board)

        return self._easy_move(board)

    # ---------------------------------------------------------
    # EASY AI
    # ---------------------------------------------------------

    def _easy_move(self, board):
        """Choose a random empty position."""

        empty_cells = board.get_empty_cells()

        if not empty_cells:
            return None

        return random.choice(empty_cells)

    # ---------------------------------------------------------
    # MEDIUM AI
    # ---------------------------------------------------------

    def _medium_move(self, board):
        """
        Medium AI:
        1. Try to win.
        2. Try to block the player.
        3. Take the center.
        4. Prefer corners.
        5. Otherwise choose any available cell.
        """

        # Try to win.
        winning_move = self._find_winning_move(
            board,
            PLAYER_O
        )

        if winning_move is not None:
            return winning_move

        # Try to block the player.
        blocking_move = self._find_winning_move(
            board,
            PLAYER_X
        )

        if blocking_move is not None:
            return blocking_move

        # Take the center if available.
        if board.is_valid_move(4):
            return 4

        # Prefer corners.
        corners = [0, 2, 6, 8]

        available_corners = [
            position
            for position in corners
            if board.is_valid_move(position)
        ]

        if available_corners:
            return random.choice(available_corners)

        # Otherwise choose any available cell.
        return self._easy_move(board)

    def _find_winning_move(self, board, player):
        """Find a move that allows the given player to win."""

        for position in board.get_empty_cells():

            board.cells[position] = player

            winner, _ = board.check_winner()

            board.cells[position] = EMPTY

            if winner == player:
                return position

        return None

    # ---------------------------------------------------------
    # HARD AI - MINIMAX
    # ---------------------------------------------------------

    def _hard_move(self, board):
        """
        Hard AI using the Minimax algorithm.

        The AI plays as PLAYER_O.
        The human player is PLAYER_X.
        """

        best_score = float("-inf")
        best_move = None

        for position in board.get_empty_cells():

            # Make the AI move.
            board.cells[position] = PLAYER_O

            score = self._minimax(
                board,
                False,
                0
            )

            # Undo the move.
            board.cells[position] = EMPTY

            if score > best_score:
                best_score = score
                best_move = position

        return best_move

    def _minimax(self, board, is_maximizing, depth):
        """
        Minimax algorithm.

        PLAYER_O = AI
        PLAYER_X = Human

        Returns a score based on the final game result.
        """

        winner, _ = board.check_winner()

        # AI wins.
        if winner == PLAYER_O:
            return 10 - depth

        # Human wins.
        if winner == PLAYER_X:
            return depth - 10

        # Draw.
        if not board.get_empty_cells():
            return 0

        # AI's turn - maximize score.
        if is_maximizing:

            best_score = float("-inf")

            for position in board.get_empty_cells():

                board.cells[position] = PLAYER_O

                score = self._minimax(
                    board,
                    False,
                    depth + 1
                )

                board.cells[position] = EMPTY

                best_score = max(
                    best_score,
                    score
                )

            return best_score

        # Human's turn - minimize score.
        else:

            best_score = float("inf")

            for position in board.get_empty_cells():

                board.cells[position] = PLAYER_X

                score = self._minimax(
                    board,
                    True,
                    depth + 1
                )

                board.cells[position] = EMPTY

                best_score = min(
                    best_score,
                    score
                )

            return best_score