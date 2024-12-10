import pyxel

class Sprite:
    
    def __init__(self, x:int, y:int, velocity:int):
        self.x        = x
        self.y        = y
        self.velocity = velocity
        
    def draw(self):
        pass

    def update(self):
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
    def __init__(self):        
        super().__init__(100, 100, 2)
        self.sprite = 6
        
        self.
        self.cooldown = True

    def update(self):
        pass

    def draw(self): # Processa a imagem e anição do player

        index_image = (6, 0)

        pyxel.blt(self.x, self.y, 0, 16 * index_image[0], 16 * index_image[1], 16,16)

class Enemy(Sprite):
    def __init__(self):
        pass




class Shot:
    def __init__(self):
        self.shots = []
        
        self.shot_enemies = []

    def shot(self, posi_x, posi_y, player:bool=True):
        if player:
            self.shot_player[0] = posi_x
            self.shot_player[1] = posi_y

    def calculte_trajectory(self):
        self.shot_player[1] = self.shot_player[1] - self.player_velocity    

    def draw(self):
        pyxel.circ(self.shot_player[0], self.shot_player[1], 2, 7)


class App:
    def __init__(self) -> None:

        self.screen_width = 160
        self.screen_height= 120

        pyxel.init(self.screen_width, self.screen_height, title="Hello my game")

        self.load_imagens()

        self.player = Player()
        self.shot   = Shot(self.screen_width, self.screen_width)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_LEFT): self.player.walk_left()
        if pyxel.btn(pyxel.KEY_RIGHT): self.player.walk_rigth()

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.shot.shot(self.player.x, self.player.y)

        self.shot.calculte_trajectory()


    def draw(self):
        pyxel.cls(0)
        self.shot.draw()
        self.player.draw()


    def load_imagens(self):
        pyxel.images[0].load(0,0, "../SpritesSheets/Sprites.png")

App()