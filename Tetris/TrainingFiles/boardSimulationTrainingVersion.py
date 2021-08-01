
class TetrisSim:
    picked = {
        0:False,
        1:False,
        2:False,
        3:False,
        4:False,
        5:False,
        6:False,
    }
    speeds = {
        0:48,
        1:43,
        2:38,
        3:33,
        4:28,
        5:23,
        6:18,
        7:13,
        8:8,
        9:6,
        10:5,
        11:5,
        12:5,
        13:4,
        14:4,
        15:4,
        16:3,
        17:3,
        18:3,
        19:2,
        20:2,
        21:2,
        22:2,
        23:2,
        24:2,
        25:2,
        26:2,
        27:2,
        28:2,
    }
    def __init__(self,field,block,reserved):
        self.field = field
        self.currentBlock = block
        self.reserved = reserved
        self.nextShapes = None
        self.down=False
        self.gameOver = False
        self.height=24
        self.width = 10
        self.score = 0
        self.level=0

    def Drop(self):
        while not self.intersects():
            self.currentBlock.y+=1
        self.currentBlock.y-=1

        return self.placeBlock(),self.checkIfGameOver()

    def Down(self):
        if self.currentBlock is not None:
            self.currentBlock.y+=1
            if self.intersects():
                self.currentBlock.y-=1
                self.placeBlock()



    def Right(self):
        if self.currentBlock is not None:
            self.currentBlock.x+=1
            if self.intersects():
                self.currentBlock.x-=1

    def Left(self):
        if self.currentBlock is not None:
            self.currentBlock.x-=1
            if self.intersects():
                self.currentBlock.x+=1

    def Reserve(self):
        if self.reserved is None:
                self.reserved = self.currentBlock
                self.currentBlock=None
                return
        tempBlock=self.currentBlock
        self.currentBlock=self.reserved
        self.reserved = tempBlock

    def Rotates(self):
        if self.currentBlock is not None:
            oldRotation = self.currentBlock.rotate
            self.currentBlock.Rotate()
            if self.intersects():
                self.currentBlock.rotate=oldRotation

    def intersects(self):
        try:
            for i in range(4):
                for j in range(4):
                    if i*4+j in self.currentBlock.currentRotation():
                        if i+self.currentBlock.y > self.height -1 or j+ self.currentBlock.x > self.width-1 or self.currentBlock.x + j < 0 or self.field[i+self.currentBlock.y][j+self.currentBlock.x] != 0:
                            return True
            return False
        except IndexError:
            print(self.currentBlock.x,self.currentBlock.y)


    def placeBlock(self):
            if self.currentBlock.y>-25:
                for i in range(4):
                    for j in range(4):
                        if (i*4+j) in self.currentBlock.currentRotation():
                            self.field[i+self.currentBlock.y][j+self.currentBlock.x] = self.currentBlock.colour
            return self.scoreLines()

    def scoreLines(self):
        score=0
        for i in range(self.height):
            count=0
            for j in range(self.width):
                if self.field[i][j]!=0:
                    count+=1
            if count==self.width:
                score+=1
                for ii in range(i,0,-1):
                    for jj in range(0,self.width):
                        self.field[ii][jj]=self.field[ii-1][jj]
        #Score calculation taken from here: https://tetris.fandom.com/wiki/Scoring

        if score==1:
            self.score+= 40*(self.level+1)
        elif score ==2:
            self.score+= 100*(self.level+1)
        elif score ==3:
            self.score+= 300*(self.level+1)
        elif score ==4:
            self.score+= 1200*(self.level+1)
        return score

    def checkIfGameOver(self):
        self.currentBlock= self.nextShapes.pop(0)
        return self.intersects()

    def printBoard(self):
        print("new board")
        for x in self.field:
            row=""
            for y in x:
                if(y==0):
                    row=row+"-"
                else:
                    row=row+"+"
            print(row)

