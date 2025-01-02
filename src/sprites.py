import pyxel
from random import randint
from colision import HitBox, Collision

class Sprite:
    def __init__(self, x:float, y:float, velocity:float) -> None:
        self.x:float = x
        self.y:float = y
        self.velocity:float = velocity
        
    def draw(self, frameCount:int):
        pass

    def update(self, frameCount:int):
        pass

    def walk_up(self):
        self.y = self.y - self.velocity
    
    def walk_down(self):
        self.y = self.y + self.velocity

    def walk_rigth(self):
        self.x = self.x + self.velocity

    def walk_left(self):
        self.x = self.x - self.velocity


class Player(Sprite):
    def __init__(self) -> None:        
        super().__init__(100, 160, 2)
        self.lives:int = 3
        self.score:int = 0
        self.kills:int = 0
        self.sprite:int = 6
        self.inCooldown:bool = False
        self.colldownTime:float = 30 * 0.5
        self.lastShotFrame:int = 0
        self.index_image:tuple = (6, 0)
        self.hitbox:HitBox = HitBox(type(self), 0, self.x, self.y, 16, 16) 

    def update(self, frameCount:int) -> None:
        self.hitbox.update(self.x, self.y)
        self.__cooldownShot(frameCount)
    
    def shot(self, frameCount:int) -> None:
        self.lastShotFrame = frameCount
        self.inCooldown = True

    def kill(self) -> None:
        self.lives -= 1

    def addScore(self, poits:int) -> None:
        self.score += poits

    def __cooldownShot(self, frameCount:int) -> None:
        if (frameCount >= self.lastShotFrame + self.colldownTime) and self.inCooldown:
            self.inCooldown = False

    def draw(self) -> None:
        # self.hitbox.draw()
        pyxel.blt(self.x, self.y, 0, 16 * self.index_image[0], 16 * self.index_image[1], 16,16, 0)


class Boss(Sprite):
    def __init__(self):
        super().__init__()
        pass


class Enemy(Sprite):
    def __init__(self, enemy:int, x:float, y:float, id:int, screenHeigth:int, screenWidth:int) -> None:
        super().__init__(x, y, 2)
        self.screenHeigth:int = screenHeigth
        self.screenWidth:int  = screenWidth
        self.cooldownShot:float =  30 * 0.5
        self.stepInterval:float = 30 * 0.5
        self.id:int = id
        self.type:int = enemy
        self.hitbox:HitBox = HitBox(type(self), self.id, self.x, self.y, 16, 16)
        self.indexImage:list = [0,0]
        self.imageLoop:int = 0
        self.walk:int = 0
        self.nextStep:int = 0
        self.walkQuanti:int = 16

    def update(self, frameCount:int, frameRate:int) -> None:
        self.__walk(frameCount, frameRate)
        self.hitbox.update(self.x, self.y)

    def shot(self, playerX:int, playerY:int, shotList, collision:Collision):
        shot:bool = (1 == randint(1, 100))
        if playerX >= self.x and playerX-16 <= self.x and shot:
            shotList.shot(self.x, self.y, 2, False)

    def destroy(self):
        self.hitbox.destroy()

    def draw(self, frameCount:int, frameRate:int) -> None:
        self.indexImage[0] = (self.type * 2) + self.imageLoop
        pyxel.blt(self.x, self.y, 0, 16 * self.indexImage[0], 16 * self.indexImage[1], 16,16,0)

    def __walk(self, frameCount:int, frameRate:int):
        if frameCount >= self.nextStep:
            self.imageLoop = int(not self.imageLoop)
            self.walk_rigth()
            self.nextStep = frameCount +  self.stepInterval
        
