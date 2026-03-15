import sdl2
import sdl2.sdlttf as ttf
import ctypes
import config


class Texte:
    def __init__(self,renderer, font="assets/DejaVuSans.ttf", color=(255, 255, 0, 255), x=0, y=0):
        self.renderer = renderer.sdlrenderer
        self.x = x
        self.y = y

        self.font = ttf.TTF_OpenFont(b"src/assets/DejaVuSans.ttf", 16)
     
        self.color = sdl2.SDL_Color(*color)
        

    def renderer_text(self,text=""):
        """Rendu du texte à l'écran"""
        surface = ttf.TTF_RenderUTF8_Blended(self.font,text.encode("utf-8"), self.color)
        texture = sdl2.SDL_CreateTextureFromSurface(self.renderer, surface)

        w, h = ctypes.c_int(0), ctypes.c_int(0)
        sdl2.SDL_QueryTexture(texture, None, None, ctypes.byref(w), ctypes.byref(h))

        dst = sdl2.SDL_Rect(self.x, self.y, w.value, h.value)
        sdl2.SDL_RenderCopy(self.renderer, texture, None, dst)

        sdl2.SDL_DestroyTexture(texture)
        sdl2.SDL_FreeSurface(surface)

