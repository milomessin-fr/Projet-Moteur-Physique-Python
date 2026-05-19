import sdl2
import sdl2.ext
import ctypes

#import de fichiers
from .entity import Entity
from .config import config_collision as configC
from .config import config_window as configW

import sdl2
import sdl2.sdlttf as sdlttf

class InterfaceCompteur:
    def __init__(self, renderer, chemin_police=b"arial.ttf", taille_police=24):
        if hasattr(renderer, 'sdlrenderer'):
            self.renderer = renderer.sdlrenderer
        else:
            self.renderer = renderer
            
        self.police = None
        
        if sdlttf.TTF_Init() == -1:
            return

        self.police = sdlttf.TTF_OpenFont(chemin_police, taille_police)

    def dessiner(self, quantite, x=10, y=10, couleur_rgb=(255, 255, 255)):
        if not self.police:
            return

        texte_str = f"Grains: {quantite}".encode('utf-8')
        r, g, b = couleur_rgb
        couleur_sdl = sdl2.SDL_Color(r, g, b, 255)

        surface_texte = sdlttf.TTF_RenderText_Blended(self.police, texte_str, couleur_sdl)
        if not surface_texte:
            return

        texture_texte = sdl2.SDL_CreateTextureFromSurface(self.renderer, surface_texte)
        if not texture_texte:
            sdl2.SDL_FreeSurface(surface_texte)
            return

        largeur = surface_texte.contents.w
        hauteur = surface_texte.contents.h

        rect_destination = sdl2.SDL_Rect(x, y, largeur, hauteur)
        sdl2.SDL_RenderCopy(self.renderer, texture_texte, None, rect_destination)

        sdl2.SDL_FreeSurface(surface_texte)
        sdl2.SDL_DestroyTexture(texture_texte)

    def detruire(self):
        if self.police:
            sdlttf.TTF_CloseFont(self.police)
        sdlttf.TTF_Quit()


class BorderFactory:
    def __init__(self, factory):
        self.factory = factory

    def create(self, win_w, win_h, margin, thickness, color=(255, 255, 0, 255), static=True):
        """
        Crée 4 murs statiques à une distance 'margin' des bords de la fenêtre.
        """

       
        inner_w = win_w - (2 * margin)
        inner_h = win_h - (2 * margin)

        surf_h = sdl2.SDL_CreateRGBSurface(0, inner_w, thickness, 32, 0, 0, 0, 0)
        surf_v = sdl2.SDL_CreateRGBSurface(0, thickness, inner_h, 32, 0, 0, 0, 0)
        
        sdl_color = sdl2.ext.Color(*color)
        sdl2.ext.fill(surf_h, sdl_color)
        sdl2.ext.fill(surf_v, sdl_color)

        s_top = self.factory.from_surface(surf_h)
        s_bottom = self.factory.from_surface(surf_h)
        s_left = self.factory.from_surface(surf_v)
        s_right = self.factory.from_surface(surf_v)

        x_start = margin
        y_start = margin

        return [
            # HAUT 
            Entity(x_start, y_start, s_top, static),
            
            # BAS 
            Entity(x_start, y_start + inner_h - thickness, s_bottom, static),
            
            # GAUCHE 
            Entity(x_start, y_start, s_left,static),
            
            # DROITE 
            Entity(x_start + inner_w - thickness, y_start, s_right, static)

        ]





COLORS = {
    0: (0,  0,  0,  0),   
    2: (194, 178, 128, 255),  
    1: (30,  100, 200, 255),   
    3: (100, 80,  60,  255),  
    5: (50, 50, 50, 50), 
    9: (120,120,120,120),
}

class Render:
    def __init__(self, renderer):
        if hasattr(renderer, 'sdlrenderer'):
            self.renderer = renderer.sdlrenderer
        else:
            self.renderer = renderer
        self.chunk_px   = configC.CHUNK_SIZE * configC.CELL_SIZE
        self.cell_size  = configC.CELL_SIZE
        self.chunk_size = configC.CHUNK_SIZE
        self._cache: dict = {}

    def _build_texture(self, chunk_data: dict):
        ps = self.chunk_px
        cs = self.cell_size
        buf = (ctypes.c_uint8 * (ps * ps * 4))()
        for (ci, cj), grain_type in chunk_data.items():
            r, g, b, a = COLORS.get(grain_type, (255, 0, 255, 255))
            if grain_type != 0:
                for dy in range(cs):
                    for dx in range(cs):
                        px  = ci * cs + dx
                        py  = cj * cs + dy
                        idx = (py * ps + px) * 4
                        buf[idx]     = r
                        buf[idx + 1] = g
                        buf[idx + 2] = b
                        buf[idx + 3] = a
        tex = sdl2.SDL_CreateTexture(
            self.renderer,
            sdl2.SDL_PIXELFORMAT_RGBA8888,
            sdl2.SDL_TEXTUREACCESS_STREAMING,
            ps, ps,
        )
        sdl2.SDL_UpdateTexture(tex, None, buf, ctypes.c_int(ps * 4))
        return tex

    def construire(self):
        for cx, cy in list(configC.MAP_DIRTY):
            if (cx, cy) in self._cache:
                sdl2.SDL_DestroyTexture(self._cache[(cx, cy)])
            self._cache[(cx, cy)] = self._build_texture(configC.MAP[(cx, cy)])
        configC.MAP_DIRTY.clear()

        for (cx, cy), tex in self._cache.items():
            ps  = self.chunk_px
            dst = sdl2.SDL_Rect(cx * ps, cy * ps, ps, ps)
            sdl2.SDL_RenderCopy(self.renderer, tex, None, dst)

    def destroy(self):
        for tex in self._cache.values():
            sdl2.SDL_DestroyTexture(tex)
        self._cache.clear()