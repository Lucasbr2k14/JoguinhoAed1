from random import randint
from sprites import Player, Enemy, Boss
from colision import Collision
from shot import Shot

class ShotList:
    def __init__(self, colision:Collision) -> None:
        self.collision:Collision = colision
        self.shotList:list[Shot] = []
        self.destroyList:list[int] = []
        self.id = 0

    def shot(self, x:float, y:float, velocity:int, player:bool):
        self.id += 1
        shot = Shot(x,y,velocity, self.id, player)
        self.shotList.append(shot)
        self.collision.addHitBox(shot.hitbox)

    def update(self) -> None:
        self.__deleteClass()
        for shot in self.shotList:
            shot.update()
        if len(self.shotList) > 0:
            for j in range(len(self.shotList)-1,  -1, -1):
                if self.shotList[j].y >= 200 or self.shotList[j].y <= 20:
                    self.destroy(self.shotList[j].id)

    def getByid(self, id:int) -> Shot | None:
        for i in range(len(self.shotList)):
            if self.shotList[i].id == id:
                return self.shotList[i]
        return None

    def clearShots(self):
        for i in range(len(self.shotList)):
            self.destroy(self.shotList[i].id)

    def destroy(self, id:int) -> None:
        self.destroyList.append(id)

    def __deleteClass(self) -> None:        
        if len(self.destroyList) > 0:
            for i in range(len(self.destroyList)-1, -1, -1):
                id = self.destroyList[i]
                for j in range(len(self.shotList)-1, -1, -1):
                    if self.shotList[j].id == id:
                        self.shotList[j].destory()
                        self.shotList.pop(j)
            self.destroyList.pop(i)
    
    def reset(self) -> None:
        self.clearShots()
        self.id = 0

    def draw(self):
        for shot in self.shotList:
            shot.draw()


class EnemyList:
    def __init__(self, screenHeigth:int, screenWidth:int, player:Player, shotList:ShotList, collision:Collision):
        self.player:Player = player
        self.shotList:ShotList = shotList
        self.collision:Collision = collision
        self.screenHeigth:int = screenHeigth
        self.screenWidth:int = screenWidth
        self.listEnemy:list[Enemy | Boss] = []
        self.destroyList:list[int] = []
        self.enemyStepInterval:float = 0
        self.probabilityShot:int = 1000
        self.id:int = 0

    def randomEnemy(self) -> None:
        x,y = randint(10,160), randint(1,5) * 26
        enemyType = randint(0,2)
        self.createEnemy(enemyType, x, y)

    def createEnemy(self, type:int, x:float, y:float, stepInterval:float):
        enemy:Enemy = Enemy(type, x, y, self.id, stepInterval, self.screenWidth, self.screenHeigth)
        self.listEnemy.append(enemy)
        self.collision.addHitBox(enemy.hitbox)
        self.id += 1

    def createBoss(self, x:int, y:int) -> None:
        boss:Boss = Boss(x, y, self.id) 
        self.listEnemy.append(boss)
        self.collision.addHitBox(boss.hitBox)
        self.id += 1

    def update(self, frameCount:int, frameRate:int) -> None:
        self.__deleteClass()
        for enemy in self.listEnemy:
            if type(enemy).__name__ != "Boss":
                enemy.updatePropietes(self.enemyStepInterval, self.probabilityShot)
            if type(enemy).__name__ == "Boss" and enemy.live <= 0:
                self.destroy(enemy.id)
            enemy.update(frameCount, frameRate, self.player.x, self.player.y, self.shotList)

    def getById(self, id:int) -> Enemy | Boss:
        for i in range(len(self.listEnemy)):
            if self.listEnemy[i].id == id:
                return self.listEnemy[i]

    def destroy(self, id:int) -> None:
        self.destroyList.append(id)

    def __deleteClass(self) -> None:
        if len(self.destroyList) > 0:
            for i in range(len(self.destroyList)-1, -1, -1):
                id = self.destroyList[i]
                for j in range(len(self.listEnemy)-1, -1, -1):
                    if self.listEnemy[j].id == id:
                        self.listEnemy[j].destroy()
                        self.listEnemy.pop(j)
                self.destroyList.pop(i)
    
    def clearEnemy(self):
        for i in range(len(self.listEnemy)):
            self.destroy(self.listEnemy[i].id)
    
    def reset(self) -> None:
        self.clearEnemy()
        self.enemyStepInterval = 0
        self.id = 0

    def draw(self, frameCount:int, frameRate:int) -> None:
        for enemy in self.listEnemy:
            enemy.draw(frameCount, frameRate)
            