import pyxel

class HitBox:
    def __init__(self, name:str, id:int, element:type) -> None:
        self.name:str = name
        self.type:str = element.__name__
        self.id:int = id
        self.poits:list[list] = [[0,0],[0,0]]


class Collision:
    def __init__(self) -> None:
        self.listObjects:list[HitBox] = []
    
    def test(self) -> None:
        pass        

class Sprite:
    def __init__(self, x:float, y:float, velocity:float) -> None:
        self.x:float = x
        self.y:float = y
        self.velocity:float = velocity
        
    def draw(self, frameCout):
        pass

    def update(self, ):
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
        super().__init__(100, 100, 2)
        self.sprite:int = 6
        
        self.inCooldown:bool = False
        self.colldownTime:float = 30 * 1
        self.lastShotFrame:int = 0
    
    def shot(self, frameCount:int):
        self.lastShotFrame = frameCount

    def __cooldownShot(self, frameCount:int):
        if frameCount >= self.lastShotFrame + self.colldown:
            self.inCooldown = False

    def update(self, frameCount:int):
        self.__cooldownShot(frameCount)

    def draw(self):
        index_image:tuple = (6, 0)
        pyxel.blt(self.x, self.y, 0, 16 * index_image[0], 16 * index_image[1], 16,16)


class Shot:
    def __init__(self, x:float,y:float, velocity:int, player:bool) -> None:
        self.x:float = x
        self.y:float = y
        self.player:bool = player
        self.velocity:int = velocity
        self.index_image:tuple = (8, 0)
    
    def update(self) -> None:
        self.y += self.velocity

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16 * self.index_image[0], 16 * self.index_image[1], 16,16)


class ShotList:
    def __init__(self) -> None:
        self.shotList:list[Shot] = []

    def shot(self, x:float, y:float, velocity:int, player:bool):
        self.shotList.append(Shot(x,y,velocity,player))

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

        self.screen_width:int = 160
        self.screen_height:int = 160
        self.fps:int = 30

        self.frameCout:int = 0

        pyxel.init(self.screen_width, self.screen_height, title="Hello my game", fps=self.fps)

        self.load_imagens()

        # self.collision:Collision = Collision()
        self.player:Player = Player()
        self.shotList:ShotList = ShotList()

        pyxel.run(self.update, self.draw)

    def update(self):
        self.frameCout = pyxel.frame_count

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # Update class
        self.player.update(self.frameCout)

        # Keys
        if pyxel.btn(pyxel.KEY_LEFT): self.player.walk_left()
        if pyxel.btn(pyxel.KEY_RIGHT): self.player.walk_rigth()
        if pyxel.btnp(pyxel.KEY_SPACE): self.shotList.shot(self.player.x, self.player.y, -4, True)

        self.shotList.update()
       
    def draw(self):
        pyxel.cls(7)
        self.shotList.draw()
        self.player.draw()


    def load_imagens(self):
        pyxel.images[0].load(0,0, "../SpritesSheets/Sprites.png")

App()