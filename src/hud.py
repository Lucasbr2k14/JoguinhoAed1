from sprites import Player
import pyxel

class HUD:
    def __init__(self, screen_width:int, screen_heigth:int, player:Player):
        self.player:Player = player
        self.screenWidth:int = screen_width
        self.screenHeigth:int = screen_heigth
        
    def draw(self):
        pyxel.rect(0, 21, self.screenWidth, 1, 7)
        for i in range(self.player.lives):
            pyxel.blt(20*i+1, 5, 0, 16 * 6, 16 * 0, 16,16, 0)
