import pytest
import sys
sys.path.append("..")
from Tetris.aiTetrisScript import numberOfHoles #import puyosNearEachOther
from Tetris.aiTetrisScript import bumpinessAndTotalHeight

class TestTetrisAI():
    def test_holes(self):
        tempField = [[0] * 10 for i in range(24)]
        tempField[23][0] = (155, 0, 0)
        tempField[23][1] = (155, 0, 0)
        tempField[23][2] = (155, 0, 0)
        tempField[22][2] = (155, 0, 0)
        tempField[22][0] = (155, 0, 0)
        tempField[22][3] = (155, 0, 0)
        tempField[21][0] = (155, 0, 0)
        tempField[21][1] = (155, 0, 0)
        tempField[21][2] = (155, 0, 0)
        holes = numberOfHoles(tempField)
        assert(holes == 2)


        tempField[23][4] = (155, 155, 0)
        tempField[23][6] = (155, 155, 0)
        tempField[23][8] = (155, 155, 0)
        tempField[22][4] = (155, 155, 0)
        tempField[22][5] = (155, 155, 0)
        tempField[22][6] = (155, 155, 0)
        tempField[22][7] = (155, 155, 0)
        tempField[22][8] = (155, 155, 0)
        tempField[22][9] = (155, 155, 0)
        holes = numberOfHoles(tempField)
        assert(holes == 5 )

    def test_heightsAndBumpiness(self):
        tempField = [[0] * 10 for i in range(24)]

        tempField[23][0] = (155, 0, 0)
        tempField[23][1] = (155, 0, 0)
        tempField[23][2] = (155, 0, 0)
        tempField[23][4] = (155, 0, 0)
        tempField[23][5] = (155, 0, 0)
        tempField[23][6] = (155, 0, 0)
        tempField[23][7] = (155, 0, 0)
        tempField[23][8] = (155, 0, 0)

        tempField[22][0] = (155, 0, 0)
        tempField[22][1] = (155, 0, 0)
        tempField[22][2] = (155, 0, 0)
        tempField[22][5] = (155, 0, 0)
        tempField[22][6] = (155, 0, 0)
        tempField[22][7] = (155, 0, 0)
        tempField[22][8] = (155, 0, 0)

        tempField[21][0] = (155, 0, 0)
        tempField[21][6] = (155, 0, 0)
        tempField[21][7] = (155, 0, 0)
        tempField[21][8] = (155, 0, 0)

        tempField[20][7] = (155, 0, 0)
        tempField[20][8] = (155, 0, 0)

        tempField[19][8] = (155, 0, 0)
        totalHeightAndBumpiness = bumpinessAndTotalHeight(tempField)
        assert (totalHeightAndBumpiness[0] == 22)
        assert (totalHeightAndBumpiness[1] == 13)

        # [0,0,0,0,0,0,0,0,x,x] 8
        # [x,0,0,0,0,0,0,x,x,x] 7,8
        # [x,0,0,0,0,0,x,x,x,x] 0,6,7,8
        # [x,x,x,0,0,x,x,x,x,x] 0,1,2,5,6,7,8
        # [x,x,x,0,x,x,x,x,x,x] 0,1,2,4,5,6,7,8,9 Going for this shape

        tempField[23][9] = (155, 155, 0)

        tempField[22][9] = (155, 155, 0)

        tempField[21][9] = (155, 155, 0)

        tempField[20][0] = (155, 155, 0)
        tempField[20][9] = (155, 155, 0)

        tempField[19][9] = (155, 155, 0)
        totalHeightAndBumpiness = bumpinessAndTotalHeight(tempField)
        assert (totalHeightAndBumpiness[0] == 28)
        assert (totalHeightAndBumpiness[1] == 9)

