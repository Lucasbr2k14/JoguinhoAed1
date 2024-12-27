from random import randint
from sprites import Enemy
from shot import Shot

class EnemyList:
    def __init__(self, screenHeigth:int, screenWidth:int):
        self.listEnemy:list[Enemy] = []
        self.screenHeigth:int = screenHeigth
        self.screenWidth:int = screenWidth
        self.destroyList:list[int] = []
        self.id:int = 0

    def randomEnemy(self):
        x,y = randint(10,160), randint(1,5) * 26
        enemyType = randint(0,2)
        enemy = Enemy(enemyType, x,y,self.id, self.screenHeigth, self.screenWidth)
        self.listEnemy.append(enemy)
        self.id += 1
        return enemy.hitbox

    def update(self):
    
        self.__deleteClass()

        for enemy in self.listEnemy:
            enemy.update()

    def getById(self, id:int) -> Enemy:
        for i in range(len(self.listEnemy)):
            if self.listEnemy[i].id == id:
                return self.listEnemy[i]

    def draw(self, frameCount:int, frameRate:int):
        for enemy in self.listEnemy:
            enemy.draw(frameCount, frameRate)

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


class ShotList:
    def __init__(self) -> None:
        self.shotList:list[Shot] = []
        self.destroyList:list[int] = []
        self.id = 0

    def shot(self, x:float, y:float, velocity:int, player:bool):
        self.id += 1
        shot = Shot(x,y,velocity, self.id, player)
        self.shotList.append(shot)
        return shot.hitbox

    def update(self) -> None:
        self.__deleteClass()
        for shot in self.shotList:
            shot.update()
        if len(self.shotList) > 0:
            for j in range(len(self.shotList)-1,  -1, -1):
                if self.shotList[j].y >= 200 or self.shotList[j].y <= 0:
                    self.destroy(self.shotList[j].id)

    def draw(self):
        for shot in self.shotList:
            shot.draw()

    def getByid(self, id:int) -> Shot | None:
        for i in range(len(self.shotList)):
            if self.shotList[i].id == id:
                return self.shotList[i]
        return None

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
