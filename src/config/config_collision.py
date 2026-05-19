

MAP = None


CHUNK_SIZE = 32
WORLD_WIDTH = 0
WORLD_HEIGHT = 0
CELL_SIZE = 1

MAP_DIRTY = set()
MAP_ACTIVE = set()

MAX_VELOCITY_GRAINS = 3

RADIUS = 10

MESH_LISTE = []

# Boule de pierre
STONE_BALL_CELLS  = set()        # (chunk_xy, local_x, local_y) de chaque cellule 5
STONE_BALL_CENTER = (0, 0)       # centre en coordonnées monde (wx, wy)
STONE_BALL_VY     = 0            # vitesse de chute
STONE_BALL_ACTIVE = False        # True = la boule tombe