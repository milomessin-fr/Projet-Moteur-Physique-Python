




#grains de sables tailles et quantités
CUBE_X = 2            #Taille des grains
CUBE_Y = CUBE_X

GRAINS_QUANTITY = 1000 # explicite




# Moteur physique configurations
GRAVITE = -50
RIGIDITE = -0.8 #c le coef qui redistribue la vitesse après une collision




#Interface configurations
WORLD_X = 40
WORLD_Y = 40
WORLD_WIDTH = 800 #correspond à la largeur du monde physique
WORLD_HEIGHT = 600 #correspond à la hauteur du monde physique   // pour changez la taille de l'écran changer ces 2 valeurs HEIGHT et WIDTH, tout va s'adapter nrml


WINDOW_WIDTH = WORLD_X + WORLD_WIDTH + WORLD_X
WINDOW_HEIGHT = WORLD_Y + WORLD_HEIGHT + WORLD_Y


FACTORY = None #Factory pour créer les sprites, les carrés .


TC = CUBE_X #Unité de mesure des grains ça correspond à la taille d'un grain de sable
GRILLE_X_MIN, GRILLE_X_MAX = WORLD_X+TC, WORLD_WIDTH + WORLD_X - TC
GRILLE_Y_MIN, GRILLE_Y_MAX = WORLD_Y, WORLD_HEIGHT


LIMITE_SOL = WORLD_Y + WORLD_HEIGHT - 1
LIMITE_PLAFOND = WORLD_Y + 2




# Delta time (temps entre chaque frame)
FPS = 60
DT = 0.16 #1.0 / FPS 