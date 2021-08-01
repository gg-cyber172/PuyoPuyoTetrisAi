import pytest
import sys
sys.path.append("..")
from PuyoPuyo.aiPuyoPuyoScript import puyosNearEachOther #import puyosNearEachOther
from PuyoPuyo.aiPuyoPuyoScript import heights
#from src.PuyoPuyo.puyo_puyo import puyo_puyo

class TestPuyoPuyoAi():
    def test_puyosNearEachOther(self):
        tempField=[["."] * 6 for i in range(12)]
        tempField[11][0] = (155,0,0)
        tempField[11][1] = (155, 0, 0)
        tempField[11][2] = (155, 0, 0)
        puyosneareachother,puyostacks = puyosNearEachOther(tempField)
        assert(puyosneareachother==3)
        assert(puyostacks==0)

        tempField[11][5] = (155, 155, 0)
        tempField[10][5] = (155,155,0)
        tempField[9][5] = (155,155,0)
        puyosneareachother,puyostacks = puyosNearEachOther(tempField)
        assert(puyosneareachother==6)
        assert(puyostacks==1)

    def test_heights(self):
        tempField = [["."] * 6 for i in range(12)]
        tempField[11][0] = (155, 0, 0)
        tempField[11][1] = (155, 0, 0)
        tempField[11][2] = (155, 0, 0)
        sumHeight,maxHeight = heights(tempField)
        assert(sumHeight==3)
        assert(maxHeight==1)
        tempField[11][5] = (155, 155, 0)
        tempField[10][5] = (155,155,0)
        tempField[9][5] = (155,155,0)
        tempField[11][3]= (155,155,0)
        sumHeight, maxHeight = heights(tempField)
        assert(sumHeight==7)
        assert(maxHeight==3)