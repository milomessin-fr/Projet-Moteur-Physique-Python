import sdl2
import sdl2.ext
import time
from entity import Carre
from sdl2 import SDL_KEYDOWN, SDLK_SPACE
import config
import random

class MoteurPhysique:
    def __init__(self):
        """"Initialisation du moteur physique et de la fenêtre"""
        sdl2.ext.init()
        self.window = sdl2.ext.Window("Moteur Physique NSI", size=(config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self.window.show()

        self.renderer = sdl2.ext.Renderer(self.window)
        config.FACTORY = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)  
        self.last_time = sdl2.SDL_GetTicks()

        # Initialisation des grains de sable et de leur tableau et de la grille qui définit leur positions pour simplifier leur calcul de collision
        self.tableau_grains = []
        self.colonnes = list(range(config.GRILLE_X_MIN, config.GRILLE_X_MAX, config.TC))
        self.lignes   = list(range(config.GRILLE_Y_MIN, config.GRILLE_Y_MAX, config.TC))

        self.apparition_grains(config.GRAINS_QUANTITY)

       

        # Définition des limites du monde
        self.WORLD_X = config.WORLD_X
        self.WORLD_Y = config.WORLD_Y
        self.WORLD_WIDTH = config.WORLD_WIDTH
        self.WORLD_HEIGHT = config.WORLD_HEIGHT

        # Framerate
        self.FPS = config.FPS
        
        print("Debug => Appuyez sur la barre d'espace pour entrer dans le mode debug")

    def apparition_grains(self,nb_grains):
        """Fait apparaître des grain de sable à une position aléatoire"""
        for el in range(nb_grains):
            self.tableau_grains.append(Carre(x=random.choice(self.colonnes), y=random.choice(self.lignes)))



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
        for el in self.tableau_grains:
            dst_rect = sdl2.SDL_Rect(int(el.x), int(el.y), config.CUBE_X, config.CUBE_Y)
            sdl2.render.SDL_RenderCopy(raw_r, el.sprite.texture, None, dst_rect)

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
                            print("- config.'vars' : GRAVITE, RIGIDITE, GRAINS_QUANTITY.")
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

        
        for el in self.tableau_grains:
            prochaine_y = el.y + (el.v_y * config.DT)
            el.calcul_colision_mur()
            el.calcul_gravite()
            el.update_movement()
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
            config.DT = 1.0 / self.FPS  
            
            self.handle_input()
            self.construire()
            self.colision()
            

        sdl2.ext.quit()
        return 1













if __name__ == "__main__":
    moteur = MoteurPhysique()
    moteur.run_app()