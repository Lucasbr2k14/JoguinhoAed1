from random import randint
import pyxel

class HitBox:
    def __init__(self, element:type, id:int, x:int, y:int, h:int, w:int) -> None:
        self.type:str = element.__name__
        self.id:int = id
        self.x:int = x
        self.y:int = y
        self.x1:int = 0
        self.y1:int = 0
        self.heigth:int = h
        self.width:int = w
    
    def update(self, x:int, y:int):
        self.x = x
        self.y = y; 
        self.x1 = self.x + self.width
        self.y1 = self.y + self.heigth
    
    def draw(self):
        pyxel.circ(self.x, self.y, 2, 7)
        pyxel.circ(self.x1, self.y1, 2, 7)

class Collision:
    def __init__(self) -> None:
        self.list:list[HitBox] = []
    
    def test(self) -> list[HitBox]:
        pass


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
    
    def shot(self, frameCount:int) -> None:
        self.lastShotFrame = frameCount
        self.inCooldown = True

    def __cooldownShot(self, frameCount:int) -> None:
        if (frameCount >= self.lastShotFrame + self.colldownTime) and self.inCooldown:
            self.inCooldown = False

    def update(self, frameCount:int) -> None:
        self.__cooldownShot(frameCount)

    def draw(self) -> None:
        index_image:tuple = (6, 0)
        pyxel.blt(self.x, self.y, 0, 16 * index_image[0], 16 * index_image[1], 16,16)


class Enemy(Sprite):
    def __init__(self, screenHeigth:int, screenWidth:int) -> None:
        
        super().__init__(10, 10, 0.4)
        self.screenHeigth:int = screenHeigth
        self.screenWidth:int  = screenWidth
        self.hitbox = HitBox(type(self), self.x, self.y, 0, 16, 16)
        self.index_image = (0,0)

        self.walk = 0

    def update(self) -> None:
        
        if self.x + 16>= 200:
            self.walk = 1

        if self.x <= 0:
            self.walk = 0

        if self.walk == 0:
            self.walk_rigth()
        else:
            self.walk_left()

        self.hitbox.update(self.x, self.y)

    def draw(self) -> None:
        pyxel.blt(self.x, self.y, 0, 16 * self.index_image[0], 16 * self.index_image[1], 16,16)

class EnemyList:
    def __init__(self):
        self.listEnemy:list[Enemy] = []
    
    def update(self):
        pass
    
    def draw(self):
        pass

    def random_enemy(self):
        pass

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

    def shot(self, x:float, y:float, velocity:int, player:bool):
        self.shotList.append(Shot(x,y,velocity,player, len(self.shotList)))

    def update(self):
        for i in range(len(self.shotList)):
            self.shotList[i].update()

    def draw(self):
        for i in range(len(self.shotList)):
            self.shotList[i].draw()

    def destroy(self, i:int):
        if i > 0 and i < len(self.shotList):
            del self.shotList[i]


class App:
    def __init__(self) -> None:

        self.screen_width:int = 200
        self.screen_height:int = 200
        self.fps:int = 30

        self.frameCout:int = 0

        pyxel.init(self.screen_width, self.screen_height, title="Hello my game", fps=self.fps)

        self.load_imagens()

        self.collision:Collision = Collision()
        self.player:Player = Player()
        self.shotList:ShotList = ShotList()
        self.enemy:Enemy = Enemy(self.screen_height, self.screen_width)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.frameCout = pyxel.frame_count

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # Colisions

        # Update class
        self.player.update(self.frameCout)

        # Keys
        if pyxel.btn(pyxel.KEY_LEFT): self.player.walk_left()
        if pyxel.btn(pyxel.KEY_RIGHT): self.player.walk_rigth()
        
        if pyxel.btnp(pyxel.KEY_SPACE) and not self.player.inCooldown: 
            self.shotList.shot(self.player.x+7, self.player.y, -4, True)
            self.player.shot(self.frameCout)

        self.enemy.update()
        self.shotList.update()
       
    def draw(self):
        pyxel.cls(0)
        self.shotList.draw()
        self.enemy.draw()
        self.player.draw()


    def load_imagens(self):
        pyxel.images[0].load(0,0, "../SpritesSheets/Sprites.png")

App()