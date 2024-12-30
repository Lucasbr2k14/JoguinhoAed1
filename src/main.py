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

        pyxel.init(self.screen_width, self.screen_height, title="Hello my game", fps=self.frameRate)

        self.load_imagens()

        self.shotList:ShotList = ShotList()
        self.player:Player = Player()
        self.hud:HUD = HUD(self.screen_height, self.screen_width)
        self.collision:Collision = Collision()
        self.enemyList:EnemyList = EnemyList(self.screen_height, self.screen_width, self.player, self.shotList, self.collision)

        self.collision.addHitBox(self.player.hitbox)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.frameCout = pyxel.frame_count  

        self.colision()
        self.keys()
       
        # Update class
        self.player.update(self.frameCout)
        self.enemyList.update()
        self.shotList.update()

    def keys(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE): pyxel.quit()
        if pyxel.btn(pyxel.KEY_LEFT): self.player.walk_left()
        if pyxel.btn(pyxel.KEY_RIGHT): self.player.walk_rigth()

        if pyxel.btnp(pyxel.KEY_RETURN):
            enemy = self.enemyList.randomEnemy()
            self.collision.addHitBox(enemy.hitbox)

        if pyxel.btnp(pyxel.KEY_SPACE) and not self.player.inCooldown: 
            shot = self.shotList.shot(self.player.x+7, self.player.y, -4, True)
            self.collision.addHitBox(shot)
            self.player.shot(self.frameCout)

    def colision(self):
        colisionList:list[list[HitBox]] = self.collision.test()
        print(colisionList)
        for i in range(len(colisionList)):
            if colisionList[i][0].type == "Enemy" and colisionList[i][1].type == "Shot":
                if(self.shotList.getByid(colisionList[i][1].id).player):
                    self.enemyList.destroy(colisionList[i][0].id)
                    self.shotList.destroy(colisionList[i][1].id)
        
            if (colisionList[i][0].type == "Enemy" and colisionList[i][1].type == "Enemy"):
                enemy1 = self.enemyList.getById(colisionList[i][0].id)
                enemy2 = self.enemyList.getById(colisionList[i][1].id)
                enemy1.walk = int(not enemy1.walk)
                enemy2.walk = int(not enemy2.walk)

            if (colisionList[i][0].type == "Player" and colisionList[i][1].type == "Shot"):
                if not self.shotList.getByid(colisionList[i][1].id).player:
                    self.player.kill()
                    self.shotList.destroy(colisionList[i][1].id)

    def draw(self):
        pyxel.cls(0)
        self.shotList.draw()
        self.enemyList.draw(self.frameCout, self.frameRate)
        self.player.draw()

    def load_imagens(self):
        pyxel.images[0].load(0, 0, "../SpritesSheets/Sprites.png")


if __name__ == "__main__":
    Game()
