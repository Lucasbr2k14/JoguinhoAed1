from colision import HitBox, Collision
from sprites import Player
from lists import EnemyList, ShotList
from hud import HUD, Menu, GameOverScreen
from solids import Floor
import pyxel

# Game level faz todo o gerenciamento das fases do jogo
class GameLevel:
    def __init__(self, player:Player, shotList:ShotList, enemyList:EnemyList):
        
        self.enemyStepIntervalIncrement:int = 50    # Em % esse incremento para cada inimigo eliminado aumentando a velicidade.
        self.enemyProbabilityShotDecrement:int = 20 # Em % esse decremento para a probalidade dos tiros dos inimigos
        self.enemyStepInterval:float = 30 * 1/1     # A o tempo em si em frames 
        self.enemyGrid:list[int] = [4,9]            # A grid que será incrementada o primeiro valor que são as colunas
        self.enemyProbabilityShot:int = 1000        # A probabilidade de tiro inicial


        self.player:Player = player
        self.shotList:ShotList =  shotList
        self.enemyList:EnemyList = enemyList
        self.gameLevel:int = 0
        self.gameOver:bool = False

    def update(self):

        self.enemyList.enemyStepInterval = self.enemyStepInterval - self.player.levelKills * (self.enemyStepIntervalIncrement/100)
        self.enemyList.probabilityShot = int(self.enemyProbabilityShot - self.player.score * (self.enemyProbabilityShotDecrement/100))

        if self.player.lives < 0:
            self.gameOver = True

        if len(self.enemyList.listEnemy) <= 0:
            self.player.nextLevel()
            self.shotList.clearShots()
            self.gameLevel += 1
            self.createLevel()
            self.enemyGrid[0] = min(self.enemyGrid[0]+1, 6)

    def createLevel(self):
        if self.gameLevel % 5 != 0:
            for j in range(0, self.enemyGrid[0]):
                for i in range(0, self.enemyGrid[1]):
                    x = i * 20
                    self.enemyList.createEnemy(j % 3, x, (j + 1) * 20, self.enemyStepInterval)
        else:   
            self.enemyList.createBoss(100,50)

    def reset(self):
        self.gameLevel = 0
        self.gameOver = False
        self.enemyGrid = [4,9]


# Classe principal do jogo
class Game:
    def __init__(self) -> None:
        self.screen_width:int = 200
        self.screen_height:int = 200
        self.frameRate:int = 30
        self.frameCout:int = 0
        self.showMenu:bool = True
        self.gameRuning:bool = False

        pyxel.init(self.screen_width, self.screen_height, title="Space Invaiders", fps=self.frameRate)

        self.load_imagens()

        self.player:Player =  Player()
        self.collision:Collision = Collision()
        self.shotList:ShotList = ShotList(self.collision)
        self.enemyList:EnemyList = EnemyList(self.screen_height, self.screen_width, self.player, self.shotList, self.collision)
        self.gameLevel:GameLevel = GameLevel(self.player, self.shotList, self.enemyList)
        self.menu:Menu = Menu(self.screen_width, self.screen_height)
        self.hud:HUD = HUD(self.screen_width, self.screen_height, self.player)
        self.gameOverScreen:GameOverScreen = GameOverScreen(self.screen_width, self.screen_height)
        self.floor:Floor = Floor(self.screen_width, self.screen_width)


        self.collision.addHitBox(self.player.hitbox)
        self.collision.addHitBox(self.floor.hitbox)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.frameCout = pyxel.frame_count  
        self.gameRuning = not self.gameLevel.gameOver

        self.keys()

        # Update class
        if self.gameRuning and not self.showMenu:
            self.colision()
            self.floor.update()
            self.gameLevel.update()
            self.player.update(self.frameCout)
            self.enemyList.update(self.frameCout, self.frameRate)
            self.shotList.update()

    def draw(self):
        pyxel.cls(0)
        if self.gameRuning and not self.showMenu:
            self.shotList.draw()
            self.enemyList.draw(self.frameCout, self.frameRate)
            self.hud.draw()
            self.player.draw()
        
        if self.showMenu:
            self.menu.draw(self.frameCout)

        if self.gameLevel.gameOver:
            self.gameOverScreen.draw()
    
    def keys(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE): 
            pyxel.quit()
        
        if pyxel.btn(pyxel.KEY_LEFT) and self.player.x >= 0+1: 
            self.player.walk_left()
        
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player.x <= self.screen_width - 17: 
            self.player.walk_rigth()

        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.gameLevel.gameOver:
                self.resetGame()
            if self.showMenu:
                self.showMenu = False

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
                    self.player.killEnemy()
                    self.enemyList.destroy(colisionList[i][0].id)
                    self.shotList.destroy(colisionList[i][1].id)
    
            if colisionList[i][0].type == "Player" and colisionList[i][1].type == "Shot":
                if not self.shotList.getByid(colisionList[i][1].id).player:
                    self.player.kill()
                    self.shotList.destroy(colisionList[i][1].id)

            if colisionList[i][0].type == "Boss" and colisionList[i][1].type == "Shot":
                if self.shotList.getByid(colisionList[i][1].id).player:
                    self.shotList.destroy(colisionList[i][1].id)
                    boss = self.enemyList.getById(colisionList[i][0].id)
                    boss.colisionPlayerShot()
            
            if colisionList[i][0].type == "Player" and colisionList[i][1].type == "Enemy":
                self.enemyList.destroy(colisionList[i][1].id)
                self.player.instaKill()

            if colisionList[i][0].type == "Shot" and colisionList[i][1].type == "Shot":
                self.shotList.destroy(colisionList[i][0].id)
                self.shotList.destroy(colisionList[i][1].id)
            
            if colisionList[i][0].type == "Floor" and colisionList[i][1].type == "Enemy":
                self.enemyList.destroy(colisionList[i][1].id)
                self.player.instaKill()

    def resetGame(self):
        self.player.reset()
        self.shotList.reset()
        self.enemyList.reset()
        self.gameLevel.reset()

    def load_imagens(self):
        pyxel.images[0].load(0, 0, "../SpritesSheets/Sprites.png") 


if __name__ == "__main__":
    Game()
