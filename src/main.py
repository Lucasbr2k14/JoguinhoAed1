from random import randint
import pyxel

class HitBox:
    def __init__(self, element:type, id:int, x:int, y:int, h:int, w:int) -> None:
        self.type:str = element.__name__
        self.id:int = id
        self.heigth:int = h
        self.width:int = w
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
        for i in self.poits:
            pyxel.circ(i['x'], i['y'], 2, 7)


class Collision:
    def __init__(self) -> None:
        self.list:list[HitBox] = []
    
    def __testTwoElements(self, hitBoxA:HitBox, hitBoxB:HitBox) -> bool:
        
        
        coli = ((hitBoxA.poits[0]['y'] <= hitBoxB.poits[0]['y'] and hitBoxA.poits[2]['y'] <= hitBoxB.poits[0]['y']))
        

        if (hitBoxA.type == 'Player'):
            print('a', coli)


        if(coli and hitBoxA.type == 'Player'):
            print("Colisão")
            

    def addHitBox(self, hitbox:HitBox):
        self.list.append(hitbox)

    def addListHitBox(self, hitbox:list[HitBox]):
        for i in range(len(hitbox)):
            self.list.append(hitbox[i])

    def destroy(self, number:int):
        del self.list[number]

    def test(self) -> list[HitBox]:
        for i in range(len(self.list)):
            for j in range(len(self.list)):
                if(self.list[i] != self.list[j]):
                    self.__testTwoElements(self.list[i], self.list[j])


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
        self.sprite:int = 6
        self.inCooldown:bool = False
        self.colldownTime:float = 30 * 0.5
        self.lastShotFrame:int = 0
        self.index_image:tuple = (6, 0)
        self.hitbox:HitBox = HitBox(type(self), 0, self.x, self.y, 16, 16) 
    
    def shot(self, frameCount:int) -> None:
        self.lastShotFrame = frameCount
        self.inCooldown = True

    def __cooldownShot(self, frameCount:int) -> None:
        if (frameCount >= self.lastShotFrame + self.colldownTime) and self.inCooldown:
            self.inCooldown = False

    def update(self, frameCount:int) -> None:
        self.hitbox.update(self.x, self.y)
        self.__cooldownShot(frameCount)

    def getHitbox(self):
        return self.hitbox

    def draw(self) -> None:
        self.hitbox.draw()
        pyxel.blt(self.x, self.y, 0, 16 * self.index_image[0], 16 * self.index_image[1], 16,16, 0)


class Enemy(Sprite):
    def __init__(self, x:float, y:float, screenHeigth:int, screenWidth:int) -> None:
        
        super().__init__(x, y, 0.4)
        self.screenHeigth:int = screenHeigth
        self.screenWidth:int  = screenWidth
        self.hitbox = HitBox(type(self), self.x, self.y, 0, 16, 16)
        self.index_image = (0,0)

        self.walk = 0

    def update(self) -> None:
        
        # if self.x + 16 >= 200:
        #     self.walk = 1

        # if self.x <= 0:
        #     self.walk = 0

        # if self.walk == 0:
        #     self.walk_rigth()
        # else:
        #     self.walk_left()

        self.hitbox.update(self.x, self.y)

    def draw(self) -> None:
        self.hitbox.draw()
        pyxel.blt(self.x, self.y, 0, 16 * self.index_image[0], 16 * self.index_image[1], 16,16,0)


class EnemyList:
    def __init__(self, screenHeigth:int, screenWidth:int):
        self.listEnemy:list[Enemy] = []
        self.screenHeigth:int = screenHeigth
        self.screenWidth:int = screenWidth

    def update(self):
        for enemy in self.listEnemy:
            enemy.update()
    
    def draw(self):
        for enemy in self.listEnemy:
            enemy.draw()

    def randomEnemy(self):
        x,y = randint(10,160), randint(1,5) * 26
        enemy = Enemy(x,y,self.screenHeigth, self.screenWidth)
        self.listEnemy.append(enemy)
        return enemy.hitbox


class Shot:
    def __init__(self, x:float,y:float, velocity:int, id:int, player:bool) -> None:
        self.x:float = x
        self.y:float = y
        self.id:int  = id
        self.player:bool = player
        self.velocity:int = velocity
        self.hitbox = HitBox(type(self), x ,y ,id , 8, 2)
        self.index_image:tuple = (8, 0)
    
    def update(self) -> None:
        self.y += self.velocity
        self.hitbox.update(self.x, self.y)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16 * self.index_image[0] + 7, 16 * self.index_image[1] + 4, 2,8)
    
    def getHitbox(self) -> HitBox:
        return self.hitbox


class ShotList:
    def __init__(self) -> None:
        self.shotList:list[Shot] = []
        self.id = 0

    def shot(self, x:float, y:float, velocity:int, player:bool):
        self.id += 1
        shot = Shot(x,y,velocity,player, self.id)
        self.shotList.append(shot)
        return shot.hitbox

    def update(self):
        for shot in self.shotList:
            shot.update()

        if len(self.shotList) > 0:
            for i in range(len(self.shotList)-1,  -1, -1):
                if self.shotList[i].y >= 160 or self.shotList[i].y <= 0: self.destroy(i)

    def draw(self):
        for shot in self.shotList:
            shot.draw()

    def getHitBoxs(self) -> list[HitBox]:
        hitboxs = []

        for i in range(len(self.shotList)):
            hitboxs.append(self.shotList[i].hitbox)

        return hitboxs

    def destroy(self, shot:int):
        self.shotList.pop(shot)


class App:
    def __init__(self) -> None:

        self.screen_width:int = 200
        self.screen_height:int = 200
        self.fps:int = 30

        self.frameCout:int = 0

        pyxel.init(self.screen_width, self.screen_height, title="Hello my game", fps=self.fps)

        self.load_imagens()

        self.player:Player = Player()
        self.shotList:ShotList = ShotList()
        self.enemyList:EnemyList = EnemyList(self.screen_height, self.screen_width)
        self.collision:Collision = Collision()

        self.collision.addHitBox(self.player.getHitbox())

        pyxel.run(self.update, self.draw)

    def update(self):
        self.frameCout = pyxel.frame_count
        print("Frame count:", self.frameCout)    

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # Colision test

        self.collision.test()

        # Keys
        if pyxel.btn(pyxel.KEY_LEFT): self.player.walk_left()
        if pyxel.btn(pyxel.KEY_RIGHT): self.player.walk_rigth()
        if pyxel.btn(pyxel.KEY_UP): self.player.walk_up()
        if pyxel.btn(pyxel.KEY_DOWN): self.player.walk_down()

        if pyxel.btnp(pyxel.KEY_RETURN): 
            enemy = self.enemyList.randomEnemy()
            self.collision.addHitBox(enemy)

        if pyxel.btnp(pyxel.KEY_SPACE) and not self.player.inCooldown: 
            shot = self.shotList.shot(self.player.x+7, self.player.y, -4, True)
            self.collision.addHitBox(shot)
            self.player.shot(self.frameCout)

        print(len(self.collision.list))


        # Update class
        self.player.update(self.frameCout)
        self.enemyList.update()
        self.shotList.update()
       
    def draw(self):
        pyxel.cls(0)
        self.shotList.draw()
        self.enemyList.draw()
        self.player.draw()


    def load_imagens(self):
        pyxel.images[0].load(0, 0, "../SpritesSheets/Sprites.png")

App()