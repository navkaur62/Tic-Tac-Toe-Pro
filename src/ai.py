import random

from src.constants import PLAYER_O, EMPTY


class AI:
    """Handle computer-player decisions."""

    def __init__(self, difficulty="EASY"):
        self.difficulty = difficulty.upper()

    def set_difficulty(self, difficulty):
        """Change the AI difficulty."""

        self.difficulty = difficulty.upper()

    def get_move(self, board):
        """
        Return a position for the AI to play.

        For EASY mode, the AI selects a random
        available position.
        """

        if self.difficulty == "EASY":
            return self._easy_move(board)

        return self._easy_move(board)

    def _easy_move(self, board):
        """Choose a random empty position."""

        empty_cells = board.get_empty_cells()

        if not empty_cells:
            return None

        return random.choice(empty_cells)