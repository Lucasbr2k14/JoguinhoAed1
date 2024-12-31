from sprites import Player
import pyxel

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
