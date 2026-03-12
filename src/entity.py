import sdl2.ext

class Carre:
    def __init__(self, sprite, x=0, y=0):
        self.sprite = sprite
        self.sprite.position = x, y
        self.sprite.owner = self
        self.x = x
        self.y = y
        self.vx = 100 
        self.vy = 100 

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        self.sprite.x = int(self.x)
        self.sprite.y = int(self.y)


