from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from PuyoPuyo.puyo_puyo import puyo_puyo
from threading import Thread
import pygame
import copy
import numpy as np
import tensorflow as tf
import time
import os
from PuyoPuyo.aiNNPuyoPuyo import PuyoPuyoAgent
import random
import PuyoPuyo.PuyoPuyoSimulation as PuyoPuyoSimulation
configuration = tf.compat.v1.ConfigProto()
configuration.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=configuration)




def doMoves(movementList,movementQueue):
    for item in movementList:
        movementQueue.put(item)

def bestMoves(board,block,movementsList,simulatedPuyoPuyo,simulationMovements):
    #Simulates each possible future board state and calculate a score for each
    movementTracker = 0
    boardScores = {}
    simulatedList = {}
    for movements in movementsList:
        simulatedBoardScores = simulateBoard(board,block,movements,simulatedPuyoPuyo,simulationMovements)
        boardScores[movementTracker] = simulatedBoardScores
        movementTracker+=1
    return boardScores

def simulateBoard(board,block,movements,simulatedPuyoPuyo,aiSimulationMovements):
    simulatedPuyoPuyo.board= copy.deepcopy(board)
    simulatedPuyoPuyo.currentpuyoblock = copy.deepcopy(block)
    for move in movements:
        numberOfLinesCleared=aiSimulationMovements[move]()
    return boardScoring(simulatedPuyoPuyo.board,numberOfLinesCleared)

def boardScoring(board,numberOfLinesCleared):
    puyosNearEachOtherSameColour, puyoStacks = puyosNearEachOther(board)
    sumHeight, maxHeight = heights(board)
    return [sumHeight,puyosNearEachOtherSameColour, puyoStacks,numberOfLinesCleared,maxHeight]

def heights(board):
    sumHeight=0
    maxHeight=0
    for column in zip(*board):
        i=0
        while i<len(board) and column[i]==".":
            i+=1
        sumHeight+=len(board)-i
        if maxHeight==0 or maxHeight<len(board)-i:
            maxHeight=len(board)-i
    return sumHeight,maxHeight

def puyosNearEachOther(board):
    #This function checks how many of the same coloured puyos are touching each other and also how many are in a 3 high column
    puyosNearEachOther=0
    puyoStack=0
    for height in range(len(board)):
        for index in range(len(board[height])):
            if index!= 0 and board[height][index]!="." and board[height][index]==board[height][index-1]:
                puyosNearEachOther+=1
            elif index!=len(board[height])-1 and board[height][index]!="." and board[height][index]==board[height][index+1]:
                puyosNearEachOther+=1
            elif height!=len(board)-1 and board[height][index]!="." and board[height][index]==board[height+1][index]:
                puyosNearEachOther+=1
            elif height != 0 and board[height][index] != "." and board[height][index] == board[height - 1][index]:
                puyosNearEachOther += 1
            if board[height][index]!="." and height!=len(board)-1 and height!=0 and board[height+1][index]==board[height][index] and board[height-1][index]==board[height][index]:
                puyoStack+=1
    return puyosNearEachOther,puyoStack

def playPuyo(currentBoardQueue,currentPieceQueue,gameOver,movementQueue,loadingScreen):
    movementsList = [['drop'], ['left', 'drop'], ['left', 'left', 'drop'], ['right', 'drop'],
                     ['right', 'right', 'drop'], ['right', 'right', 'right', 'drop'],
                     ['right', 'right', 'right', 'right', 'drop'], ['rotate', 'drop'], ['rotate', 'left', 'drop'],
                     ['rotate', 'left', 'left', 'drop'], ['rotate', 'right', 'drop'],
                     ['rotate', 'right', 'right', 'drop'], ['rotate', 'right', 'right', 'right', 'drop'],
                     ['rotate', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'drop'],
                     ['rotate', 'rotate', 'left', 'drop'], ['rotate', 'rotate', 'left', 'left', 'drop'],
                     ['rotate', 'rotate', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'drop'],
                     ['rotate', 'rotate', 'right', 'right', 'right', 'drop'],
                     ['rotate', 'rotate', 'right', 'right', 'right', 'right', 'drop'],
                     ['rotate', 'rotate', 'rotate', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'drop'],
                     ['rotate', 'rotate', 'rotate', 'left', 'left', 'drop'],
                     ['rotate', 'rotate', 'rotate', 'right', 'drop'],
                     ['rotate', 'rotate', 'rotate', 'right', 'right', 'drop'],
                     ['rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'drop'],
                     ['rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'drop']]
    simulatedPuyoPuyo = PuyoPuyoSimulation.puyo_puyo()
    aiSimulationMovements = {
        'drop': simulatedPuyoPuyo.drop,
        'left': simulatedPuyoPuyo.moveleftAi,
        'right': simulatedPuyoPuyo.moverightAi,
        'rotate': simulatedPuyoPuyo.rotate,
    }
    puyoAgentTest = PuyoPuyoAgent(0,0)
    puyoAgentTest.model = tf.keras.models.load_model(os.path.dirname(os.path.abspath(__file__))+"\\NeuralNetworkPuyoPuyoModels\\episode1000.h5")
    #We do a predict here to load the predict module of the Neural Network so we don't have to load it later
    puyoAgentTest.model.predict(np.reshape([0,0,0,0,0],[1,5]))
    #Signal to the loading screen that the loading is done through another queue system
    loadingScreen.get()
    while not gameOver.empty():
        if not currentBoardQueue.empty() and not currentPieceQueue.empty():
            # Get information about the game from the queues
            tempBoard=currentBoardQueue.get()
            tempPiece=currentPieceQueue.get()
            # Simulate all possible end states and come back with a score for each possible board state
            boardScores = bestMoves(tempBoard,tempPiece,movementsList,simulatedPuyoPuyo,aiSimulationMovements)
            # Ask which board state the Ai should choose
            bestMoveIndex,bestScore = puyoAgentTest.bestMoves(boardScores.values())
            # Do the corresponding sequence of moves to get to the Ai's chosen board
            doMoves(movementsList[bestMoveIndex],movementQueue)




