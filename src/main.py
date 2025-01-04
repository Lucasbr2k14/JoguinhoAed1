from random import randint
from colision import HitBox, Collision
from sprites import Player
from lists import EnemyList, ShotList
from hud import HUD, GameOverScreen
import pyxel

class GameLevel:
    def __init__(self, player:Player, shotList:ShotList, enemyList:EnemyList):
        self.player:Player = player
        self.shotList:ShotList =  shotList
        self.enemyList:EnemyList = enemyList
        self.gameLevel:int = 0
        self.gameRuning:bool = True
        self.gameOver:bool = False

    def update(self):
        if self.player.lives < 0:
            self.gameRuning = False
            self.gameOver = True
            self.player.gameOver()

        if len(self.enemyList.listEnemy) <= 0:
            self.player.lives = min(self.player.lives+1, 3)
            self.gameLevel += 1
            self.createLevel()

    def createLevel(self):
        if self.gameLevel % 5 != 0:
            for j in range(0, 6):
                for i in range(0, 9):
                    x = i * 20
                    self.enemyList.createEnemy(j % 3, x, (j + 1) * 20)
        else:
            self.enemyList.createBoss(100,100)

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
        self.gameLevel:GameLevel = GameLevel(self.player, self.shotList, self.enemyList)
        
        self.hud:HUD = HUD(self.screen_width, self.screen_height, self.player)
        self.gameOverScreen:GameOverScreen = GameOverScreen(self.screen_width, self.screen_height)

        self.collision.addHitBox(self.player.hitbox)

        # self.enemyList.createBoss(100, 100)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.frameCout = pyxel.frame_count  

        self.colision()
        self.keys()

        # Update class
        self.gameLevel.update()
        self.player.update(self.frameCout)
        self.enemyList.update(self.frameCout, self.frameRate)
        self.shotList.update()

    def draw(self):
        pyxel.cls(0)
        if self.gameLevel.gameRuning:
            self.shotList.draw()
            self.enemyList.draw(self.frameCout, self.frameRate)
            self.hud.draw()
            self.player.draw()
        
        if self.gameLevel.gameOver:
            self.gameOverScreen.draw()
    
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



    def load_imagens(self):
        pyxel.images[0].load(0, 0, "../SpritesSheets/Sprites.png")


if __name__ == "__main__":
    Game()
