import sdl2.ext
import config


class Carre:
    def __init__(self, sprite, x=0.0, y=0.0):
        self.sprite = sprite
        self.sprite.owner = self

        self.sprite.position = x, y

        self.x = x
        self.y = y

        self.v_x = 0
        self.v_y = 0

        self.on_ground = False 


    def retourner_position(self):
        """Retourne la position du carré"""
        return self.x, self.y


    def calcul_gravite(self):
        """calcul de la gravité"""
        limite_sol = config.LIMITE_SOL - config.CUBE_Y
        limite_plafond = config.LIMITE_PLAFOND
        prochaine_y = self.y + (self.v_y * config.DT)
        seuil = config.GRAVITE * config.DT * 2

        if seuil < 0:
            if prochaine_y <= limite_plafond:
                self.calcul_gravite_vecteur(limite_plafond, seuil)
                
        elif seuil > 0:
            if prochaine_y >= limite_sol:
                self.calcul_gravite_vecteur(limite_sol, seuil)
        else:
            self.on_ground = False


    def calcul_gravite_vecteur(self, limite_sol, seuil):
        """calcul de la gravité / vecteurs"""

        self.y = limite_sol 
            
        if abs(self.v_y) < abs(seuil):
            self.v_y = 0
            self.y = limite_sol  
            self.on_ground = True
        else:
            self.v_y *= config.RIGIDITE
            self.on_ground = False  
            

            
    def update_movement(self):   
        """Met à jour la position du carré en fonction de sa vitesse et du temps écoulé"""
        self.x += self.v_x * config.DT

        self.v_y += config.GRAVITE * config.DT

        self.y += self.v_y * config.DT
        print(f"v_y={self.v_y:.2f} | y={self.y:.2f} | on_ground={self.on_ground}")
        self.sprite.x = round(self.x)
        self.sprite.y = round(self.y)

