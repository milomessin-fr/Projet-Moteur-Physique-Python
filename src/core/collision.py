#import divers
import threading
import sdl2
import time
import random
#import de fichiers
from ..config import config_collision as configC
from ..config import config_window as configW
class Collision:
    def __init__(self): 
        self.running = True
        #self.entity = entity
        self.verrou = threading.Lock()
        self.thread = threading.Thread(target=self.colision)

        

    def colision(self): 
        self.flip_flop = False
        self.physics_dt = 0.005
        self.accumulator = 0.0
        last_ticks = sdl2.SDL_GetTicks()
        
        while self.running:
            current_ticks = sdl2.SDL_GetTicks()
            frame_time = (current_ticks - last_ticks) / 1000.0
            last_ticks = current_ticks
            if frame_time > 0.01: 
                frame_time = 0.01
            self.accumulator += frame_time
            while self.accumulator >= self.physics_dt:
                with self.verrou:
                    if not configC.MAP_OBJECT:
                        return
                    self.tick_physics()
                self.accumulator -= self.physics_dt
            sdl2.SDL_Delay(1)





    def update_chunks(self,chunk_xy):
        self.updated_cells = set()
        chunk = configC.MAP[chunk_xy]
        chunk_x, chunk_y = chunk_xy
        self.info_matiere = configC.INFO_OBJET  # nom , densité, type, masse, static.
        self.had_change = False


        for (x,y), cell_type in list(chunk.items()):
            self.world_x = chunk_x * configC.CHUNK_SIZE + x
            self.world_y = chunk_y * configC.CHUNK_SIZE + y
            cell_below = configC.MAP_OBJECT.get_cell(self.world_x, self.world_y + 1)
            if (self.world_x,self.world_y) in self.updated_cells:
                continue

            if cell_below == -1:
                continue

            
            
            if self.info_matiere[cell_type][2] == "powder":

                if self.info_matiere[cell_type][1] > self.info_matiere[cell_below][1]:
                    self.grains_densite(cell_type,cell_below, 0, 1)
                    continue

                self.move_powder(cell_type) 

            if self.info_matiere[cell_type][2] == "liquid":

                if self.info_matiere[cell_type][1] > self.info_matiere[cell_below][1]:
                    self.grains_densite(cell_type,cell_below, 0, 1)
                    continue

                self.move_liquid(cell_type) 

            if self.info_matiere[cell_type][2] == "solid":
                continue



        return self.had_change
    

    def grains_densite(self,cell_1, cell_2, x,y):
       
        if self.info_matiere[cell_1][1] > self.info_matiere[cell_2][1] :
                self.updated_cells.add((self.world_x,self.world_y))
                self.updated_cells.add((self.world_x+x,self.world_y+y))

                configC.MAP_OBJECT.set_cell(self.world_x , self.world_y , cell_2)
                configC.MAP_OBJECT.set_cell(self.world_x + x, self.world_y + y, cell_1)
                self.had_change = True
                return True
        return False



    def move_powder(self,cell):

        directions = [1,-1]
        random.shuffle(directions)

        for dx in directions:
            cell_dx = configC.MAP_OBJECT.get_cell(self.world_x+dx,self.world_y+1)
            if cell_dx == -1:
                continue
            self.grains_densite(cell, cell_dx, dx, 1)
            break


    def move_liquid(self, cell):
        directions = [1, -1]
        random.shuffle(directions)
        vitesse = 2
        
        for dx in directions:
            cell_dx = configC.MAP_OBJECT.get_cell(self.world_x + dx, self.world_y + 1)
            if cell_dx == -1:
                continue
            if self.grains_densite(cell, cell_dx, dx, 1):
                return 
        
        random.shuffle(directions)
        for direction_signe in directions:
            derniere_case_libre_x = 0
            
            for i in range(1, vitesse + 1):
                decalage_x = direction_signe * i
                cell_hx = configC.MAP_OBJECT.get_cell(self.world_x + decalage_x, self.world_y)
                
                if cell_hx == -1:
                    break
                if self.info_matiere[cell][1] <= self.info_matiere[cell_hx][1]:
                    break
                
                derniere_case_libre_x = decalage_x
            if derniere_case_libre_x != 0:
                cell_cible = configC.MAP_OBJECT.get_cell(self.world_x + derniere_case_libre_x, self.world_y)
                if self.grains_densite(cell, cell_cible, derniere_case_libre_x, 0):
                    return







    def find_max_hauteur_grains(self, cell_1):
        g = 1
        while True:
            cell_above = configC.MAP_OBJECT.get_cell(self.world_x, self.world_y - g)

            if cell_above == -1:     
                return -(g - 1)

            if self.info_matiere[cell_1][1] > self.info_matiere[cell_above][1]:      
                return -g
            
            if self.info_matiere[cell_1][1] <= self.info_matiere[cell_above][1]: 
                return -(g - 1)
            g += 1
                

            



    



    def tick_physics(self):
        configC.MAP_OBJECT.activate_dirty_chunks()
        for mesh in configC.MESH_LISTE:
            mesh.update_physique()

        for chunk_xy in list(configC.MAP_ACTIVE):
            self.had_change = self.update_chunks(chunk_xy)
            configC.MAP_OBJECT.desactivate_stable_chunk(chunk_xy, self.had_change)



    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.colision, daemon=True)  
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join() 

