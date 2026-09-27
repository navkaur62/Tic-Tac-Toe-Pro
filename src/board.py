from src.constants import (
    BOARD_SIZE,
    PLAYER_X,
    PLAYER_O,
    EMPTY,
)


class Board:
    """Manage the Tic-Tac-Toe board and its rules."""

    def __init__(self):
        self.cells = [
            EMPTY
            for _ in range(BOARD_SIZE * BOARD_SIZE)
        ]

    def reset(self):
        """Reset the board to an empty state."""
        self.cells = [
            EMPTY
            for _ in range(BOARD_SIZE * BOARD_SIZE)
        ]

    def is_valid_move(self, position):
        """Check whether a position is available."""
        if position < 0 or position >= len(self.cells):
            return False

        return self.cells[position] == EMPTY

    def make_move(self, position, player):
        """Place a player's mark on the board."""
        if player not in (PLAYER_X, PLAYER_O):
            return False

        if not self.is_valid_move(position):
            return False

        self.cells[position] = player

        return True

    def get_empty_cells(self):
        """Return all currently empty positions."""
        return [
            index
            for index, cell in enumerate(self.cells)
            if cell == EMPTY
        ]

    def is_full(self):
        """Return True when the board has no empty cells."""
        return EMPTY not in self.cells

    def check_winner(self):
        """
        Check whether X or O has won.

        Returns:
            (winner, winning_positions)

        Example:
            ("X", [0, 1, 2])
            (None, [])
        """

        winning_combinations = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]

        for combination in winning_combinations:
            a, b, c = combination

            if (
                self.cells[a] != EMPTY
                and self.cells[a]
                == self.cells[b]
                == self.cells[c]
            ):
                return self.cells[a], list(combination)

        return None, []

    def is_draw(self):
        """Return True when the board is full without a winner."""
        winner, _ = self.check_winner()

        return (
            winner is None
            and self.is_full()
        )

    def get_cell(self, position):
        """Return the value stored at a board position."""
        if position < 0 or position >= len(self.cells):
            return None

        return self.cells[position]

    def get_state(self):
        """Return a copy of the current board state."""
        return self.cells.copy()