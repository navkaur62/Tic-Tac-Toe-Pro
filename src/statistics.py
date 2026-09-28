class Statistics:
    """Track scores and round statistics for the current match."""

    def __init__(self):
        self.player_wins = 0
        self.ai_wins = 0
        self.draws = 0
        self.rounds_played = 0

    def record_result(self, winner):
        """Record the result of a completed round."""

        self.rounds_played += 1

        if winner == "X":
            self.player_wins += 1

        elif winner == "O":
            self.ai_wins += 1

        else:
            self.draws += 1

    def reset(self):
        """Reset all match statistics."""

        self.player_wins = 0
        self.ai_wins = 0
        self.draws = 0
        self.rounds_played = 0

    def get_player_wins(self):
        return self.player_wins

    def get_ai_wins(self):
        return self.ai_wins

    def get_draws(self):
        return self.draws

    def get_rounds_played(self):
        return self.rounds_played