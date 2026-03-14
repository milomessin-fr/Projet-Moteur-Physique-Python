import sdl2
import sdl2.ext
import time
from entity import Carre
from sdl2 import SDL_KEYDOWN, SDLK_SPACE
import config


class MoteurPhysique:
    def __init__(self):
        """"Initialisation du moteur physique et de la fenêtre"""
        sdl2.ext.init()
        self.window = sdl2.ext.Window("Moteur Physique NSI", size=(config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self.window.show()

        self.renderer = sdl2.ext.Renderer(self.window)
        self.factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)  
        self.last_time = sdl2.SDL_GetTicks()

        # Initialisation du carré
        self.CUBE_X = config.CUBE_X
        self.CUBE_Y = config.CUBE_Y
        sprite_carre = self.factory.from_color(sdl2.ext.Color(255, 0, 0), size=(self.CUBE_X, self.CUBE_Y))
        self.mon_carre = Carre(sprite_carre, x=100, y=100)
        
        # Définition des limites du monde
        self.WORLD_X = config.WORLD_X
        self.WORLD_Y = config.WORLD_Y
        self.WORLD_WIDTH = config.WORLD_WIDTH
        self.WORLD_HEIGHT = config.WORLD_HEIGHT

        # Framerate
        self.FPS = config.FPS
        
        print("Debug => Appuyez sur la barre d'espace pour entrer dans le mode debug")

    
    def construire(self):
        """Construction de la scène"""
        

        raw_r = self.renderer.sdlrenderer

        
        # 1. Fond
        sdl2.render.SDL_SetRenderDrawColor(raw_r, 0, 0, 0, 255)
        sdl2.render.SDL_RenderClear(raw_r)
        
        # 2. Bordure 
        container_rect = sdl2.SDL_Rect(self.WORLD_X, self.WORLD_Y, self.WORLD_WIDTH, self.WORLD_HEIGHT)
        sdl2.render.SDL_SetRenderDrawColor(raw_r, 0, 255, 0, 255) 
        sdl2.render.SDL_RenderDrawRect(raw_r, container_rect)

        # 3. Carré
        dst_rect = sdl2.SDL_Rect(int(self.mon_carre.x), int(self.mon_carre.y), self.CUBE_X, self.CUBE_Y)
        sdl2.render.SDL_RenderCopy(raw_r, self.mon_carre.sprite.texture, None, dst_rect)

        # 4. Affichage
        sdl2.render.SDL_RenderPresent(raw_r)

        return 1




    def handle_input(self):
        """Gestion des entrées utilisateur"""
        events = sdl2.ext.get_events()
        for event in events:
           if event.type == SDL_KEYDOWN:
            # Mode débug : permet d'exécuter du code Python en temps réel
                if event.key.keysym.sym == SDLK_SPACE :
                    while True:
                        input_debug = input("Commande debug >")
                        if input_debug == "help":
                            print("Commandes disponibles :")
                            print("- dir(objet) : Permet d'accéder aux méthodes et attributs d'un objet")
                            print("- vars(objet) : Affiche les valeurs d'un objet")
                            print("- python code : Permet d'exécuter du code Python en temps réel")
                            print("- exit : Quitte le mode debug")
                        if input_debug == "exit":
                            break
                        try:
                            exec(input_debug)
                        except Exception as e:
                            print(f"Erreur : {e}")

    

    
    def colision(self):
        """Gestion des collisions et de la physique"""
        seuil = config.GRAVITE * config.DT 
        prochaine_y = self.mon_carre.y + (self.mon_carre.v_y * config.DT)

        print(f"limite_sol: {config.LIMITE_SOL}, prochaine_y: {prochaine_y}, seuil: {seuil}")

        # Calcul de la gravité et des collisions
        self.mon_carre.calcul_gravite()
        
        self.mon_carre.update_movement()
        return 1
        


    def run_app(self):
        """Lance la boucle principale du moteur """
        running = True

        while running:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    break

            current_time = sdl2.SDL_GetTicks()
            frame_time = current_time - self.last_time

            if frame_time < (1000 // self.FPS):
                sdl2.SDL_Delay((1000 // self.FPS) - frame_time)

            self.last_time = sdl2.SDL_GetTicks()
            config.DT = 1.0 / self.FPS  # dt fixe et stable = 0.016 
            
            print(config.DT)
            self.handle_input()
            self.construire()
            self.colision()
            

        sdl2.ext.quit()
        return 1













if __name__ == "__main__":
    moteur = MoteurPhysique()
    moteur.run_app()