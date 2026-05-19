
 # Bibliothèque pysdl
from curses import window

import sdl2 
import sdl2.ext 
from sdl2 import SDL_KEYDOWN, SDLK_SPACE
import sdl2.sdlttf as ttf

 # divers import
import random
import time
import threading
import ctypes
# import de fichiers
from ..config import config_window as config
from ..config import config_collision as configC

from .debug import DebugMenu
from ..scene import SceneBase, SceneTEST
from ..core.collision import Collision 






class MoteurRendu:
    def __init__(self):
        """"Récupération des valeurs"""
        self.quantity = 0
        self.WINDOW_WIDTH = config.WINDOW_WIDTH
        self.WINDOW_HEIGHT = config.WINDOW_HEIGHT
        self.FPS = config.FPS
        self.mode_debug = DebugMenu()
        self.collision = Collision() #mettre en parametre une table des entity non static
        #setup de la fenetre 
        self.set_window()


    def set_window(self):
        """Initialisation de la fenêtre"""
        sdl2.ext.init()
        self.window = sdl2.ext.Window("Moteur Physique NSI", size=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.window.show()
        
        self.renderer = config.renderer = sdl2.ext.Renderer(self.window)
        self.factory = config.FACTORY = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer) 
        self.last_time = sdl2.SDL_GetTicks()
        ttf.TTF_Init()

        #initialisation de toutes les scenes
        self.scene_base = None
        self.scene_test = None
        #lancement de la boucle
        self.run()
    


    def fixed_timestep(self):
        """mise à jour à intervalles de temps fixes et constants"""
        self.dt = 1.0 / self.FPS
        accumulator = 0

        current_time = sdl2.SDL_GetTicks() / 1000
        frame_time = current_time - self.last_time
        self.last_time = current_time

        accumulator += frame_time

        while accumulator >= self.dt:
            accumulator -= self.dt
        configC.DT = self.dt





    def event(self):
        """gère les events"""
        events = sdl2.ext.get_events()
        for event in events:
            x_ptr = ctypes.c_int(0)
            y_ptr = ctypes.c_int(0)
            button_state = sdl2.SDL_GetMouseState(ctypes.byref(x_ptr), ctypes.byref(y_ptr))
    
            if button_state & sdl2.SDL_BUTTON(sdl2.SDL_BUTTON_LEFT):
                mouse_pos = (x_ptr.value, y_ptr.value)
                if config.MOUSE_OPTION == 1:
                    spawn_sand_at_mouse(mouse_pos, configC.CELL_SIZE, radius=configC.RADIUS)
                elif config.MOUSE_OPTION == 2:
                    spawn_stone_at_mouse(mouse_pos, configC.CELL_SIZE, radius=configC.RADIUS)
                elif config.MOUSE_OPTION == 0:
                    spawn_clear_at_mouse(mouse_pos, configC.CELL_SIZE, radius=configC.RADIUS)
                elif config.MOUSE_OPTION == 3:
                    spawn_mesh_circle(mouse_pos, configC.CELL_SIZE, radius=configC.RADIUS)
            if event.type == sdl2.SDL_QUIT: #ferme l'application
                self.running = False
            
            if event.type == SDL_KEYDOWN: # lance le mode debug
                if event.key.keysym.sym == SDLK_SPACE :
                    self.mode_debug.menu()
                    
        
    
                        

    def render_scene(self, scene="base"):
        """initialise une scene"""
        if scene == "base":
            if self.scene_base == None :
                self.scene_base = SceneBase(renderer=self.renderer, factory=self.factory)
            self.scene_base.construire()
        if scene == "test":
            if self.scene_test == None:
                self.scene_test = SceneTEST(renderer=self.renderer, factory=self.factory)
            self.scene_test.construire()
        self.renderer.present()
        pass



    def run(self):
        """Boucle de l'application"""

        self.running = True
        self.collision.start()

        while self.running:
            self.event()

            self.fixed_timestep()
            
            with self.collision.verrou:
                self.render_scene(config.SCENE_now)


        self.collision.stop()
        self.mode_debug.stop()
        sdl2.ext.quit()




def spawn_sand_at_mouse(mouse_pos, cell_size, radius=0):
    mouse_x, mouse_y = mouse_pos

    global_mouse_x = mouse_x // cell_size
    global_mouse_y = mouse_y // cell_size

    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx * dx + dy * dy <= radius * radius:
                global_x = global_mouse_x + dx
                global_y = global_mouse_y + dy

                chunk_x = global_x // configC.CHUNK_SIZE
                chunk_y = global_y // configC.CHUNK_SIZE
                chunk_xy = (chunk_x, chunk_y)

                local_x = global_x % configC.CHUNK_SIZE
                local_y = global_y % configC.CHUNK_SIZE

                if chunk_xy in configC.MAP:
                    configC.MAP[chunk_xy][(local_x, local_y)] = 1
                    configC.MAP_DIRTY.add(chunk_xy)
                    configC.MAP_ACTIVE.add(chunk_xy)

    
def spawn_stone_at_mouse(mouse_pos, cell_size, radius=0):
    mouse_x, mouse_y = mouse_pos

    global_mouse_x = mouse_x // cell_size
    global_mouse_y = mouse_y // cell_size

    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx * dx + dy * dy <= radius * radius:
                global_x = global_mouse_x + dx
                global_y = global_mouse_y + dy

                chunk_x = global_x // configC.CHUNK_SIZE
                chunk_y = global_y // configC.CHUNK_SIZE
                chunk_xy = (chunk_x, chunk_y)

                local_x = global_x % configC.CHUNK_SIZE
                local_y = global_y % configC.CHUNK_SIZE

                if chunk_xy in configC.MAP:
                    configC.MAP[chunk_xy][(local_x, local_y)] = 5
                    configC.MAP_DIRTY.add(chunk_xy)
                    configC.MAP_ACTIVE.add(chunk_xy)

    
def spawn_clear_at_mouse(mouse_pos, cell_size, radius=0):
    mouse_x, mouse_y = mouse_pos

    global_mouse_x = mouse_x // cell_size
    global_mouse_y = mouse_y // cell_size

    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx * dx + dy * dy <= radius * radius:
                global_x = global_mouse_x + dx
                global_y = global_mouse_y + dy

                chunk_x = global_x // configC.CHUNK_SIZE
                chunk_y = global_y // configC.CHUNK_SIZE
                chunk_xy = (chunk_x, chunk_y)

                local_x = global_x % configC.CHUNK_SIZE
                local_y = global_y % configC.CHUNK_SIZE

                if chunk_xy in configC.MAP:
                    configC.MAP[chunk_xy][(local_x, local_y)] = 0
                    configC.MAP_DIRTY.add(chunk_xy)
                    configC.MAP_ACTIVE.add(chunk_xy)


def spawn_mesh_circle(mouse_pos, cell_size, radius=0):
    mouse_x,mouse_y = mouse_pos
    boule_x = mouse_x // cell_size
    boule_y = mouse_y // cell_size
    boule_rayon = radius
    configC.MESH_LISTE = [(boule_x, boule_y, boule_rayon)] # une seul pour l'instant
    


             
if __name__ == "__main__":
    moteur_rendu = MoteurRendu()
    