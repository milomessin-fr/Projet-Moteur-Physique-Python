#import des fichiers
from tkinter import SOLID

from .widget import InterfaceCompteur
from .widget import Render
from .config import config_window as configW
from .config import config_collision as configC

#import pysdl
import sdl2 
import sdl2.ext 
import math







class SceneTEST:
    """scene de TEST"""
    def __init__(self, renderer, factory):
        configC.ENTITY = []
        self.render_grain = Render(renderer)
        self.renderer = renderer
        self.factory = factory
        self.spriterenderer = sdl2.ext.TextureSpriteRenderSystem(self.renderer)
        self.table_render = []
        self.ui_compteur = InterfaceCompteur(renderer, chemin_police=b"/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf", taille_police=20)        
        map = Map()
        map.create_map()
        configC.MAP_OBJECT = map
        


    def construire(self):
        sdl2.SDL_RenderClear(self.render_grain.renderer)
        self.render_grain.construire()
        self.ui_compteur.dessiner(analyse(), x=50, y=50, couleur_rgb=(255, 255, 255))
        self.renderer.present()









class Map:
    def __init__(self):
        self.size_chunk    = configC.CHUNK_SIZE
        self.height_border = configW.WINDOW_HEIGHT // configC.CELL_SIZE // self.size_chunk
        self.width_border  = configW.WINDOW_WIDTH  // configC.CELL_SIZE // self.size_chunk
        configC.WORLD_WIDTH  = self.width_border
        configC.WORLD_HEIGHT = self.height_border
        configC.MAP        = {}   
        configC.MAP_DIRTY  = set()
        configC.MAP_ACTIVE = set()

    def set_cell(self, world_x, world_y, grain_type): # place un grain à une position monde et marque le chunk dirty
        chunk_x = world_x // self.size_chunk
        chunk_y = world_y // self.size_chunk
        local_x = world_x % self.size_chunk
        local_y = world_y % self.size_chunk
        if (chunk_x, chunk_y) in configC.MAP:
            configC.MAP[(chunk_x, chunk_y)][(local_x, local_y)] = grain_type
            self.mark_dirty(chunk_x, chunk_y)
        return

    def get_cell(self, world_x, world_y):
        cx = world_x // self.size_chunk
        cy = world_y // self.size_chunk
        lx = world_x % self.size_chunk
        ly = world_y % self.size_chunk
        chunk = configC.MAP.get((cx, cy))
        if chunk is None:
            return -1  
        return chunk[(lx, ly)]
    
    def mark_dirty(self, chunk_x, chunk_y): # rend le chunk et ses voisins dirty    
        key = (chunk_x, chunk_y)
        if key in configC.MAP:
            configC.MAP_DIRTY.add(key)
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                neighbor = (chunk_x + dx, chunk_y + dy)
                if neighbor in configC.MAP:
                    configC.MAP_DIRTY.add(neighbor)
    
    def activate_dirty_chunks(self): # passe les dirty en actve
        configC.MAP_ACTIVE.update(configC.MAP_DIRTY)
        configC.MAP_DIRTY.clear()

    def desactivate_stable_chunk(self, chunk_key, had_change): #rendort le chunk si aucun mouvement
        if not had_change:
            configC.MAP_ACTIVE.discard(chunk_key)

    def create_chunk(self) -> dict:
        chunk = {}
        for i in range(self.size_chunk):
            for j in range(self.size_chunk):
                chunk[(i, j)] = 0
        return chunk

    def create_map(self) -> dict:
        for i in range(self.width_border):
            for j in range(self.height_border):
                configC.MAP[(i, j)] = self.create_chunk()









