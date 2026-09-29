
"""Procedural audio feedback for Tic-Tac-Toe Pro.

All sound effects are generated in memory.
No external audio files are required.
"""

import io
import math
import struct
import wave

import pygame


class SoundManager:
    """Generate and manage lightweight game sound effects."""

    SAMPLE_RATE = 44100

    def __init__(self, enabled=True, volume=0.35):
        self.enabled = bool(enabled)
        self.volume = self._clamp_volume(volume)

        self.sounds = {}

        if not self.enabled:
            return

        self._initialize_audio()

    # ============================================================
    # AUDIO INITIALIZATION
    # ============================================================

    def _initialize_audio(self):
        """Initialize pygame mixer safely."""

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(
                    frequency=self.SAMPLE_RATE,
                    size=-16,
                    channels=1,
                )

            pygame.mixer.set_num_channels(12)

            self._load_sounds()

        except pygame.error:
            # The game must continue even if audio is unavailable.
            self.enabled = False
            self.sounds.clear()

    # ============================================================
    # HELPERS
    # ============================================================

    @staticmethod
    def _clamp_volume(volume):
        """Keep volume between 0.0 and 1.0."""

        return max(
            0.0,
            min(1.0, float(volume)),
        )

    # ============================================================
    # SOUND GENERATION
    # ============================================================

    def _create_tone(
        self,
        frequencies,
        duration_ms,
        volume_multiplier=1.0,
    ):
        """Create a procedural WAV tone."""

        if not isinstance(
            frequencies,
            (list, tuple),
        ):
            frequencies = [frequencies]

        frame_count = int(
            self.SAMPLE_RATE
            * duration_ms
            / 1000
        )

        raw_audio = bytearray()

        fade_frames = max(
            1,
            int(
                self.SAMPLE_RATE
                * 0.012
            ),
        )

        effective_volume = self._clamp_volume(
            self.volume * volume_multiplier
        )

        for index in range(frame_count):

            time_position = (
                index / self.SAMPLE_RATE
            )

            sample = sum(
                math.sin(
                    2.0
                    * math.pi
                    * frequency
                    * time_position
                )
                for frequency in frequencies
            ) / len(frequencies)

            # Smooth fade in/out to prevent clicking.
            envelope = 1.0

            if index < fade_frames:

                envelope = (
                    index
                    / fade_frames
                )

            elif index >= (
                frame_count
                - fade_frames
            ):

                envelope = (
                    frame_count
                    - index
                ) / fade_frames

            value = int(
                32767
                * effective_volume
                * sample
                * envelope
            )

            raw_audio.extend(
                struct.pack(
                    "<h",
                    value,
                )
            )

        buffer = io.BytesIO()

        with wave.open(
            buffer,
            "wb",
        ) as wav_file:

            wav_file.setnchannels(1)

            wav_file.setsampwidth(2)

            wav_file.setframerate(
                self.SAMPLE_RATE
            )

            wav_file.writeframes(
                raw_audio
            )

        buffer.seek(0)

        return pygame.mixer.Sound(
            file=buffer
        )

    # ============================================================
    # LOAD ALL SOUNDS
    # ============================================================

    def _load_sounds(self):
        """Generate every sound effect."""

        self.sounds = {

            # ----------------------------------------------------
            # Gameplay
            # ----------------------------------------------------

            "player_move": self._create_tone(
                520,
                85,
                1.00,
            ),

            "ai_move": self._create_tone(
                360,
                90,
                0.85,
            ),

            # ----------------------------------------------------
            # Results
            # ----------------------------------------------------

            "win": self._create_tone(
                [660, 880],
                260,
                1.05,
            ),

            "draw": self._create_tone(
                [300, 240],
                220,
                0.90,
            ),

            # ----------------------------------------------------
            # UI
            # ----------------------------------------------------

            "click": self._create_tone(
                700,
                45,
                0.65,
            ),

            "difficulty": self._create_tone(
                [500, 760],
                120,
                0.75,
            ),

            # ----------------------------------------------------
            # Restart
            # ----------------------------------------------------

            "restart": self._create_tone(
                [440, 660],
                100,
                0.75,
            ),
        }

    # ============================================================
    # PLAY SOUND
    # ============================================================

    def play(self, name):
        """Play a named sound effect."""

        if not self.enabled:
            return

        if not pygame.mixer.get_init():
            return

        sound = self.sounds.get(name)

        if sound is not None:
            try:
                sound.play()
            except pygame.error:
                pass

    # ============================================================
    # ENABLE / DISABLE
    # ============================================================

    def set_enabled(self, enabled):
        """Enable or disable sound effects."""

        enabled = bool(enabled)

        if enabled == self.enabled:
            return

        if enabled:

            self.enabled = True

            try:

                if not pygame.mixer.get_init():

                    pygame.mixer.init(
                        frequency=self.SAMPLE_RATE,
                        size=-16,
                        channels=1,
                    )

                    pygame.mixer.set_num_channels(
                        12
                    )

                self._load_sounds()

            except pygame.error:

                self.enabled = False
                self.sounds.clear()

        else:

            self.stop_all()

            self.enabled = False

    # ============================================================
    # VOLUME
    # ============================================================

    def set_volume(self, volume):
        """Update the master sound-effect volume."""

        self.volume = self._clamp_volume(
            volume
        )

        if not self.enabled:
            return

        # Sounds are procedurally generated using the volume,
        # so regenerate them when the volume changes.
        try:
            self._load_sounds()
        except pygame.error:
            pass

    def get_volume(self):
        """Return current master volume."""

        return self.volume

    # ============================================================
    # STATUS
    # ============================================================

    def is_enabled(self):
        """Return whether sound effects are enabled."""

        return self.enabled

    # ============================================================
    # STOP
    # ============================================================

    def stop_all(self):
        """Stop all currently playing sounds."""

        if (
            self.enabled
            and pygame.mixer.get_init()
        ):

            pygame.mixer.stop()

    # ============================================================
    # SHUTDOWN
    # ============================================================

    def shutdown(self):
        """Safely release the audio mixer."""

        if pygame.mixer.get_init():

            pygame.mixer.stop()

            pygame.mixer.quit()

        self.sounds.clear()

