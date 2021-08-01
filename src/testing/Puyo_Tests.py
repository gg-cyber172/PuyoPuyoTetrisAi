#pytest -q Puyo_Tests.py

import pytest
import sys
import pygame
sys.path.append("..")
from PuyoPuyo.puyo_puyo import puyo_puyo as pp

pygame.init()
screen = pygame.display.set_mode((1920,1080))
puyoinst = pp(screen)



class TestPuyoMethods():


    def test_moveleft(self):

        #default value for x1,x2 = 2
        puyoinst.currentpuyoblock = puyoinst.getnewpuyo()
        puyoinst.moveleft()
        assert (puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"]) == (1,1)

        puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"] = 4,3
        puyoinst.moveleft()
        assert (puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"]) == (3,2)

        puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"] = 0,0
        puyoinst.moveleft()
        assert (puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"]) == (0,0)


    def test_moveright(self):
        #default value for x1,x2 = 2
        puyoinst.currentpuyoblock = puyoinst.getnewpuyo()
        puyoinst.moveright()
        assert (puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"]) == (3,3)

        puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"] = 2,3
        puyoinst.moveright()
        assert (puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"]) == (3,4)

        puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"] = 5,5
        puyoinst.moveright()
        assert (puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"]) == (5,5)


    def test_movedown(self):
        #default value for y1,y2 = -1,0
        puyoinst.currentpuyoblock = puyoinst.getnewpuyo()
        puyoinst.movedown()
        assert (puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"]) == (0,1)

        puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"] = 8,7
        puyoinst.movedown()
        assert (puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"]) == (9,8)

        puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"] = 12,11
        puyoinst.movedown()
        assert (puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"]) == (12,11)


    def test_rotate(self):
        #default value for rotation = [1,4]
        puyoinst.currentpuyoblock = puyoinst.getnewpuyo()
        puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"] = 5,6
        puyoinst.rotate()
        assert (puyoinst.currentpuyoblock["rotation"]) == ([4,5])

        puyoinst.rotate()
        assert (puyoinst.currentpuyoblock["rotation"]) == ([4,7])
        puyoinst.rotate()

        assert (puyoinst.currentpuyoblock["rotation"]) == ([3,4])
        puyoinst.rotate()
        assert (puyoinst.currentpuyoblock["rotation"]) == ([1,4])

        puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"] = 5,5
        puyoinst.rotate()
        assert (puyoinst.currentpuyoblock["rotation"]) == ([1,4])

        puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"] = 0,0
        puyoinst.currentpuyoblock["rotation"] = [4,7]
        puyoinst.rotate()
        assert (puyoinst.currentpuyoblock["rotation"]) == ([4,7])


    def test_isvalidmovement(self):
        puyoinst.currentpuyoblock = puyoinst.getnewpuyo()
        puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"] = 2,2
        puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"] = 5,6
        assert (puyoinst.isvalidmovement("left")) == True
        puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"] = 0,0
        assert (puyoinst.isvalidmovement("left")) == False
        assert (puyoinst.isvalidmovement("right")) == True
        puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"] = 5,5
        assert (puyoinst.isvalidmovement("right")) == False

        # default is [1,4]
        assert (puyoinst.isvalidmovement("rotate")) == False
        puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"] = 4,4
        assert (puyoinst.isvalidmovement("rotate")) == True

        puyoinst.currentpuyoblock["rotation"] = [4,7]
        assert (puyoinst.isvalidmovement("rotate")) == True
        puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"] = 0,0
        assert (puyoinst.isvalidmovement("rotate")) == False

        puyoinst.currentpuyoblock["rotation"] = [4,7]
        puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"] = 0,0
        assert (puyoinst.isvalidmovement("rotate")) == False

        puyoinst.currentpuyoblock["rotation"] = [1,4]
        puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"] = 0,1
        assert (puyoinst.isvalidmovement("rotate")) == True
        puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"] = 10,11
        assert (puyoinst.isvalidmovement("down")) == False

        puyoinst.currentpuyoblock["rotation"] = [3,4]
        puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"] = 10,10
        assert (puyoinst.isvalidmovement("down")) == True
        puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"] = 11,11
        assert (puyoinst.isvalidmovement("down")) == False


    def test_addtoboard(self):
        puyoinst.currentpuyoblock = puyoinst.getnewpuyo()
        puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"] = 0,1
        puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"] = 11,11
        emptyboard = puyoinst.getstartboard()

        puyoinst.addtoboard(puyoinst.currentpuyoblock, "pos")
        assert emptyboard != puyoinst.board

        board2 = puyoinst.board
        puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"] = 1,2
        puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"] = 10,11
        board2[puyoinst.currentpuyoblock["y1"]][puyoinst.currentpuyoblock["x1"]] = puyoinst.currentpuyoblock["colours"][0]
        board2[puyoinst.currentpuyoblock["y2"]][puyoinst.currentpuyoblock["x2"]] = puyoinst.currentpuyoblock["colours"][1]

        puyoinst.currentpuyoblock["x1"],puyoinst.currentpuyoblock["x2"] = 1,2
        puyoinst.currentpuyoblock["y1"],puyoinst.currentpuyoblock["y2"] = 10,10

        puyoinst.addtoboard(puyoinst.currentpuyoblock, "pos")
        assert board2 == puyoinst.board

    def test_chaincheckandremove(self):
        
        puyoinst.board = puyoinst.getstartboard()
        testboard = puyoinst.getstartboard()
        puyoinst.board[11][0] = (155, 0, 0)
        puyoinst.board[11][1] = (155, 0, 0)
        puyoinst.board[11][2] = (155, 0, 0)

        puyoinst.board[10][0] = (0, 155, 0)
        puyoinst.board[10][1] = (0, 155, 0)
        puyoinst.board[10][2] = (0, 155, 0)

        puyoinst.board[9][0] = (155, 0, 0)

        testboard = puyoinst.getstartboard()
        testboard[11][3] = (0, 0, 155)

        block = puyoinst.getnewpuyo()
        block["colours"] = ((0, 155, 0),(0, 0, 155))
        block["x1"] = 3
        block["x2"] = 3
        block["y1"] = 10
        block["y2"] = 11

        puyoinst.board[10][3] = (0, 155, 0)
        puyoinst.board[11][3] = (0, 0, 155)

        puyoinst.chaincheckandremove(block,"pos")
        assert testboard == puyoinst.board


    def test_scorelines(self):
        puyoinst.board = puyoinst.getstartboard()
        testboard = puyoinst.getstartboard()
        puyoinst.board[11][0] = (155, 0, 0)
        puyoinst.board[11][1] = (155, 0, 0)
        puyoinst.board[11][2] = (155, 0, 0)

        puyoinst.board[10][0] = (0, 155, 0)
        puyoinst.board[10][1] = (0, 155, 0)
        puyoinst.board[10][2] = (0, 155, 0)

        puyoinst.board[9][0] = (155, 0, 0)
        
        puyoinst.currentpuyoblock = puyoinst.getnewpuyo()
        puyoinst.currentpuyoblock["colours"] = ((0, 155, 0),(0, 0, 155))
        puyoinst.currentpuyoblock["x1"] = 3
        puyoinst.currentpuyoblock["x2"] = 3
        puyoinst.currentpuyoblock["y1"] = 10
        puyoinst.currentpuyoblock["y2"] = 11

        assert 91 == puyoinst.scoreLines("pos")

        puyoinst.board = puyoinst.getstartboard()
        testboard = puyoinst.getstartboard()
        puyoinst.board[11][0] = (155, 0, 0)
        puyoinst.board[11][1] = (155, 0, 0)
        puyoinst.board[11][2] = (155, 0, 0)

        puyoinst.board[10][0] = (0, 155, 0)
        puyoinst.board[10][1] = (0, 155, 0)
        puyoinst.board[10][2] = (0, 155, 0)

        puyoinst.board[9][0] = (155, 0, 0)
        
        puyoinst.currentpuyoblock = puyoinst.getnewpuyo()
        puyoinst.currentpuyoblock["colours"] = ((0, 155, 0),(0, 0, 155))
        puyoinst.currentpuyoblock["x1"] = 3
        puyoinst.currentpuyoblock["x2"] = 3
        puyoinst.currentpuyoblock["y1"] = 10
        puyoinst.currentpuyoblock["y2"] = 11

        puyoinst.board[11][4] = (0, 0, 155)
        puyoinst.board[11][5] = (0, 0, 155)
        puyoinst.board[10][5] = (0, 0, 155)

        assert 91 != puyoinst.scoreLines("pos")

    def test_removegrey(self):

        testboard = puyoinst.getstartboard()
        testboard[11][0] = (128, 128, 128)
        testboard[11][1] = (128, 128, 128)

        puyoinst.board = puyoinst.getstartboard()
        puyoinst.board[11][0] = (128, 128, 128)
        puyoinst.board[11][1] = (128, 128, 128)
        puyoinst.board[11][2] = (128, 128, 128)
        puyoinst.board[10][2] = (128, 128, 128)

        puyoinst.board[11][4] = (128, 128, 128)
        puyoinst.board[10][4] = (128, 128, 128)

        puyoinst.removegrey([(10,3),(11,3)])

        assert testboard == puyoinst.board
        

    def test_movedownfloating(self):

        testboard = puyoinst.getstartboard()
        testboard[11][0] = (155, 0, 0)
        testboard[11][1] = (155, 0, 0)

        testboard[11][2] = (0, 155, 0)
        testboard[10][2] = (0, 155, 0)

        testboard[11][3] = (0, 0, 155)
        testboard[11][4] = (0, 0, 155)
        testboard[10][4] = (0, 0, 155)

        puyoinst.board = puyoinst.getstartboard()
        puyoinst.board[10][0] = (155, 0, 0)
        puyoinst.board[10][1] = (155, 0, 0)

        puyoinst.board[11][2] = (0, 155, 0)
        puyoinst.board[10][2] = (0, 155, 0)

        puyoinst.board[11][3] = (0, 0, 155)
        puyoinst.board[10][4] = (0, 0, 155)
        puyoinst.board[9][4] = (0, 0, 155)

        puyoinst.move_down_floating()

        assert testboard == puyoinst.board

    def test_checklocalrecur(self):
        puyoinst.board = puyoinst.getstartboard()
        puyoinst.board[10][0] = (155, 0, 0)
        puyoinst.board[10][1] = (155, 0, 0)

        puyoinst.board[11][0] = (0, 155, 0)
        puyoinst.board[11][1] = (0, 155, 0)
        puyoinst.board[11][2] = (0, 155, 0)
        puyoinst.board[10][2] = (0, 155, 0)

        puyoinst.board[11][3] = (0, 0, 155)
        puyoinst.board[10][3] = (0, 0, 155)
        puyoinst.board[11][4] = (0, 0, 155)

        assert [(11, 1), (11, 0), (11, 2), (10, 2)] == puyoinst.checklocalrecur(11,0,(0, 155, 0))

        assert [] == (puyoinst.checklocalrecur(10,0,(155, 0, 0)))


        

       

