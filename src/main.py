from random import randint
import pyxel

class HitBox:
    def __init__(self, element:type, id:int, x:int, y:int, h:int, w:int) -> None:
        self.type:str = element.__name__
        self.id:int = id
        self.heigth:int = h
        self.width:int = w
        self.destroyHitBox:bool = False
        self.poits:list = [
            {'x':0,'y':0},
            {'x':0,'y':0},
            {'x':0,'y':0},
            {'x':0,'y':0}
        ]

    def update(self, x:int, y:int) -> None:
        self.poits[0]['x'] = x
        self.poits[0]['y'] = y
        self.poits[3]['x'] = x + self.width
        self.poits[3]['y'] = y + self.heigth
        self.poits[1]['x'] = self.poits[3]['x']
        self.poits[1]['y'] = self.poits[0]['y']
        self.poits[2]['x'] = self.poits[0]['x']
        self.poits[2]['y'] = self.poits[3]['y']

    def draw(self):
        colors = [5, 2, 7, 3]
        for i in range(len(self.poits)):
            pyxel.circ(self.poits[i]['x'], self.poits[i]['y'], 2, colors[i])

    def destroy(self):
        self.destroyHitBox = True

    def __str__(self):
        return f"{self.type} id:{self.id}"


class Collision:
    def __init__(self) -> None:
        self.list:list[HitBox] = []
    
    def __testTwoElements(self, hitBoxA:HitBox, hitBoxB:HitBox) -> bool:
        poitsColision:list[bool] = [False, False, False, False]
        for i in range(0,4):
            poitsVerify:list[bool] = [
                hitBoxA.poits[0]['y'] <= hitBoxB.poits[i]['y'],
                hitBoxA.poits[2]['y'] >= hitBoxB.poits[i]['y'],
                hitBoxA.poits[0]['x'] <= hitBoxB.poits[i]['x'],
                hitBoxA.poits[1]['x'] >= hitBoxB.poits[i]['x'] 
            ]
            poitsColision[i] = (poitsVerify[0] and poitsVerify[1]) and (poitsVerify[2] and poitsVerify[3])
        return True in poitsColision

    def addHitBox(self, hitbox:HitBox):
        self.list.append(hitbox)

    def addListHitBox(self, hitbox:list[HitBox]):
        for i in range(len(hitbox)):
            self.list.append(hitbox[i])

    def destroy(self, number:int):
        del self.list[number]

    def test(self) -> list[HitBox]:
        for i in range(len(self.list)-1, -1, -1):
            if self.list[i].destroyHitBox:
                self.list.pop(i)
        
        listColisionFrame:list[HitBox] = []

        for i in range(len(self.list)):
            for j in range(len(self.list)):
                if(self.list[i] != self.list[j]):
                    coli = self.__testTwoElements(self.list[i], self.list[j])
                    if coli:
                        listColisionFrame.append([self.list[i], self.list[j]])
        
        return listColisionFrame
    

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
        self.poits:int = 0
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
        super().__init__(x, y, 0.4)
        self.screenHeigth:int = screenHeigth
        self.screenWidth:int  = screenWidth
        self.id:int = id
        self.type:int = enemy
        self.hitbox:HitBox = HitBox(type(self), self.id, self.x, self.y, 16, 16)
        self.index_image:list = [0,0]
        self.walk:int = 0
        
    def update(self) -> None:
        
        if self.x + 16 >= 200:
            self.walk = int(not self.walk)

        if self.x <= 0:
            self.walk = int(not self.walk)

        if self.walk == 0:
            self.walk_rigth()
        else:
            self.walk_left()

        self.hitbox.update(self.x, self.y)

    def destroy(self):
        self.hitbox.destroy()

    def draw(self, frameCount:int, frameRate:int) -> None:
        # self.hitbox.draw()
        self.index_image[0] = (self.type * 2) + int(frameCount/(frameRate/4) % 2)
        pyxel.blt(self.x, self.y, 0, 16 * self.index_image[0], 16 * self.index_image[1], 16,16,0)


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

class HUD:
    def __init__(self, screen_wdth:int, scren_heigth:int):
        pass
    
    def draw(self):
        pass

class Game:
    def __init__(self) -> None:

        self.screen_width:int = 200
        self.screen_height:int = 200
        self.frameRate:int = 30

        self.frameCout:int = 0

        pyxel.init(self.screen_width, self.screen_height, title="Hello my game", fps=self.frameRate)

        self.load_imagens()

        self.hud:HUD = HUD(self.screen_height, self.screen_width)
        self.player:Player = Player()
        self.shotList:ShotList = ShotList()
        self.enemyList:EnemyList = EnemyList(self.screen_height, self.screen_width)
        self.collision:Collision = Collision()

        self.collision.addHitBox(self.player.hitbox)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.frameCout = pyxel.frame_count  

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # Colision test

        colisionList:list[list[HitBox]] = self.collision.test()

        for i in range(len(colisionList)):
            if colisionList[i][0].type == "Enemy" and colisionList[i][1].type == "Shot":
                if(self.shotList.getByid(colisionList[i][1].id).player):
                    self.enemyList.destroy(colisionList[i][0].id)
                    self.shotList.destroy(colisionList[i][1].id)

            if colisionList[i][0].type == "Enemy" and colisionList[i][1].type == "Enemy":
                enemy1 = self.enemyList.getById(colisionList[i][0].id)
                enemy2 = self.enemyList.getById(colisionList[i][1].id)
                enemy1.walk = int(not enemy1.walk)
                enemy2.walk = int(not enemy2.walk)

                
        # Keys
        if pyxel.btn(pyxel.KEY_LEFT): self.player.walk_left()
        if pyxel.btn(pyxel.KEY_RIGHT): self.player.walk_rigth()


        if pyxel.btnp(pyxel.KEY_RETURN): 
            enemy = self.enemyList.randomEnemy()
            self.collision.addHitBox(enemy)

        if pyxel.btnp(pyxel.KEY_SPACE) and not self.player.inCooldown: 
            shot = self.shotList.shot(self.player.x+7, self.player.y, -4, True)
            self.collision.addHitBox(shot)
            self.player.shot(self.frameCout)

        # Update class
        self.player.update(self.frameCout)
        self.enemyList.update()
        self.shotList.update()
       
    def draw(self):
        pyxel.cls(0)
        self.shotList.draw()
        self.enemyList.draw(self.frameCout, self.frameRate)
        self.player.draw()


    def load_imagens(self):
        pyxel.images[0].load(0, 0, "../SpritesSheets/Sprites.png")

Game()