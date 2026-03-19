
 # Bibliothèque pysdl
import sdl2 
from sdl2 import SDL_KEYDOWN, SDLK_SPACE
import sdl2.sdlttf as ttf

 # divers import
import random
import time

# import de fichiers
import src/config_window as config
print(config.FPS)


class MoteurRendu:
    def __init__(self):
        """"Récupération des valeurs"""
        self.WORLD_X = 800
        self.WORLD_Y = 600
        self.FPS = config.FPS

        #setup de la fenetre 
        self.set_window()

    def set_window(self):
        """Initialisation de la fenêtre"""