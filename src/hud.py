from sprites import Player
import pyxel

class Menu:
    def __init__(self, screen_width:int, screen_heigth:int) -> None:
        self.screenWidth:int = screen_width
        self.screenHeigth:int = screen_heigth

    def draw(self, frameCount:int):

        animate = int((frameCount/15) % 2)

        pyxel.text(62, 100-6, "PRESS ENTER TO START", 7)

        pyxel.blt(73, 120, 0, 16 * (0 + animate), 0, 16, 16, 0)
        pyxel.text(91, 125, "10 SCORE", 11)
        pyxel.blt(73, 136, 0, 16 * (2 + animate), 0, 16, 16, 0)
        pyxel.text(91, 140, "20 SCORE", 3)
        pyxel.blt(73, 152, 0, 16 * (4 + animate), 0, 16, 16, 0)
        pyxel.text(91, 156, "30 SCORE", 2)

class HUD:
    def __init__(self, screen_width:int, screen_heigth:int, player:Player) -> None:
        self.player:Player = player
        self.screenWidth:int = screen_width
        self.screenHeigth:int = screen_heigth
        
    def draw(self) -> None:
        pyxel.rect(0, 18, self.screenWidth, 1, 7)

        pyxel.text(5, 7, "SCORE: ", 7)
        pyxel.text(25+5, 7, str(int(self.player.score)), 3)

        pyxel.text(116, 7, "LIVES:", 7)

        for i in range(self.player.lives):
            pyxel.blt(20*i+140, 2, 0, 16 * 6, 16 * 0, 16,16, 0)


class GameOverScreen:
    def __init__(self, screen_width:int, screen_heigth:int):
        self.screenWidth:int = screen_width
        self.screenHeigth:int = screen_heigth

    def draw(self):
        pyxel.text((self.screenWidth/2)-(9*5)/2 + 5, (self.screenHeigth/2)-20, "GAME OVER", 7)
        pyxel.text((self.screenWidth/2)-(11*5)/2 + 5, (self.screenHeigth/2)-10, "PRESS ENTER",7)

