"""Procedural audio feedback for Tic-Tac-Toe Pro.

The game does not need external .wav/.mp3 assets. Short sounds are generated
in memory when the sound manager starts, keeping the project self-contained.
"""

import io
import math
import struct
import wave

import pygame


class SoundManager:
    """Create and play lightweight UI/game sound effects."""

    SAMPLE_RATE = 44100

    def __init__(self, enabled=True, volume=0.35):
        self.enabled = enabled
        self.volume = max(0.0, min(1.0, volume))
        self.sounds = {}

        if not self.enabled:
            return

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=self.SAMPLE_RATE, size=-16, channels=1)
            pygame.mixer.set_num_channels(12)
            self._load_sounds()
        except pygame.error:
            # The game should still work if the computer has no audio device.
            self.enabled = False

    def _create_tone(self, frequencies, duration_ms, volume=None):
        """Create a short WAV tone in memory and return it as a pygame Sound."""

        if volume is None:
            volume = self.volume

        frame_count = int(self.SAMPLE_RATE * duration_ms / 1000)
        raw = bytearray()

        if not isinstance(frequencies, (list, tuple)):
            frequencies = [frequencies]

        for index in range(frame_count):
            t = index / self.SAMPLE_RATE
            sample = sum(
                math.sin(2.0 * math.pi * frequency * t)
                for frequency in frequencies
            ) / len(frequencies)

            # Small fade-in/out prevents clicks at the edges.
            fade_frames = max(1, int(self.SAMPLE_RATE * 0.012))
            envelope = 1.0
            if index < fade_frames:
                envelope = index / fade_frames
            elif index >= frame_count - fade_frames:
                envelope = (frame_count - index) / fade_frames

            value = int(32767 * volume * sample * envelope)
            raw.extend(struct.pack("<h", value))

        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.SAMPLE_RATE)
            wav_file.writeframes(raw)

        buffer.seek(0)
        return pygame.mixer.Sound(file=buffer)

    def _load_sounds(self):
        self.sounds = {
            "player_move": self._create_tone(520, 85),
            "ai_move": self._create_tone(360, 90, self.volume * 0.85),
            "win": self._create_tone([660, 880], 260, self.volume * 1.05),
            "draw": self._create_tone([300, 240], 220, self.volume * 0.9),
            "click": self._create_tone(700, 45, self.volume * 0.65),
            "restart": self._create_tone([440, 660], 100, self.volume * 0.75),
            "difficulty": self._create_tone([500, 760], 120, self.volume * 0.75),
        }

    def play(self, name):
        """Play a named sound effect if audio is available."""

        if not self.enabled:
            return

        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()

    def set_volume(self, volume):
        """Set the volume of all generated effects."""

        self.volume = max(0.0, min(1.0, volume))

        if not self.enabled:
            return

        for sound in self.sounds.values():
            sound.set_volume(self.volume)

    def stop_all(self):
        """Stop all currently playing effects."""

        if self.enabled and pygame.mixer.get_init():
            pygame.mixer.stop()

    def shutdown(self):
        """Release the audio mixer."""

        if self.enabled and pygame.mixer.get_init():
            pygame.mixer.quit()
