

import threading


from ..config import config_window as configW
from ..config import config_collision as configC
from ..widget import Render as RenderWidget

class DebugMenu:
    def __init__(self):
        self.thread = threading.Thread(target=self.menu, daemon=True)
        self.thread.start()
        pass
    def stop(self):
        self.thread.join() 
        
    def menu(self):
        while True:
            input_debug = input("Commande debug >")
            if input_debug == "clear":
                self.clear_grain()
                print("Grains cleared.")

            elif input_debug == "setup ground":
                self.clear_grain()
                self.setup_ground()
                print("Ground setup completed.")
            
            elif input_debug == 'option stone':
                configW.MOUSE_OPTION = 2
                print("Mouse option set to stone.")

            elif input_debug == 'option sand':
                configW.MOUSE_OPTION = 1
                print("Mouse option set to sand.")
            
            elif input_debug == 'option clear':
                configW.MOUSE_OPTION = 0
                print("Mouse option set to clear.")


            else:
                try: 
                    exec(input_debug)
                except Exception as e:
                    print(f"Erreur : {e}")


    def clear_grain(self):
        for chunk_xy in configC.MAP:
            configC.MAP[chunk_xy] = {}
        
        configC.MAP_ACTIVE.clear()
        configC.MAP_DIRTY.clear()
        
        for chunk_xy in configC.MAP:
            configC.MAP_DIRTY.add(chunk_xy)



    def setup_ground(self):
        les_chunks_x = [cx for cx, cy in configC.MAP.keys()]
        les_chunks_y = [cy for cx, cy in configC.MAP.keys()]
        
        min_x, max_x = min(les_chunks_x), max(les_chunks_x)
        max_y = max(les_chunks_y)
        
        chunks_sol_y = range(max_y - 4, max_y + 1)
        
        for cy in chunks_sol_y:
            for cx in range(min_x, max_x + 1):
                chunk_xy = (cx, cy)
                if chunk_xy in configC.MAP:
                    for local_x in range(configC.CHUNK_SIZE):
                        for local_y in range(configC.CHUNK_SIZE):
                            configC.MAP[chunk_xy][(local_x, local_y)] = 1
                    
                    configC.MAP_DIRTY.add(chunk_xy)