class RigidBody: # bloc unis
    def __init__(self, position_grille, info_type_id, radius):
        self.type_id = info_type_id
        self.radius = radius
        self.density = configC.INFO_OBJET[info_type_id][1]
        self.mass = round(((radius ** 2) * math.pi)) * self.density

        self.x = float(position_grille[0])
        self.y = float(position_grille[1])
        self.velocity_y = 0.0
        self.on_ground = False

        self.max_fall_speed = 16.0
        self.depth_counter = 0
        self.max_depth = 0
        self.positions_finales = {}


        self.mesh_relative = set(configC.MESH)
        self.bottom_pixels = self.extraire_bordure_basse()
        self.construire()


    def construire(self):
        cx, cy = int(round(self.x)), int(round(self.y))
        for rx, ry in self.mesh_relative:
            wx, wy = cx + rx, cy + ry
            cell = configC.MAP_OBJECT.get_cell(wx, wy)
            if cell == 0 or cell == self.type_id:
                configC.MAP_OBJECT.set_cell(wx, wy, self.type_id)

    def effacer(self):
        cx, cy = int(round(self.x)), int(round(self.y))
        for rx, ry in self.mesh_relative:
            wx, wy = cx + rx, cy + ry
            if configC.MAP_OBJECT.get_cell(wx, wy) == self.type_id:
                configC.MAP_OBJECT.set_cell(wx, wy, 0)

    def deplacer(self, new_cx, new_cy):
        old_cx, old_cy = int(round(self.x)), int(round(self.y))
        old_cells = {(old_cx + rx, old_cy + ry) for rx, ry in self.mesh_relative}
        new_cells = {(new_cx + rx, new_cy + ry) for rx, ry in self.mesh_relative}
        a_liberer = old_cells - new_cells
        a_occuper = new_cells - old_cells
        a_conserver = old_cells & new_cells

        for wx, wy in a_occuper:
            cell = configC.MAP_OBJECT.get_cell(wx, wy)
            if cell == -1:
                return False
            if cell == 0 or cell == self.type_id:
                continue
            cell_info = configC.INFO_OBJET.get(cell)
            if cell_info is None:
                return False
            if cell_info[2] == "solid" or self.mass <= cell_info[1]:
                return False

        deplaces = {(wx, wy): configC.MAP_OBJECT.get_cell(wx, wy)
                   for wx, wy in a_occuper
                   if configC.MAP_OBJECT.get_cell(wx, wy) != 0 and configC.MAP_OBJECT.get_cell(wx, wy) != self.type_id}

        for wx, wy in a_liberer:
            if configC.MAP_OBJECT.get_cell(wx, wy) == self.type_id:
                configC.MAP_OBJECT.set_cell(wx, wy, 0)  

        for wx, wy in a_occuper | a_conserver:
            configC.MAP_OBJECT.set_cell(wx, wy, self.type_id)

        self.search_place(deplaces,new_cx)      

        self.x = float(new_cx)
        self.y = float(new_cy)
        return True
    

    def search_place(self, deplaces, centre_x):
        place_prise = set()

        for (wx, wy), matiere_id in deplaces.items():
            direction_x = 1 if wx >= centre_x else -1
            x, y = wx, wy
            dest = None  # ← déjà là

            for _ in range(200):
                test_x = x + direction_x
                cell = configC.MAP_OBJECT.get_cell(test_x, y)

                if cell == 0 and (test_x, y) not in place_prise:
                    dest = (test_x, y)
                    break

                if cell == self.type_id:
                    direction_x *= -1
                    y -= 1
                    continue

                if cell == matiere_id:
                    dest = None  
                    while True:
                        y -= 1
                        cell_up = configC.MAP_OBJECT.get_cell(x, y)
                        if (x, y) in place_prise:
                            direction_x *= -1
                            break
                        if cell_up == 0:
                            dest = (x, y)
                            break
                        if cell_up == self.type_id:
                            direction_x *= -1
                            break
                        if cell_up != matiere_id and cell_up != 0:
                            direction_x *= -1
                            break
                    if dest:
                        break
                    continue

                y -= 1
                cell_up = configC.MAP_OBJECT.get_cell(x, y)
                if cell_up == self.type_id or cell_up == -1 or (x, y) in place_prise:
                    direction_x *= -1

            if dest is None:
                for dx, dy in [(direction_x, 0), (0, -1), (-direction_x, 0),
                            (direction_x, -1), (-direction_x, -1)]:
                    alt = (wx + dx, wy + dy)
                    if alt not in place_prise and configC.MAP_OBJECT.get_cell(*alt) == 0:
                        dest = alt
                        break

            if dest:
                place_prise.add(dest)
                configC.MAP_OBJECT.set_cell(dest[0], dest[1], matiere_id)


    def marquer_dirty(self):
        cx, cy = int(round(self.x)), int(round(self.y))
        chunks = set()
        for rx, ry in self.mesh_relative:
            wx = (cx + rx) // configC.CHUNK_SIZE
            wy = (cy + ry) // configC.CHUNK_SIZE
            chunks.add((wx, wy))
            chunks.add((wx, wy + 1))
        for cxy in chunks:
            if cxy in configC.MAP:
                configC.MAP_DIRTY.add(cxy)


    def extraire_bordure_basse(self):
        colonnes = {}
        for rx, ry in self.mesh_relative:
            if rx not in colonnes or ry > colonnes[rx]:
                colonnes[rx] = ry
        return [(rx, ry) for rx, ry in colonnes.items()]

    def extraire_bordure_haute(self):
        colonnes = {}
        for rx, ry in self.mesh_relative:
            if rx not in colonnes or ry < colonnes[rx]:
                colonnes[rx] = ry
        return [(rx, ry) for rx, ry in colonnes.items()]

    def scan_contact(self, sign):
        PRIORITE = {"wall": 5, "solid": 4, "powder": 3, "liquid": 2, "gaz": 1, None: 0}
        best_type, best_densite, best_restitution = None, 0.0, 0.0
        bordure = self.bottom_pixels if sign == 1 else self.extraire_bordure_haute()
        cx, cy = int(round(self.x)), int(round(self.y))

        for rx, ry in bordure:
            wx, wy = cx + rx, cy + ry + sign
            cell = configC.MAP_OBJECT.get_cell(wx, wy)

            if cell == -1:
                return "wall", 0.0, 0.0
            if cell == self.type_id or cell == 0:
                continue

            cell_info = configC.INFO_OBJET.get(cell)
            if cell_info is None:
                continue

            d = cell_info[1]
            contact_type = cell_info[2]

            if contact_type == "solid":
                if d >= 4:
                    restitution = min(0.85, d / (d + 1.0))
                    if PRIORITE[contact_type] > PRIORITE.get(best_type, 0):
                        best_type, best_densite, best_restitution = contact_type, d, restitution
                    elif contact_type == best_type and restitution > best_restitution:
                        best_densite, best_restitution = d, restitution
                continue

            if d == 0 or self.mass <= d:
                continue

            if PRIORITE.get(contact_type, 0) > PRIORITE.get(best_type, 0):
                best_type, best_densite = contact_type, d
            elif contact_type == best_type and d > best_densite:
                best_densite = d

        return best_type, best_densite, best_restitution


    def apply_friction(self, velocity, contact_type, contact_densite):
        if contact_type is None:
            return velocity * (1.0 - 0.01 * self.density)
        if contact_type == "wall":
            return 0.0
        if contact_type == "solid":
            coeff = 0.15 + (contact_densite * 0.05)
            return velocity * (1.0 - coeff)
        if contact_type == "powder":
            coeff = 0.1 + (contact_densite * 0.08)
            return velocity * (1.0 - coeff)
        if contact_type == "liquid":
            coeff = 0.05 + (contact_densite * 0.03)
            return velocity * (1.0 - coeff)
        return velocity

    def calculate_max_depth(self, contact_type, contact_densite):
        if contact_type is None or contact_type == "wall":
            return 0
        kinetic = 0.5 * self.mass * (self.velocity_y ** 2)
        if kinetic == 0:
            return 0
        if contact_type == "solid":
            return max(1, int(kinetic / (contact_densite * 100)))
        elif contact_type == "powder":
            return max(2, int(kinetic / (contact_densite * self.density * 15)))
        elif contact_type == "liquid":
            return max(5, int(kinetic / (contact_densite * self.density * 8)))
        return 0

    def compute_velocity(self, contact_type, contact_densite, restitution):
        kinetic = 0.5 * self.mass * (self.velocity_y ** 2)

        if contact_type in ("wall", "solid"):
            self.on_ground = True
            self.depth_counter = 0
            return 0.0

        if contact_type == "powder":
            drag_force = (contact_densite * self.density) * 50
            if kinetic < drag_force * 2:
                drag_force *= 1.2
            energy_remaining = max(0.0, kinetic - drag_force)
            speed = (2 * energy_remaining / self.mass) ** 0.5 if energy_remaining > 0 else 0.0
            if speed < 0.5:
                self.on_ground = True
                return 0.0
            speed = self.apply_friction(speed, contact_type, contact_densite)
            return speed * (1.0 if self.velocity_y >= 0 else -1.0)

        if contact_type == "liquid":
            drag_force = (contact_densite * self.density) * 20 * abs(self.velocity_y)
            energy_remaining = max(0.0, kinetic - drag_force)
            speed = (2 * energy_remaining / self.mass) ** 0.5 if energy_remaining > 0 else 0.0
            speed = self.apply_friction(speed, contact_type, contact_densite)
            return speed * (1.0 if self.velocity_y >= 0 else -1.0)

        return self.velocity_y


    def update_physique(self):
        if not self.on_ground:
            self.velocity_y = min(self.velocity_y + configC.GRAVITY, self.max_fall_speed)

        sign = 1 if self.velocity_y >= 0 else -1
        steps = max(1, int(abs(self.velocity_y)))

        for _ in range(steps):
            contact_type, contact_densite, restitution = self.scan_contact(sign)

            if contact_type in ("powder", "liquid") and self.depth_counter == 0:
                self.max_depth = self.calculate_max_depth(contact_type, contact_densite)

            if contact_type in ("powder", "liquid"):
                self.depth_counter += 1
                if self.depth_counter > self.max_depth:
                    self.on_ground = True
                    self.velocity_y = 0.0
                    break

            new_velocity = self.compute_velocity(contact_type, contact_densite, restitution)
            if new_velocity == 0.0:
                self.on_ground = True
                self.velocity_y = 0.0
                break

            future_cy = int(round(self.y)) + sign
            if not self.deplacer(int(round(self.x)), future_cy):
                self.on_ground = True
                self.velocity_y = 0.0
                self.depth_counter = 0
                break

            if contact_type not in ("powder", "liquid"):
                self.depth_counter = 0

            self.velocity_y = new_velocity
            sign = 1 if self.velocity_y >= 0 else -1
            if abs(self.velocity_y) < 0.5:
                self.on_ground = True
                self.velocity_y = 0.0
                self.depth_counter = 0
                break

        self.marquer_dirty()


def analyse():
    quantity = 0
    for chunk_xy in configC.MAP:
        chunk_data = configC.MAP[chunk_xy]
        for i in chunk_data:
            grain_type = chunk_data[i]
            if grain_type in (1,2,3,4):
                quantity += 1
    return quantity