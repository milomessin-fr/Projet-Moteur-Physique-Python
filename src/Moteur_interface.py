import sdl2
import sdl2.ext
import time
from entity import Carre
class MoteurPhysique:
    def __init__(self):
        """"Initialisation du moteur physique et de la fenêtre"""
        sdl2.ext.init()
        self.window = sdl2.ext.Window("Moteur Physique NSI", size=(600, 700))
        self.window.show()

        self.renderer = sdl2.ext.Renderer(self.window)
        self.factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)  
        self.last_time = sdl2.SDL_GetTicks()

        # Initialisation du carré
        self.CUBE_X = 50
        self.CUBE_Y = 50     
        sprite_carre = self.factory.from_color(sdl2.ext.Color(255, 0, 0), size=(self.CUBE_X, self.CUBE_Y))
        self.mon_carre = Carre(sprite_carre, x=100, y=100)
                

    def construire(self):
        """Construction de la scène"""
        WORLD_X = 40
        WORLD_Y = 40
        WORLD_WIDTH = 520
        WORLD_HEIGHT = 620

        raw_r = self.renderer.sdlrenderer

        
        # 1. Fond
        sdl2.render.SDL_SetRenderDrawColor(raw_r, 0, 0, 0, 255)
        sdl2.render.SDL_RenderClear(raw_r)
        
        # 2. Bordure 
        container_rect = sdl2.SDL_Rect(WORLD_X, WORLD_Y, WORLD_WIDTH, WORLD_HEIGHT)
        sdl2.render.SDL_SetRenderDrawColor(raw_r, 0, 255, 0, 255) 
        sdl2.render.SDL_RenderDrawRect(raw_r, container_rect)

        # 3. Carré
        dst_rect = sdl2.SDL_Rect(int(self.mon_carre.x), int(self.mon_carre.y), self.CUBE_X, self.CUBE_Y)
        sdl2.render.SDL_RenderCopy(raw_r, self.mon_carre.sprite.texture, None, dst_rect)

        # 4. Affichage
        sdl2.render.SDL_RenderPresent(raw_r)




    def handle_input(self):
        """Gestion des entrées utilisateur"""
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                return False
        return True
    

    
    def colision(self, dt):
        """Gestion des collisions"""
        prochaine_x = self.mon_carre.x + (self.mon_carre.v_x * dt)
        prochaine_y = self.mon_carre.y + (self.mon_carre.v_y * dt)

        if prochaine_x < 40 or prochaine_x + self.CUBE_X > 560:
            self.mon_carre.v_x *= -1

        if prochaine_y < 40 or prochaine_y + self.CUBE_Y > 660:
            self.mon_carre.v_y *= -1

        self.mon_carre.update_movement(dt)
    


    def run_app(self):
        """"Lance la boucle principale du moteur """
        running = True

        while running:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    running = False 

            current_time = sdl2.SDL_GetTicks()
            dt = (current_time - self.last_time) / 1000.0
            self.last_time = current_time
            if dt > 0.1: 
                dt = 0.016

            self.handle_input()
            self.construire()
            self.colision(dt)
            

        sdl2.ext.quit()













if __name__ == "__main__":
    moteur = MoteurPhysique()
    moteur.run_app()