from src.board import Board
from src.constants import PLAYER_X, PLAYER_O


class Game:
    """Manage the overall Tic-Tac-Toe game state."""

    def __init__(self):
        self.board = Board()

        self.current_player = PLAYER_X

        self.winner = None
        self.winning_positions = []

        self.is_round_over = False
        self.is_draw = False

    def reset_round(self):
        """Start a new round."""

        self.board.reset()

        self.current_player = PLAYER_X

        self.winner = None
        self.winning_positions = []

        self.is_round_over = False
        self.is_draw = False

    def make_move(self, position):
        """
        Make a move for the current player.

        Returns:
            True if the move was successful.
            False if the move was invalid.
        """

        if self.is_round_over:
            return False

        if not self.board.make_move(
            position,
            self.current_player
        ):
            return False

        self.check_round_status()

        if not self.is_round_over:
            self.switch_player()

        return True

    def switch_player(self):
        """Switch between X and O."""

        if self.current_player == PLAYER_X:
            self.current_player = PLAYER_O
        else:
            self.current_player = PLAYER_X

    def check_round_status(self):
        """Check whether the current round has ended."""

        winner, positions = self.board.check_winner()

        if winner:
            self.winner = winner
            self.winning_positions = positions
            self.is_round_over = True
            return

        if self.board.is_full():
            self.is_draw = True
            self.is_round_over = True

    def get_winner(self):
        """Return the winner of the round."""

        return self.winner

    def get_current_player(self):
        """Return the player whose turn it is."""

        return self.current_player

    def get_board_state(self):
        """Return a copy of the current board state."""

        return self.board.get_state()