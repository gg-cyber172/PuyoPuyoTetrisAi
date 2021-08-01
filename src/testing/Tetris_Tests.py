#pytest -q Tetris_Tests.py

import pytest
import sys
import pygame
sys.path.append("..")
from Tetris.Tetris import Tetris as tt

pygame.init()
screen = pygame.display.set_mode((1920,1080))
tetrisinst = tt()



class TestTetrisMethods():


    def test_useReserved(self):
        assert tetrisinst.reserved == None

        tetrisinst.newBlock()
        testblock = tetrisinst.currentBlock
        tetrisinst.useReserved()
        assert tetrisinst.reserved == testblock and tetrisinst.currentBlock == None

        tetrisinst.newBlock()
        testblock2 = tetrisinst.currentBlock
        tetrisinst.useReserved()

        assert tetrisinst.currentBlock == testblock and tetrisinst.reserved == testblock2

    def test_godrop(self):
        tetrisinst.newBlock()
        colour = tetrisinst.currentBlock.colour
        tetrisinst.currentBlock.x = -1# needs to be -1 to get into first pos on field
        tetrisinst.currentBlock.type = 0 #square
        testboard = tetrisinst.field

        testboard[23][0] = colour
        testboard[23][1] = colour
        testboard[22][0] = colour
        testboard[22][1] = colour

        tetrisinst.goDrop()

        assert testboard == tetrisinst.field

        tetrisinst.newBlock()
        colour = tetrisinst.currentBlock.colour
        tetrisinst.currentBlock.x = 2
        tetrisinst.currentBlock.type = 2 #t block
        
        testboard[23][2] = colour
        testboard[23][3] = colour
        testboard[23][4] = colour
        testboard[22][3] = colour
        
        tetrisinst.goDrop()

        assert testboard == tetrisinst.field

    def test_goDown(self):
        tetrisinst.newBlock()
        tetrisinst.currentBlock.y = 3
        tetrisinst.goDown()
        assert tetrisinst.currentBlock.y == 4

    def test_goRight(self):
        tetrisinst.newBlock()
        tetrisinst.currentBlock.type = 0 #square
        tetrisinst.currentBlock.y = 3
        tetrisinst.currentBlock.x = 5
        tetrisinst.goRight()
        assert tetrisinst.currentBlock.x == 6

        tetrisinst.currentBlock.x = 9
        tetrisinst.goRight()
        assert tetrisinst.currentBlock.x == 9

    def test_goLeft(self):
        tetrisinst.newBlock()
        tetrisinst.currentBlock.type = 0 #square
        tetrisinst.currentBlock.y = 3
        tetrisinst.currentBlock.x = 5
        tetrisinst.goLeft()
        assert tetrisinst.currentBlock.x == 4

        tetrisinst.currentBlock.x = -1
        tetrisinst.goLeft()
        assert tetrisinst.currentBlock.x == -1

    def test_rotate_line(self):
        tetrisinst.newBlock()
        tetrisinst.currentBlock.type = 1 #lineblock
        tetrisinst.currentBlock.y = 5
        tetrisinst.currentBlock.x = 5

        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 1
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 0
        tetrisinst.currentBlock.x = 9
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 0

    def test_rotate_tblock(self):
        tetrisinst.newBlock()
        tetrisinst.currentBlock.type = 2 #lineblock
        tetrisinst.currentBlock.y = 5
        tetrisinst.currentBlock.x = 5

        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 1
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 2
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 3
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 0

        tetrisinst.Rotate()#put it to 1
        tetrisinst.currentBlock.x = 9
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 1

        tetrisinst.currentBlock.x = -1
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 1

    def test_rotate_sblock(self):
        tetrisinst.newBlock()
        tetrisinst.currentBlock.type = 3 #sblock
        tetrisinst.currentBlock.y = 5
        tetrisinst.currentBlock.x = 5

        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 1
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 0
        
        tetrisinst.Rotate()
        tetrisinst.currentBlock.x = 9
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 1
    
    def test_rotate_zblock(self):
        tetrisinst.newBlock()
        tetrisinst.currentBlock.type = 4 #zblock
        tetrisinst.currentBlock.y = 5
        tetrisinst.currentBlock.x = 5

        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 1
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 0

        tetrisinst.Rotate()
        tetrisinst.currentBlock.x = -1
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 1
    
    def test_rotate_lblock(self):
        tetrisinst.newBlock()
        tetrisinst.currentBlock.type = 5 #lblock
        tetrisinst.currentBlock.y = 5
        tetrisinst.currentBlock.x = 5

        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 1
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 2
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 3
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 0

        tetrisinst.Rotate()
        tetrisinst.currentBlock.x = 9
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 1

        tetrisinst.currentBlock.x = 5
        tetrisinst.Rotate()
        tetrisinst.Rotate()
        tetrisinst.currentBlock.x = -1
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 3

    def test_rotate_jblock(self):
        tetrisinst.newBlock()
        tetrisinst.currentBlock.type = 5 #jblock
        tetrisinst.currentBlock.y = 5
        tetrisinst.currentBlock.x = 5

        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 1
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 2
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 3
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 0

        tetrisinst.Rotate()
        tetrisinst.currentBlock.x = -1
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 1

        tetrisinst.currentBlock.x = 5
        tetrisinst.Rotate()
        tetrisinst.Rotate()
        tetrisinst.currentBlock.x = 9
        tetrisinst.Rotate()
        assert tetrisinst.currentBlock.rotate == 3

    def test_placeblock(self):
        self.make_newfield()
        tetrisinst.newBlock()
        colour = tetrisinst.currentBlock.colour
        tetrisinst.currentBlock.x = -1# needs to be -1 to get into first pos on field
        tetrisinst.currentBlock.type = 0 #square
        testboard = tetrisinst.field

        testboard[23][0] = colour
        testboard[23][1] = colour
        testboard[22][0] = colour
        testboard[22][1] = colour

        tetrisinst.currentBlock.y = 23
        tetrisinst.placeBlock()

        assert testboard == tetrisinst.field


    def test_scorelines(self):
        self.make_newfield()


        self.make_lines(1)
        tetrisinst.level = 0
        tetrisinst.score = 0
        tetrisinst.scoreLines()
        assert tetrisinst.score == 40

        self.make_lines(2)
        tetrisinst.scoreLines()
        assert tetrisinst.score == 140

        self.make_lines(3)
        tetrisinst.scoreLines()
        assert tetrisinst.score == 440

        self.make_lines(4)
        tetrisinst.scoreLines()
        assert tetrisinst.score == 1640


        self.make_lines(1)
        tetrisinst.level = 5
        tetrisinst.score = 0
        tetrisinst.scoreLines()
        assert tetrisinst.score == 240

        self.make_lines(2)
        tetrisinst.scoreLines()
        assert tetrisinst.score == 840

        self.make_lines(3)
        tetrisinst.scoreLines()
        assert tetrisinst.score == 2640

        self.make_lines(4)
        tetrisinst.scoreLines()
        assert tetrisinst.score == 9840

    def test_addnusiance(self):
        self.make_newfield()
        tetrisinst.add_nusiance(2)
        num_empty = 0
        for j in range(2):
            for i in range(10):
                if tetrisinst.field[23-j][i] == 0:
                    num_empty +=1
        assert num_empty == 2

        tetrisinst.add_nusiance(4)
        num_empty = 0
        for j in range(6):
            for i in range(10):
                if tetrisinst.field[23-j][i] == 0:
                    num_empty +=1
        assert num_empty == 6




    def make_lines(self,num):
            for j in range(num):
                for i in range(10):
                    tetrisinst.field[23-j][i] = (155,155,155)

    def make_newfield(self):
        tetrisinst.field = []
        for i in range(24):#height
            newRow=[]
            for j in range(10):#width
                newRow.append(0)
            tetrisinst.field.append(newRow)


        
