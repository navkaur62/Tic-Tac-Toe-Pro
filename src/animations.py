import pygame


class MoveAnimation:
    """Animate a Tic-Tac-Toe mark appearing on the board."""

    def __init__(self, duration=250):
        self.duration = duration
        self.active = False
        self.elapsed = 0
        self.position = None
        self.player = None

    def start(self, position, player):
        """Start an animation for a new move."""
        self.position = position
        self.player = player
        self.elapsed = 0
        self.active = True

    def update(self, dt):
        """Update the animation."""
        if not self.active:
            return

        self.elapsed += dt

        if self.elapsed >= self.duration:
            self.elapsed = self.duration
            self.active = False

    def get_progress(self):
        """Return animation progress from 0.0 to 1.0."""
        if self.duration <= 0:
            return 1.0

        progress = self.elapsed / self.duration
        return max(0.0, min(1.0, progress))

    def is_active(self):
        """Return whether the animation is currently running."""
        return self.active

    def reset(self):
        """Reset the animation."""
        self.active = False
        self.elapsed = 0
        self.position = None
        self.player = None


class WinAnimation:
    """Animate the winning line."""

    def __init__(self, duration=500):
        self.duration = duration
        self.active = False
        self.elapsed = 0
        self.start_pos = None
        self.end_pos = None

    def start(self, start_pos, end_pos):
        """Start the winning-line animation."""
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.elapsed = 0
        self.active = True

    def update(self, dt):
        """Update the winning-line animation."""
        if not self.active:
            return

        self.elapsed += dt

        if self.elapsed >= self.duration:
            self.elapsed = self.duration
            self.active = False

    def get_progress(self):
        """Return animation progress from 0.0 to 1.0."""
        if self.duration <= 0:
            return 1.0

        progress = self.elapsed / self.duration
        return max(0.0, min(1.0, progress))

    def is_active(self):
        """Return whether the animation is currently running."""
        return self.active

    def reset(self):
        """Reset the animation."""
        self.active = False
        self.elapsed = 0
        self.start_pos = None
        self.end_pos = None