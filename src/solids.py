from colision import HitBox

class Floor:
    def __init__(self, screenWidth:int, screenHeigth:int):
        self.x = 0
        self.y = screenHeigth
        self.hitbox = HitBox(type(self), 0, 200, 0, 0, 200)
        self.destroyHitBox = False

    def update(self):
        self.hitbox.update(self.x, self.y)
