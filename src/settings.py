
"""Persistent settings for Tic-Tac-Toe Pro."""

import json
from pathlib import Path


class Settings:
    """Load, manage and save game settings."""

    DEFAULT_SETTINGS = {
        "sound_enabled": True,
        "volume": 0.35,
    }

    def __init__(self, file_path="data/settings.json"):
        self.file_path = Path(file_path)

        self.sound_enabled = True
        self.volume = 0.35

        self.load()

    # ============================================================
    # LOAD
    # ============================================================

    def load(self):
        """Load settings from the JSON file."""

        try:
            if not self.file_path.exists():

                self._apply_defaults()
                self.save()
                return

            with self.file_path.open(
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

            self.sound_enabled = bool(
                data.get(
                    "sound_enabled",
                    self.DEFAULT_SETTINGS["sound_enabled"],
                )
            )

            self.volume = self._clamp_volume(
                data.get(
                    "volume",
                    self.DEFAULT_SETTINGS["volume"],
                )
            )

        except (
            OSError,
            json.JSONDecodeError,
            TypeError,
            ValueError,
        ):

            self._apply_defaults()
            self.save()

    # ============================================================
    # SAVE
    # ============================================================

    def save(self):
        """Save current settings to JSON."""

        try:

            self.file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            data = {
                "sound_enabled": self.sound_enabled,
                "volume": self.volume,
            }

            with self.file_path.open(
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4,
                )

        except OSError:
            # The game should continue even if settings
            # cannot be saved.
            pass

    # ============================================================
    # SOUND
    # ============================================================

    def toggle_sound(self):
        """Toggle sound effects on/off."""

        self.sound_enabled = not self.sound_enabled

        self.save()

        return self.sound_enabled

    def set_sound_enabled(self, enabled):
        """Set sound effects state."""

        self.sound_enabled = bool(enabled)

        self.save()

    # ============================================================
    # VOLUME
    # ============================================================

    def set_volume(self, volume):
        """Set volume between 0.0 and 1.0."""

        self.volume = self._clamp_volume(
            volume
        )

        self.save()

    def increase_volume(self, amount=0.05):
        """Increase volume."""

        self.set_volume(
            self.volume + amount
        )

    def decrease_volume(self, amount=0.05):
        """Decrease volume."""

        self.set_volume(
            self.volume - amount
        )

    # ============================================================
    # HELPERS
    # ============================================================

    @staticmethod
    def _clamp_volume(volume):
        """Keep volume between 0.0 and 1.0."""

        return max(
            0.0,
            min(
                1.0,
                float(volume),
            ),
        )

    def _apply_defaults(self):
        """Reset settings to defaults."""

        self.sound_enabled = (
            self.DEFAULT_SETTINGS[
                "sound_enabled"
            ]
        )

        self.volume = (
            self.DEFAULT_SETTINGS[
                "volume"
            ]
        )

