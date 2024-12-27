from colision import HitBox
import pyxel

class Shot:
    def __init__(self, x:float,y:float, velocity:int, id:int, player:bool) -> None:
        self.x:float = x
        self.y:float = y
        self.id:int  = id
        self.player:bool = player
        self.velocity:int = velocity
        self.hitbox = HitBox(type(self), self.id, x ,y, 8, 2)
        self.index_image:tuple = (8, 0)
    
    def update(self) -> None:
        self.y += self.velocity
        self.hitbox.update(self.x, self.y)

    def destory(self) -> None:
        self.hitbox.destroy()

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16 * self.index_image[0] + 7, 16 * self.index_image[1] + 4, 2,8)
    