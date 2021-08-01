import pygame
import random
from . import Shapes

class Tetris:
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
    def __init__(self):
        self.height=24
        self.width = 10
        self.field = []# Initialising the field with this for some reason breaks things [[0]*self.width]*self.height
        self.currentBlock = None
        self.score=0
        self.linesCleared=0
        self.level=0
        self.down=False
        self.gameOver = False
        self.reserved = None
        self.startX = (1920/2)-(self.width*(35/2))#The top left of the grid's x cord, 35 is how big each square is in units
        self.startY = (1080/2)-(self.height*(35/2))#The top left of the grid's y cord, 35 is how big each square is in units
        self.nextShapes=[]
        for i in range(3):
            self.picked=self.nextShapes.append(Shapes.Shapes(3,0,self.picked))
            self.picked=self.nextShapes[-1].picked
        for i in range(self.height):
            newRow=[]
            for j in range(self.width):
                newRow.append(0)
            self.field.append(newRow)

    def drawField(self,screen,pos = "null"):
        boxsize = int((max(screen.get_width(),screen.get_height())/2)/27)
        if pos == "null": 
            for i in range(self.height):
                for j in range(self.width):
                    pygame.draw.rect(screen, (0,0,0),[(screen.get_width()/2.75)+boxsize*j,(screen.get_height()/8)+boxsize*i,boxsize,boxsize],1)
                    #pygame.draw.rect(screen, (0,0,0),[self.startX+35*j,self.startY+35*i,35,35],1)
                    if self.field[i][j]!=0:
                        pygame.draw.rect(screen,self.field[i][j],[(screen.get_width()/2.75)+boxsize*j+1,(screen.get_height()/8)+boxsize*i+1,boxsize-2,boxsize-2])
        elif pos == "P1":
            for i in range(self.height):
                for j in range(self.width):
                    pygame.draw.rect(screen, (0,0,0),[(screen.get_width()/8)+boxsize*j,(screen.get_height()/8)+boxsize*i,boxsize,boxsize],1)
                    #pygame.draw.rect(screen, (0,0,0),[self.startX+35*j,self.startY+35*i,35,35],1)
                    if self.field[i][j]!=0:
                        pygame.draw.rect(screen,self.field[i][j],[(screen.get_width()/8)+boxsize*j+1,(screen.get_height()/8)+boxsize*i+1,boxsize-2,boxsize-2])

        elif pos == "P2":
            for i in range(self.height):
                for j in range(self.width):
                    pygame.draw.rect(screen, (0,0,0),[(screen.get_width()/1.5)+boxsize*j,(screen.get_height()/8)+boxsize*i,boxsize,boxsize],1)
                    #pygame.draw.rect(screen, (0,0,0),[self.startX+35*j,self.startY+35*i,35,35],1)
                    if self.field[i][j]!=0:
                        pygame.draw.rect(screen,self.field[i][j],[(screen.get_width()/1.5)+boxsize*j+1,(screen.get_height()/8)+boxsize*i+1,boxsize-2,boxsize-2])


    def newBlock(self):
        self.down = False
        self.currentBlock= self.nextShapes.pop(0)
        self.nextShapes.append(Shapes.Shapes(3,0,self.picked))
        self.picked=self.nextShapes[-1].picked
        if self.intersects():
            self.gameOver = True


    def drawBlock(self,screen,pos="null"):
        boxsize = int((max(screen.get_width(),screen.get_height())/2)/27)
        if pos == "null":
            for i in range(4):
                for j in range(4):
                    if (i*4+j) in self.currentBlock.currentRotation():
                        pygame.draw.rect(screen, (self.currentBlock.colour),[(screen.get_width()/2.75)+boxsize*(j+self.currentBlock.x)+1,(screen.get_height()/8)+boxsize*(i+self.currentBlock.y)+1,boxsize-2,boxsize-2])
        elif pos == "P1":
            for i in range(4):
                for j in range(4):
                    if (i*4+j) in self.currentBlock.currentRotation():
                        pygame.draw.rect(screen, (self.currentBlock.colour),[(screen.get_width()/8)+boxsize*(j+self.currentBlock.x)+1,(screen.get_height()/8)+boxsize*(i+self.currentBlock.y)+1,boxsize-2,boxsize-2])

        elif pos == "P2":
            for i in range(4):
                for j in range(4):
                    if (i*4+j) in self.currentBlock.currentRotation():
                        pygame.draw.rect(screen, (self.currentBlock.colour),[(screen.get_width()/1.5)+boxsize*(j+self.currentBlock.x)+1,(screen.get_height()/8)+boxsize*(i+self.currentBlock.y)+1,boxsize-2,boxsize-2])

    def useReserved(self):
        if self.reserved is None:
            self.reserved = self.currentBlock
            self.currentBlock=None
            return
        self.reserved.x=self.currentBlock.x
        self.reserved.y=self.currentBlock.y
        tempBlock=self.currentBlock
        self.currentBlock=self.reserved
        self.reserved = tempBlock


    def goDown(self):
        amount = 0
        if self.currentBlock is not None and not self.gameOver:
            self.currentBlock.y+=1
            if self.intersects():
                self.currentBlock.y-=1
                amount = self.placeBlock()
        return amount


    def goDrop(self):
        #TODO Fix bug of None
        if self.currentBlock is not None:
            while self.currentBlock is not None and not self.intersects() and not self.gameOver:
                self.currentBlock.y+=1
            self.currentBlock.y-=1
            return self.placeBlock()


    def goRight(self):
        if self.currentBlock is not None and not self.gameOver:
            self.currentBlock.x+=1
            if self.intersects():
                self.currentBlock.x-=1

    def goLeft(self):
        if self.currentBlock is not None and not self.gameOver:
            self.currentBlock.x-=1
            if self.intersects():
                self.currentBlock.x+=1


    def Rotate(self):
        if self.currentBlock is not None and not self.gameOver:
            oldRotation = self.currentBlock.rotate
            self.currentBlock.Rotate()
            if self.intersects():
                self.currentBlock.rotate=oldRotation

    def intersects(self):
            for i in range(4):
                for j in range(4):
                    if i*4+j in self.currentBlock.currentRotation():
                        if i+self.currentBlock.y > self.height -1 or j+ self.currentBlock.x > self.width-1 or self.currentBlock.x + j < 0 or self.field[i+self.currentBlock.y][j+self.currentBlock.x] != 0:
                            return True
            return False


    def placeBlock(self):
        #TODO Fix IndexError Here
        try:
            for i in range(4):
                for j in range(4):
                    if (i*4+j) in self.currentBlock.currentRotation():
                        self.field[i+self.currentBlock.y][j+self.currentBlock.x] = self.currentBlock.colour
            amount = self.scoreLines()
            self.currentBlock=None
            return amount
        except IndexError:
            print(i,j,self.currentBlock.x,self.currentBlock.y)

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
        self.linesCleared+=score
        if score==1:
            self.score+= 40*(self.level+1)
        elif score ==2:
            self.score+= 100*(self.level+1)
        elif score ==3:
            self.score+= 300*(self.level+1)
        elif score ==4:
            self.score+= 1200*(self.level+1)
        return score

    def pressDown(self):
        self.down = True

    def drawQueue(self,screen,pos="null"):
        boxsize = int((max(screen.get_width(),screen.get_height())/2)/27)
        shapeY=0
        if pos == "null":  
            for block in self.nextShapes:
                for i in range(4):#y                #pygame.draw.rect(screen, (0,0,0),[self.startX+35*j,self.startY+35*i,35,35],1)
                    for j in range(4):#x            #(1920/2)+(10*(36/2)),(1080/2)-(25*(35/2))
                        if (i*4+j) in block.currentRotation():
                            pygame.draw.rect(screen,(0,0,0), [((screen.get_width()/1.65)+(boxsize*j)),((screen.get_height()/8)+(boxsize*i)+(boxsize*shapeY*4)),boxsize,boxsize],2)
                            #pygame.draw.rect(screen,(0,0,0),[((1920/2)+(11*(34/2))+35*j),((1080/2)-(23*(35/2))+(35*i)+(35*shapeY*4)),50,50],1)
                            pygame.draw.rect(screen, (block.colour),[((screen.get_width()/1.65)+boxsize*j)+1,((screen.get_height()/8)+(boxsize*i)+(boxsize*shapeY*4))+1,boxsize-1,boxsize-1])
                shapeY+=1
        elif pos == "P1":
            for block in self.nextShapes:
                for i in range(4):#y                #pygame.draw.rect(screen, (0,0,0),[self.startX+35*j,self.startY+35*i,35,35],1)
                    for j in range(4):#x            #(1920/2)+(10*(36/2)),(1080/2)-(25*(35/2))
                        if (i*4+j) in block.currentRotation():
                            pygame.draw.rect(screen,(0,0,0), [((screen.get_width()/3)+(boxsize*j)),((screen.get_height()/8)+(boxsize*i)+(boxsize*shapeY*4)),boxsize,boxsize],2)
                            #pygame.draw.rect(screen,(0,0,0),[((1920/2)+(11*(34/2))+35*j),((1080/2)-(23*(35/2))+(35*i)+(35*shapeY*4)),50,50],1)
                            pygame.draw.rect(screen, (block.colour),[((screen.get_width()/3)+boxsize*j)+1,((screen.get_height()/8)+(boxsize*i)+(boxsize*shapeY*4))+1,boxsize-1,boxsize-1])
                shapeY+=1
        elif pos == "P2":
            for block in self.nextShapes:
                for i in range(4):#y                #pygame.draw.rect(screen, (0,0,0),[self.startX+35*j,self.startY+35*i,35,35],1)
                    for j in range(4):#x            #(1920/2)+(10*(36/2)),(1080/2)-(25*(35/2))
                        if (i*4+j) in block.currentRotation():
                            pygame.draw.rect(screen,(0,0,0), [((screen.get_width()/1.15)+(boxsize*j)),((screen.get_height()/8)+(boxsize*i)+(boxsize*shapeY*4)),boxsize,boxsize],2)
                            #pygame.draw.rect(screen,(0,0,0),[((1920/2)+(11*(34/2))+35*j),((1080/2)-(23*(35/2))+(35*i)+(35*shapeY*4)),50,50],1)
                            pygame.draw.rect(screen, (block.colour),[((screen.get_width()/1.15)+boxsize*j)+1,((screen.get_height()/8)+(boxsize*i)+(boxsize*shapeY*4))+1,boxsize-1,boxsize-1])
                shapeY+=1
        

    def drawReserve(self,screen,pos="null"):
        boxsize = int((max(screen.get_width(),screen.get_height())/2)/27)
        if pos == "null":
            if self.reserved is not None:
                for i in range(4):#y                #pygame.draw.rect(screen, (0,0,0),[self.startX+35*j,self.startY+35*i,35,35],1)
                    for j in range(4):#x            #(1920/2)+(10*(36/2)),(1080/2)-(25*(35/2))
                        if (i*4+j) in self.reserved.currentRotation():
                            pygame.draw.rect(screen,(0,0,0),[((screen.get_width()/3.5)+boxsize*j),((screen.get_height()/8)+(boxsize*i)),boxsize,boxsize],2)
                            pygame.draw.rect(screen, (self.reserved.colour),[((screen.get_width()/3.5)+boxsize*j)+1,((screen.get_height()/8)+(boxsize*i)+1),boxsize-1,boxsize-1])
        elif pos == "P1":
            if self.reserved is not None:
                for i in range(4):#y                #pygame.draw.rect(screen, (0,0,0),[self.startX+35*j,self.startY+35*i,35,35],1)
                    for j in range(4):#x            #(1920/2)+(10*(36/2)),(1080/2)-(25*(35/2))
                        if (i*4+j) in self.reserved.currentRotation():
                            pygame.draw.rect(screen,(0,0,0),[((screen.get_width()/22)+boxsize*j),((screen.get_height()/8)+(boxsize*i)),boxsize,boxsize],2)
                            pygame.draw.rect(screen, (self.reserved.colour),[((screen.get_width()/22)+boxsize*j)+1,((screen.get_height()/8)+(boxsize*i)+1),boxsize-1,boxsize-1])

        elif pos == "P2":
            if self.reserved is not None:
                for i in range(4):#y                #pygame.draw.rect(screen, (0,0,0),[self.startX+35*j,self.startY+35*i,35,35],1)
                    for j in range(4):#x            #(1920/2)+(10*(36/2)),(1080/2)-(25*(35/2))
                        if (i*4+j) in self.reserved.currentRotation():
                            pygame.draw.rect(screen,(0,0,0),[((screen.get_width()/1.7)+boxsize*j),((screen.get_height()/8)+(boxsize*i)),boxsize,boxsize],2)
                            pygame.draw.rect(screen, (self.reserved.colour),[((screen.get_width()/1.7)+boxsize*j)+1,((screen.get_height()/8)+(boxsize*i)+1),boxsize-1,boxsize-1])

    def speedCheck(self):
        if self.level>=29:
            return 1
        return self.speeds[self.level]

    def add_nusiance(self,value):
        #if value >= self.height():
           # self.gameOver = True
            #return
        for y in range(1,self.height):#go through all an move up
            for x in range(0,self.width):
                if self.field[y][x] != 0:
                    if y - value >= 0:
                        col = self.field[y][x]
                        self.field[y][x] = 0
                        self.field[y - value][x] = col
                    else:
                        self.gameOver = True
                        return
        emptypos = random.randint(0, 9)
        for y in range(self.height-value,self.height):
            for x in range(0,self.width):
                if x == emptypos:
                    pass
                else:
                    self.field[y][x] = (128, 128, 128)

    def drawnus(self,pos,value,screen):
        boxsize = int((max(screen.get_width(),screen.get_height())/2)/27)
        width = screen.get_width()
        height = screen.get_height()
        textfontnorm = pygame.font.SysFont("Calibri", 32,True)
        if pos == "P1":
            pygame.draw.rect(screen,(128, 128, 128),[width/12, height/1.2,boxsize * 2,boxsize * 2])
            num = textfontnorm.render(str(value),True, (0, 0, 0))
            numrect = num.get_rect()
            numrect.topleft = (width/10.45, height/1.17)
            screen.blit(num,numrect)
        if pos == "P2":
            pygame.draw.rect(screen,(128, 128, 128),[width/1.17,height/1.2,boxsize * 2,boxsize * 2])
            num = textfontnorm.render(str(value),True, (0, 0, 0))
            numrect = num.get_rect()
            numrect.topleft = (width/1.15, height/1.17)
            screen.blit(num,numrect)
        