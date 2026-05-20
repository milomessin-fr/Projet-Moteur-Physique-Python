

MAP = None  
MAP_OBJECT = None

CHUNK_SIZE = 32 # mut
WORLD_WIDTH = 0  #pas mut
WORLD_HEIGHT = 0 # pas mut
CELL_SIZE = 4 # mut





RADIUS = 5 # mut

MESH_LISTE = [] # pas mut 
MESH = set()


MAP_DIRTY = set()
MAP_ACTIVE = set() 

COLOR_OBJET = {
    0: (0,  0,  0,  0),   
    1: (30,  100, 200, 255), 
    2: (50, 50, 50, 50), 
    3: (120,120,120,120),
    4: (0,  255,  0,  0),
}


# Fiche de chaque matière : nom , densité, type, masse, static.
INFO_OBJET = {
    0: ["air",   0,  "gaz",    0, False],
    1: ["sand",  2,  "powder", 1, False],
    2: ["stone", 4,  "solid",  2, False],
    3: ["metal", 5,  "solid",  1, False],
    4: ["water", 1,  "liquid", 1, False],
}


GRAVITY = 0.8