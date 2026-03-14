import sdl2.ext
import config


class Carre:
    def __init__(self,x ,y):
        self.x = x
        self.y = y
        self.v_x = 0
        self.v_y = 0

        sprite_carre = config.FACTORY.from_color(sdl2.ext.Color(255, 0, 0), size=(config.CUBE_X, config.CUBE_Y))
        self.sprite = sprite_carre
        self.sprite.owner = self

        self.sprite.position = self.x, self.y


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
        

    def calcul_gravite_vecteur(self, limite_sol, seuil):
        """calcul du vecteurs pour la gravité si elle est négative ou positive"""

        self.y = limite_sol 
            
        if abs(self.v_y) < abs(seuil):
            self.v_y = 0
            self.y = limite_sol  
        else:
            self.v_y *= config.RIGIDITE
            

            
    def update_movement(self):   
        """Met à jour la position du carré en fonction de sa vitesse et du temps écoulé"""
        self.x += self.v_x * config.DT

        self.v_y += config.GRAVITE * config.DT

        self.y += self.v_y * config.DT
        self.sprite.x = round(self.x)
        self.sprite.y = round(self.y)

