




#grains de sables tailles et quantités
CUBE_X = 4
CUBE_Y = 4

GRAINS_QUANTITY = 10000




# Moteur physique configurations
GRAVITE = 800
RIGIDITE = -0.16




#Interface configurations
WORLD_X = 40
WORLD_Y = 40
WORLD_WIDTH = 800
WORLD_HEIGHT = 600


WINDOW_WIDTH = WORLD_X + WORLD_WIDTH + WORLD_X
WINDOW_HEIGHT = WORLD_Y + WORLD_HEIGHT + WORLD_Y


FACTORY = None


TC = CUBE_X #Unité de mesure des grains ça correspond à la taille d'un grain de sable
GRILLE_X_MIN, GRILLE_X_MAX = WORLD_X+TC, WORLD_WIDTH + WORLD_X - TC
GRILLE_Y_MIN, GRILLE_Y_MAX = WORLD_Y, WORLD_HEIGHT


LIMITE_SOL = WORLD_Y + WORLD_HEIGHT - 1
LIMITE_PLAFOND = WORLD_Y + 2




# Delta time (temps entre chaque frame)
FPS = 60
DT = 0.16