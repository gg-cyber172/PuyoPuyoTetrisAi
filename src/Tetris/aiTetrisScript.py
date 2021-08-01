from multiprocessing import Process
from threading import Thread
from copy import deepcopy
import tensorflow as tf
import pygame
import time
import Tetris.Tetris as Tetris
import Tetris.boardSimulation as boardSimulation
import copy
import itertools
import queue
import os
import numpy as np
import os
from Tetris.aiNNTetris import TetrisAgent

def numberOfHoles(board):
    holes = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if i!=0 and board[i][j]==0 and board[i-1][j]!=0:
                holes+=1
    return holes

def bumpinessAndTotalHeight(board):
    columnHeights=[]
    bumpiness=0
    totalHeight=0
    for column in zip(*board):
        i = 0
        while i < len(board) and column[i] == 0:
            i += 1
        totalHeight+=len(board)-i
        columnHeights.append(len(board)-i)
    for i in range(len(columnHeights)-1):
        bumpiness+=(abs(columnHeights[i]-columnHeights[i+1]))
    return [totalHeight,bumpiness]

def penalityCalc(board,linesCleared):
    temp = bumpinessAndTotalHeight(board)
    return [numberOfHoles(board),temp[0], temp[1],linesCleared]



def simulateBoard(tempBoard,tempBlock,tempReserved,listItem,simulation,keysDictAI):
    simulation.currentBlock=copy.deepcopy(tempBlock)
    simulation.field=copy.deepcopy(tempBoard)
    simulation.reserved = copy.deepcopy(tempReserved)
    for item in listItem:
        if item!="":
            linesCleared=keysDictAI[item]()
    return penalityCalc(simulation.field,linesCleared)

def bestMoves(tempBoard,tempBlock,tempReserved,movementsList,simulation,keysDictAI):
    #This simulates each possible future board state and returns a score for each
    movementTracker = 0
    boardScores = {}
    possibleMovements = {}
    simulatedList = {}
    for movements in movementsList:
        simulatedBoardScores = simulateBoard(tempBoard,tempBlock,tempReserved,movements,simulation,keysDictAI)
        boardScores[movementTracker] = simulatedBoardScores
        movementTracker += 1

    return boardScores

def doMoves(movementsList,movementQueue):
    #Signal to the game to do this sequence of moves
    for movement in movementsList:
        movementQueue.put(movement)




def playTetris(queueOfBoards,queueOfCurrentPiece,queueOfReserve,gameOver,movementQueue,loadingScreen):
    movementsList=[['drop'], ['left', 'drop'], ['left', 'left', 'drop'], ['left', 'left', 'left', 'drop'], ['left', 'left', 'left', 'left', 'drop'], ['left', 'left', 'left', 'left', 'left', 'drop'], ['right', 'drop'], ['right', 'right', 'drop'], ['right', 'right', 'right', 'drop'], ['right', 'right', 'right', 'right', 'drop'], ['right', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'drop'], ['rotate', 'left', 'drop'], ['rotate', 'left', 'left', 'drop'], ['rotate', 'left', 'left', 'left', 'drop'], ['rotate', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'left', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'right', 'drop'], ['rotate', 'right', 'right', 'drop'], ['rotate', 'right', 'right', 'right', 'drop'], ['rotate', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'right', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'drop'], ['rotate', 'rotate', 'left', 'drop'], ['rotate', 'rotate', 'left', 'left', 'drop'], ['rotate', 'rotate', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'left', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'drop'],['reserve', 'left', 'drop'],['reserve', 'left', 'left', 'drop'],['reserve', 'left', 'left', 'left', 'drop'],['reserve', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'left', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'right', 'drop'],['reserve', 'right', 'right', 'drop'],['reserve', 'right', 'right', 'right', 'drop'],['reserve', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'right', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'drop'],['reserve', 'rotate', 'left', 'drop'],['reserve', 'rotate', 'left', 'left', 'drop'],['reserve', 'rotate', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'left', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'right', 'drop'],['reserve', 'rotate', 'right', 'right', 'drop'],['reserve', 'rotate', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'right', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'drop'],['reserve', 'rotate', 'rotate', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'left', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'right', 'drop']]
    simulation = boardSimulation.TetrisSim(None, None, None)
    keysDictAI = {
        "rotate": simulation.Rotates,
        "down": simulation.Down,
        "right": simulation.Right,
        "left": simulation.Left,
        "drop": simulation.Drop,
        "reserve": simulation.Reserve
    }
    tetrisAgent=TetrisAgent(0,0)
    tetrisAgent.model= tf.keras.models.load_model(os.path.dirname(os.path.abspath(__file__))+"\\NeuralNetworkModelsTetris\\episode4300.h5")
    #We do a predict here to load the predict module of the Neural Network so we don't have to load it later
    tetrisAgent.model.predict(np.reshape([0,0,0,0],[1,4]))
    #Signal to the loading screen that the loading is done through another queue system
    loadingScreen.get()
    while not gameOver.empty():
        if not queueOfBoards.empty() and not queueOfCurrentPiece.empty():
            #Get information about the game from the queues
            tempBoard = queueOfBoards.get()
            tempPiece = queueOfCurrentPiece.get()
            tempReserve = queueOfReserve.get()
            #This only happens when it's the very first move of the game so this will always be the first command
            if tempReserve==None:
                movementQueue.put("reserve")
            else:
                #Simulate all possible end states and come back with a score for each possible board state
                boardScores = bestMoves(tempBoard, tempPiece,tempReserve, movementsList, simulation, keysDictAI)
                #Ask which board state the Ai should choose
                bestMoveIndex, bestScore = tetrisAgent.bestMoves(boardScores.values())
                #Do the corresponding sequence of moves to get to the Ai's chosen board
                doMoves(movementsList[bestMoveIndex], movementQueue)
