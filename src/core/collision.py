#import divers
import threading
import sdl2
import time
import random
#import de fichiers
from ..config import config_collision as config
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
                    self.update_stone_ball()
                    self.chunk_active()
                self.accumulator -= self.physics_dt
            sdl2.SDL_Delay(1)

    def update_stone_ball(self):
        if not config.MESH_LISTE:
            return
        boule_x, boule_y, boule_rayon = config.MESH_LISTE[0]
        prochain_y = boule_y + 1





    def chunk_active(self):
        active_chunks = list(config.MAP_ACTIVE)
        self.flip_flop = not self.flip_flop
        already_moved = set()
        
        for xy_chunk in active_chunks:
            chunk_data = config.MAP[xy_chunk]
            has_moved = False

            colonnes_x = range(config.CHUNK_SIZE) if self.flip_flop else range(config.CHUNK_SIZE - 1, -1, -1)

            for x in colonnes_x:
                for y in range(config.CHUNK_SIZE - 1, -1, -1):
                    if (xy_chunk, x, y) in already_moved:
                        continue
                        
                    if (x, y) not in chunk_data:
                        continue
                        
                    vitesse_actuelle = chunk_data[(x, y)]
                    
                    if vitesse_actuelle == 0:
                        continue

                    if vitesse_actuelle == 9:
                        continue #--- IGNORE --- Pierre immobile

                    if vitesse_actuelle == 5:
                        continue
                    
                    moved, dest_chunk, dest_x, dest_y = self.process_grain_physics_tracked(xy_chunk, x, y, vitesse_actuelle)
                    
                    if moved:
                        has_moved = True
                        already_moved.add((dest_chunk, dest_x, dest_y))

            if not has_moved:
                config.MAP_ACTIVE.discard(xy_chunk)



    def process_grain_physics_tracked(self, chunk_xy, x, y, vitesse):
        cases_parcourues, dest_chunk, dest_y = self.calculate_trajectory(chunk_xy, x, y, vitesse)

        if cases_parcourues > 0:
            nouvelle_vitesse = self.calculate_acceleration(vitesse)
            self.update_gravity(chunk_xy, x, y, dest_chunk, x, dest_y, nouvelle_vitesse)
            return True, dest_chunk, x, dest_y
        else:
            moved_diagonal, diag_chunk, diag_x, diag_y = self.check_diagonals(chunk_xy, x, y, vitesse)
            
            if moved_diagonal:
                self.update_gravity(chunk_xy, x, y, diag_chunk, diag_x, diag_y, 1)
                return True, diag_chunk, diag_x, diag_y
            else:
                self.handle_blocked_grain(chunk_xy, x, y, vitesse)
                return False, chunk_xy, x, y








    def check_diagonals(self, chunk_xy, x, y, vitesse):
        chunk_x, chunk_y = chunk_xy

        directions = []

        if random.random() < 0.5:
            directions = [-1, 1]
        else:
            directions = [1, -1]

        for dx in directions:
            prochain_x = x + dx
            prochain_y = y + 1
            prochain_chunk = chunk_xy

            if prochain_y == config.CHUNK_SIZE:
                prochain_chunk = (chunk_x, chunk_y + 1)
                prochain_y = 0

            cx, cy = prochain_chunk
            if prochain_x < 0:
                prochain_chunk = (cx - 1, cy)
                prochain_x = config.CHUNK_SIZE - 1
            elif prochain_x == config.CHUNK_SIZE:
                prochain_chunk = (cx + 1, cy)
                prochain_x = 0

            if prochain_chunk in config.MAP:
                if self.can_move_to(prochain_chunk, prochain_x, prochain_y):
                    return True, prochain_chunk, prochain_x, prochain_y

        return False, chunk_xy, x, y












    def calculate_trajectory(self, chunk_xy, x, y, vitesse):
        cases_parcourues = 0
        test_y = y
        test_chunk = chunk_xy
        chunk_x, chunk_y = chunk_xy

        for _ in range(vitesse):
            prochain_y = test_y + 1
            prochain_chunk = test_chunk
            chunk_x, chunk_y = test_chunk

            if prochain_y == config.CHUNK_SIZE:
                prochain_chunk = (chunk_x, chunk_y + 1)
                prochain_y = 0

            if prochain_chunk not in config.MAP:
                break

            if self.can_move_to(prochain_chunk, x, prochain_y):
                test_y = prochain_y
                test_chunk = prochain_chunk
                cases_parcourues += 1
            else:
                break

        return cases_parcourues, test_chunk, test_y

    def can_move_to(self, chunk_xy, x, y):
        return config.MAP[chunk_xy].get((x, y), 0) == 0

    def calculate_acceleration(self, vitesse_actuelle):
        return min(vitesse_actuelle + 1, config.MAX_VELOCITY_GRAINS)

    def handle_blocked_grain(self, chunk_xy, x, y, vitesse_actuelle):
        if vitesse_actuelle > 1:
            config.MAP[chunk_xy][(x, y)] = 1




    def update_gravity(self, src_chunk, src_x, src_y, dest_chunk, dest_x, dest_y, nouvelle_vitesse):
            config.MAP[src_chunk][(src_x, src_y)] = 0      
            config.MAP[dest_chunk][(dest_x, dest_y)] = nouvelle_vitesse   
            
            config.MAP_DIRTY.add(src_chunk)
            config.MAP_ACTIVE.add(src_chunk)
            
            if src_chunk != dest_chunk:
                config.MAP_DIRTY.add(dest_chunk)
                config.MAP_ACTIVE.add(dest_chunk)
                
            src_cx, src_cy = src_chunk
            
            if src_y == 0: 
                top = (src_cx, src_cy - 1)
                if top in config.MAP: config.MAP_ACTIVE.add(top)
            if src_x == 0: 
                left = (src_cx - 1, src_cy)
                if left in config.MAP: config.MAP_ACTIVE.add(left)
            if src_x == config.CHUNK_SIZE - 1: 
                right = (src_cx + 1, src_cy)
                if right in config.MAP: config.MAP_ACTIVE.add(right)

    def mark_chunks_modified(self, src_chunk, dest_chunk):
        config.MAP_DIRTY.add(src_chunk)
        config.MAP_ACTIVE.add(src_chunk)
        
        if src_chunk != dest_chunk:
            config.MAP_DIRTY.add(dest_chunk)
            config.MAP_ACTIVE.add(dest_chunk)

    def wake_up_neighbors(self, src_chunk, src_y):
        if src_y == 0:
            chunk_x, chunk_y = src_chunk
            top_chunk_xy = (chunk_x, chunk_y - 1)
            if top_chunk_xy in config.MAP:
                config.MAP_ACTIVE.add(top_chunk_xy)


    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.colision, daemon=True)  
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join() 

