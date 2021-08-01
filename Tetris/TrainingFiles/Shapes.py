import random
class Shapes:
    shapes = [
        [[1,2,5,6]],                                    # cube                              0123
        [[0,1,2,3],[1,5,9,13]],                         # Line Block                        4567
        [[1,4,5,6],[1,5,6,9],[4,5,6,9],[1,4,5,9],],     # T Block                           891011
        [[0,1,5,6],[2,5,6,9]],                          # S Block
        [[1,2,4,5],[0,4,5,9]],                          # Z Block
        [[2,4,5,6],[1,5,9,10],[4,5,6,8],[0,1,5,9]],     # L Block
        [[0,4,5,6],[1,2,5,9],[4,5,6,10],[1,5,8,9]]      # J Block
    ]


    def __init__(self,x,y,picked):
        self.picked = picked
        self.x,self.y,self.rotate =x,y,0
        self.type = self.chooseType()
        self.colour=(random.randint(0,200),random.randint(0,200),random.randint(0,200))

    def chooseType(self):
        toChooseFrom=[]
        for dicV in self.picked.keys():
            if not(self.picked[dicV]):
                toChooseFrom.append(dicV)
        if len(toChooseFrom):
            chosen=random.choice(toChooseFrom)
            self.picked[chosen]=True
            return chosen
        self.resetPicked()
        return self.chooseType()

    def resetPicked(self):
        for i in range(7):
            self.picked[i]=False

    def currentRotation(self):
        return self.shapes[self.type][self.rotate]

    def Rotate(self):
        if self.rotate<len(self.shapes[self.type])-1:
            self.rotate+=1
        else:
            self.rotate=0
        return self.rotate

    def __str__(self):
        result =""
        for i in range(4):
            for j in range(4):
                if (i*4+j) in self.currentRotation():
                    result= result+"+"
                else:
                    result = result +"-"
            result = result+"\n"
        return result
