from random import randint
from colision import HitBox, Collision
from sprites import Boss, Enemy, Player
from shot import Shot
from lists import EnemyList, ShotList
from hud import HUD
import pyxel

class Game:
    def __init__(self) -> None:
        self.screen_width:int = 200
        self.screen_height:int = 200
        self.frameRate:int = 30
        self.frameCout:int = 0

        pyxel.init(self.screen_width, self.screen_height, title="Space Invaiders", fps=self.frameRate)

        self.load_imagens()

        self.player:Player =  Player()
        self.collision:Collision = Collision()
        self.shotList:ShotList = ShotList(self.collision)
        self.enemyList:EnemyList = EnemyList(self.screen_height, self.screen_width, self.player, self.shotList, self.collision)
        self.hud:HUD = HUD(self.screen_width, self.screen_height, self.player)

        self.collision.addHitBox(self.player.hitbox)

        for j in range(0, 6):
            for i in range(0, 9):
                x = i * 20
                self.enemyList.createEnemy(j % 3, x, (j + 1) * 20)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.frameCout = pyxel.frame_count  

        self.colision()
        self.keys()
       

        # Update class
        self.player.update(self.frameCout)
        self.enemyList.update(self.frameCout, self.frameRate)
        self.shotList.update()

    def keys(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE): pyxel.quit()
        if pyxel.btn(pyxel.KEY_LEFT): self.player.walk_left()
        if pyxel.btn(pyxel.KEY_RIGHT): self.player.walk_rigth()

        if pyxel.btnp(pyxel.KEY_RETURN):
           self.enemyList.randomEnemy()
           
        if pyxel.btnp(pyxel.KEY_SPACE) and not self.player.inCooldown: 
            self.shotList.shot(self.player.x+7, self.player.y, -4, True)
            self.player.shot(self.frameCout)

    def colision(self) -> None:
        colisionList:list[list[HitBox]] = self.collision.test()
        for i in range(len(colisionList)):
            if colisionList[i][0].type == "Enemy" and colisionList[i][1].type == "Shot":
                if(self.shotList.getByid(colisionList[i][1].id).player):
                    score = (self.enemyList.getById(colisionList[i][0].id).type+1) * 10
                    self.player.addScore(score)
                    self.enemyList.destroy(colisionList[i][0].id)
                    self.shotList.destroy(colisionList[i][1].id)
    
            if colisionList[i][0].type == "Player" and colisionList[i][1].type == "Shot":
                if not self.shotList.getByid(colisionList[i][1].id).player:
                    self.player.kill()
                    self.shotList.destroy(colisionList[i][1].id)

    def draw(self):
        pyxel.cls(0)
        self.shotList.draw()
        self.enemyList.draw(self.frameCout, self.frameRate)
        self.hud.draw()
        self.player.draw()

    def load_imagens(self):
        pyxel.images[0].load(0, 0, "../SpritesSheets/Sprites.png")


if __name__ == "__main__":
    Game()
