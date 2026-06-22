import os

import pygame

from . import paths


class AudioManager:
    def __init__(self, enabled=True, volume=0.65):
        self.enabled = bool(enabled)
        self.volume = float(volume)
        self.available = False
        self.sounds = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.available = True
        except Exception:
            self.available = False
        if self.available:
            self._load()

    def _load(self):
        for name in ["move", "click", "error", "win"]:
            path = paths.resolve_asset("sounds", f"{name}.wav")
            if not os.path.exists(path):
                continue
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.volume)
                self.sounds[name] = sound
            except Exception:
                pass

    def set_enabled(self, enabled):
        self.enabled = bool(enabled)

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, float(volume)))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)

    def play(self, name):
        if not self.enabled or not self.available:
            return
        sound = self.sounds.get(name)
        if sound:
            try:
                sound.play()
            except Exception:
                pass
