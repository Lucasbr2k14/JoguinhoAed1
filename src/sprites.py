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
        super().__init__(92, 160, 2)
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

    def gameOver(self):
        pass

    def __cooldownShot(self, frameCount:int) -> None:
        if (frameCount >= self.lastShotFrame + self.colldownTime) and self.inCooldown:
            self.inCooldown = False

    def draw(self) -> None:
        # self.hitbox.draw()
        pyxel.blt(self.x, self.y, 0, 16 * self.index_image[0], 16 * self.index_image[1], 16,16, 0)


class Boss(Sprite):
    def __init__(self, x:float, y:float, id:int) -> None:
        super().__init__(x, y, 2)

        self.live:int = 100
        self.id:int = id

        self.indexImage:list = [0,7] 
        self.animationRate:float = 30 * 1/2
        self.lastAnimateFrame:int = 0
        self.hitBox:HitBox = HitBox(type(self), self.id, self.x, self.y, 32, 32)

    def update(self, frameCount:int, frameRate:int, playerX:int, playerY:int, shotList) -> None:
        pass

    def draw(self, frameCount:int, frameRate:int) -> None:
        self.hitBox.draw()
        if frameCount >= self.lastAnimateFrame + self.animationRate:
            self.indexImage[0] = (self.indexImage[0] + 1) % 4
            self.lastAnimateFrame = frameCount

        pyxel.blt(self.x, self.y, 0, 32 * self.indexImage[0], 32 * self.indexImage[1], 32,32, 0)


class Enemy(Sprite):
    def __init__(self, enemy:int, x:float, y:float, id:int, screenHeigth:int, screenWidth:int) -> None:
        super().__init__(x, y, 2)
        self.stepInterval:float = 30 * 0.5
        self.coolDownTime:float =  30 * 2
        self.screenHeigth:int = screenHeigth
        self.screenWidth:int  = screenWidth
        self.id:int = id
        self.type:int = enemy
        self.lastShotFrame:int = 0
        self.probabilityShot:int = 400
        self.indexImage:list = [0,0]
        self.imageLoop:int = 0
        self.walkRigth:bool = True
        self.nextStep:int = 0
        self.walkQuanti:int = 20
        self.hitbox:HitBox = HitBox(type(self), self.id, self.x, self.y, 16, 16)

    def update(self, frameCount:int, frameRate:int, playerX:int, playerY:int, shotList) -> None:
        self.shot(playerX, playerY, frameCount, shotList)
        self.__walk(frameCount, frameRate)
        self.hitbox.update(self.x, self.y)

    def shot(self, playerX:int, playerY:int, frameCount:int, shotList):
        shot:bool = (1 == randint(1, self.probabilityShot))
        if (frameCount >= self.lastShotFrame + self.coolDownTime) and (shot):
            shotList.shot(self.x + 8, self.y + 16, 2, False)
            self.lastShotFrame = frameCount

    def destroy(self):
        self.hitbox.destroy()

    def draw(self, frameCount:int, frameRate:int) -> None:
        self.indexImage[0] = (self.type * 2) + self.imageLoop
        pyxel.blt(self.x, self.y, 0, 16 * self.indexImage[0], 16 * self.indexImage[1], 16,16,0)

    def __walk(self, frameCount:int, frameRate:int):
        if frameCount >= self.nextStep:
            self.imageLoop = int(not self.imageLoop)
            
            if self.walkRigth:
                self.walk_rigth()
                self.walkQuanti -= self.velocity
            else:
                self.walk_left()
                self.walkQuanti += self.velocity

            if self.walkQuanti <= 0 or self.walkQuanti >= 20:
                self.walkRigth = not self.walkRigth
                self.walk_down()

            self.nextStep = frameCount +  self.stepInterval
        