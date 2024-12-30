import pyxel

class HUD:
    def __init__(self, screen_wdth:int, scren_heigth:int):
        self.playerLives:int = 0
        



    def draw(self):
        pyxel.text(100, 10, f"Lives: {self.playerLives}")
