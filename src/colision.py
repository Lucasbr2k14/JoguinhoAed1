import pyxel

class HitBox:
    def __init__(self, element:type, id:int, x:int, y:int, h:int, w:int) -> None:
        self.type:str = element.__name__
        self.id:int = id
        self.heigth:int = h
        self.width:int = w
        self.destroyHitBox:bool = False
        self.poits:list = [
            {'x':0,'y':0},
            {'x':0,'y':0},
            {'x':0,'y':0},
            {'x':0,'y':0}
        ]

    def update(self, x:int, y:int) -> None:
        self.poits[0]['x'] = x
        self.poits[0]['y'] = y
        self.poits[3]['x'] = x + self.width
        self.poits[3]['y'] = y + self.heigth
        self.poits[1]['x'] = self.poits[3]['x']
        self.poits[1]['y'] = self.poits[0]['y']
        self.poits[2]['x'] = self.poits[0]['x']
        self.poits[2]['y'] = self.poits[3]['y']

    def draw(self):
        colors = [5, 2, 7, 3]
        for i in range(len(self.poits)):
            pyxel.circ(self.poits[i]['x'], self.poits[i]['y'], 2, colors[i])

    def destroy(self):
        self.destroyHitBox = True


class Collision:
    def __init__(self) -> None:
        self.list:list[HitBox] = []
    
    def __testTwoElements(self, hitBoxA:HitBox, hitBoxB:HitBox) -> bool:
        poitsColision:list[bool] = [False, False, False, False]
        for i in range(0,4):
            poitsVerify:list[bool] = [
                hitBoxA.poits[0]['y'] <= hitBoxB.poits[i]['y'],
                hitBoxA.poits[2]['y'] >= hitBoxB.poits[i]['y'],
                hitBoxA.poits[0]['x'] <= hitBoxB.poits[i]['x'],
                hitBoxA.poits[1]['x'] >= hitBoxB.poits[i]['x'] 
            ]
            poitsColision[i] = (poitsVerify[0] and poitsVerify[1]) and (poitsVerify[2] and poitsVerify[3])
        return True in poitsColision

    def addHitBox(self, hitbox:HitBox):
        self.list.append(hitbox)

    def addListHitBox(self, hitbox:list[HitBox]):
        for i in range(len(hitbox)):
            self.list.append(hitbox[i])

    def destroy(self, number:int):
        del self.list[number]

    def test(self) -> list[HitBox]:
        for i in range(len(self.list)-1, -1, -1):
            if self.list[i].destroyHitBox:
                self.list.pop(i)
        
        listColisionFrame:list[HitBox] = []

        for i in range(len(self.list)):
            for j in range(len(self.list)):
                if(self.list[i] != self.list[j]):
                    coli = self.__testTwoElements(self.list[i], self.list[j])
                    if coli and (not [self.list[j], self.list[i]] in listColisionFrame):
                        listColisionFrame.append([self.list[i], self.list[j]])

        return listColisionFrame

