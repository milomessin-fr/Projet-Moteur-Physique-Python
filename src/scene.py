#import des fichiers
from .widget import BorderFactory
from .widget import InterfaceCompteur
from .widget import Render
from .entity import Entity
from .config import config_window as configW
from .config import config_collision as configC

#import pysdl
import sdl2 
import sdl2.ext 




class SceneBase:
    """scene de base juste une bordure"""
    def __init__(self, renderer, factory):
        configC.ENTITY = []
        self.renderer = renderer
        self.factory = factory
        creator = BorderFactory(self.factory)
        self.spriterenderer = sdl2.ext.TextureSpriteRenderSystem(self.renderer)
        self.table_render = []

        #initalisation des entity et sprites
        MARGIN = 50
        self.borders = creator.create(configW.WINDOW_WIDTH, configW.WINDOW_HEIGHT, MARGIN,thickness=5, color=(255, 255, 255, 255))

        configC.ENTITY.extend(self.borders)
        
        
        


    def construire(self):
        self.renderer.clear(sdl2.ext.Color(0, 0, 0))
        self.table_render = [] 

        for el in configC.ENTITY:
            self.table_render.append(el.sprite)

        self.spriterenderer.render(self.table_render) 





class SceneTEST:
    """scene de TEST"""
    def __init__(self, renderer, factory):
        configC.ENTITY = []
        self.render_grain = Render(renderer)
        self.renderer = renderer
        self.factory = factory
        creator = BorderFactory(self.factory)
        self.spriterenderer = sdl2.ext.TextureSpriteRenderSystem(self.renderer)
        self.table_render = []
        self.ui_compteur = InterfaceCompteur(renderer, chemin_police=b"/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf", taille_police=20)        
        map = Map()
        map.create_map()
        


    def construire(self):
        sdl2.SDL_RenderClear(self.render_grain.renderer)
        self.render_grain.construire()
        self.ui_compteur.dessiner(analyse(), x=50, y=50, couleur_rgb=(255, 255, 255))
        self.renderer.present()


class Map:
    def __init__(self):
        self.size_chunk    = configC.CHUNK_SIZE
        self.height_border = configW.WINDOW_HEIGHT // configC.CELL_SIZE // self.size_chunk
        self.width_border  = configW.WINDOW_WIDTH  // configC.CELL_SIZE // self.size_chunk
        configC.WORLD_WIDTH  = self.width_border
        configC.WORLD_HEIGHT = self.height_border

    def create_chunk(self) -> dict:
        chunk = {}
        for i in range(self.size_chunk):
            for j in range(self.size_chunk):
                chunk[(i, j)] = 0
        return chunk

    def create_map(self) -> dict:
        configC.MAP        = {}   
        configC.MAP_DIRTY  = set()
        configC.MAP_ACTIVE = set()

        for i in range(self.width_border):
            for j in range(self.height_border):
                configC.MAP[(i, j)] = self.create_chunk()



def analyse():
    quantity = 0
    # On parcourt absolument TOUS les chunks de la carte, actifs ou endormis
    for chunk_xy in configC.MAP:
        chunk_data = configC.MAP[chunk_xy]
        for i in chunk_data:
            grain_type = chunk_data[i]
            if grain_type == 1 or grain_type == 5:
                quantity += 1
    return quantity