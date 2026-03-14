

# Moteur physique configurations
GRAVITE = 800
RIGIDITE = -0.16

#Interface configurations
WORLD_X = 40
WORLD_Y = 40
WORLD_WIDTH = 520
WORLD_HEIGHT = 620

WINDOW_WIDTH = WORLD_X + WORLD_WIDTH + WORLD_X
WINDOW_HEIGHT = WORLD_Y + WORLD_HEIGHT + WORLD_Y

#grains de sables tailles et quantités
CUBE_X = 4
CUBE_Y = 4

GRAINS_QUANTITY = 15


LIMITE_SOL = WORLD_Y + WORLD_HEIGHT - 1
LIMITE_PLAFOND = WORLD_Y + 2


# Delta time (temps entre chaque frame)
FPS = 60
DT = 0.16