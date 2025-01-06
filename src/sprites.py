import pyxel
from random import randint
from colision import HitBox, Collision

# Classe Sprite
# Classe onde define os principais metodos e propriedades para ser usados os sprites
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
    
    def walk_down(self, velocity:int=1):
        self.y = self.y + self.velocity * velocity

    def walk_rigth(self):
        self.x = self.x + self.velocity

    def walk_left(self):
        self.x = self.x - self.velocity


# Classe do player que herda da classe sprites
# Classe onde cuida da vida do player, cooldown dos tiros, quantas mortes o player fez e desenhar o ele na tela
class Player(Sprite):
    def __init__(self) -> None:        
        super().__init__(92, 160, 2)
        self.colldownTime:float = 30 * 1/2
        self.maxLives:int = 3
        self.score:int = 0
        self.kills:int = 0
        self.levelKills:int = 0
        self.sprite:int = 6
        self.inCooldown:bool = False
        self.lastShotFrame:int = 0
        self.index_image:tuple = (6, 0)
        self.lives:int = self.maxLives
        self.hitbox:HitBox = HitBox(type(self), 0, self.x, self.y, 16, 16) 

    def update(self, frameCount:int) -> None:
        self.hitbox.update(self.x, self.y)
        self.__cooldownShot(frameCount)
    
    def shot(self, frameCount:int) -> None:
        self.lastShotFrame = frameCount
        self.inCooldown = True

    def kill(self) -> None:
        self.lives -= 1

    def instaKill(self) -> None:
        self.lives = -1

    def killEnemy(self):
        self.kills += 1
        self.levelKills += 1

    def nextLevel(self):
        self.lives = min(self.lives+1, self.maxLives)
        self.levelKills = 0

    def addScore(self, poits:int) -> None:
        self.score += poits

    def reset(self):
        self.maxLives:int = 3
        self.score:int = 0
        self.kills:int = 0
        self.levelKills:int = 0
        self.sprite:int = 6
        self.inCooldown:bool = False
        self.lastShotFrame:int = 0
        self.lives:int = self.maxLives

    def __cooldownShot(self, frameCount:int) -> None:
        if (frameCount >= self.lastShotFrame + self.colldownTime) and self.inCooldown:
            self.inCooldown = False

    def draw(self) -> None:
        pyxel.blt(self.x, self.y, 0, 16 * self.index_image[0], 16 * self.index_image[1], 16,16, 0)


class Boss(Sprite):
    def __init__(self, x:float, y:float, id:int) -> None:
        super().__init__(x, y, 0.5)

        self.live:int = 100
        self.id:int = id

        self.coolDownTime:float =  30 * 1
        self.lastShotFrame:int = 0

        self.indexImage:list = [0,7] 
        self.animationRate:float = 30 * 1/2
        self.lastAnimateFrame:int = 0
        self.hitBox:HitBox = HitBox(type(self), self.id, self.x, self.y, 27, 27)


    def update(self, frameCount:int, frameRate:int, playerX:int, playerY:int, shotList) -> None:
        self.walk(playerX, playerY)
        self.shot(frameCount, shotList)
        self.hitBox.update(self.x, self.y)


    def walk(self, playerX:int, playerY:int):
        if playerX - 8 < self.x:
            self.walk_left()

        if playerX - 8 > self.x:
            self.walk_rigth()

    def shot(self, frameCount:int, shotList):

        if (frameCount >= self.lastShotFrame + self.coolDownTime):
            shotList.shot(self.x, self.y + 29, 2, False)
            shotList.shot(self.x + 16, self.y + 29, 2, False)
            shotList.shot(self.x + 32, self.y + 29, 2, False)
            self.lastShotFrame = frameCount

    def colisionPlayerShot(self):
        self.live -= 10

    def destroy(self):
        self.hitBox.destroy()

    def draw(self, frameCount:int, frameRate:int) -> None:
        if frameCount >= self.lastAnimateFrame + self.animationRate:
            self.indexImage[0] = (self.indexImage[0] + 1) % 4
            self.lastAnimateFrame = frameCount

        pyxel.blt(self.x, self.y, 0, 32 * self.indexImage[0], 32 * self.indexImage[1], 32,32, 0)


class Enemy(Sprite):
    def __init__(self, enemy:int, x:float, y:float, id:int, stepInterval:float, screenHeigth:int, screenWidth:int) -> None:
        super().__init__(x, y, 2)
        self.stepInterval:float = stepInterval
        self.coolDownTime:float =  30 * 1/2
        self.screenHeigth:int = screenHeigth
        self.screenWidth:int  = screenWidth
        self.id:int = id
        self.type:int = enemy
        self.lastShotFrame:int = 0
        self.probabilityShot:int = 1000
        self.indexImage:list = [0,0]
        self.imageLoop:int = 0
        self.walkRigth:bool = True
        self.nextStep:int = 0
        self.walkQuanti:int = 20
        self.hitbox:HitBox = HitBox(type(self), self.id, self.x, self.y, 16, 16)

    def update(self, frameCount:int, frameRate:int, playerX:int, playerY:int, shotList) -> None:
        self.shot(frameCount, shotList)
        self.__walk(frameCount, frameRate)
        self.hitbox.update(self.x, self.y)

    def shot(self, frameCount:int, shotList):
        shot:bool = (1 == randint(1, self.probabilityShot))

        if (frameCount >= self.lastShotFrame + self.coolDownTime) and (shot):
            shotList.shot(self.x + 8, self.y + 16, 2, False)
            self.lastShotFrame = frameCount

    def destroy(self):
        self.hitbox.destroy()

    def updatePropietes(self, stepInterval:float, probabilityShot:int) -> None:
        self.stepInterval = stepInterval
        self.probabilityShot = probabilityShot

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
                self.walk_down(2)

            self.nextStep = frameCount +  self.stepInterval
        
    def draw(self, frameCount:int, frameRate:int) -> None:
        self.indexImage[0] = (self.type * 2) + self.imageLoop
        pyxel.blt(self.x, self.y, 0, 16 * self.indexImage[0], 16 * self.indexImage[1], 16,16,0)