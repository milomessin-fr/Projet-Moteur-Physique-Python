import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import config_window

class GrilleSpatiale:
    def __init__(self,taille_cell):
        self.taille_cell = taille_cell
        self.x_fenetre = config_window.WINDOW_WIDTH
        self.y_fenetre = config_window.WINDOW_HEIGHT
        self.grille = {}
    def creer_grille(self):
        i = 0
        while i <= self.x_fenetre // self.taille_cell:
            for j in range(self.y_fenetre // self.taille_cell +1):
                self.grille[(i,j)] = None
            i += 1
    
        
grille = GrilleSpatiale(100)
grille.creer_grille()
print(grille.grille)


            


            