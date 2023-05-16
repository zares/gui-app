"""-------------------------------------
Playing application sounds using Pygame
-------------------------------------"""

import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from config.gui import SOUNDS_PATH


class AppSound:
    def __init__(self):
        pygame.init()
        self.scaner_sound = self.load_sound("scaner.wav")

    def load_sound(self, sound):
        file_path = SOUNDS_PATH / sound
        if os.path.isfile(file_path):
            return pygame.mixer.Sound(file_path)
        else:
            raise Exception(f"File {file_path} is not found!")
