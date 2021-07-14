from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from puyo_puyoTrainingVersion import puyo_puyo
from threading import Thread
from copy import deepcopy
import pygame
import numpy as np
import tensorflow as tf
import time
import aiNNPuyoPuyoTrainingVersion
import PuyoPuyoSimulationTrainingVersion
import queue

configuration = tf.compat.v1.ConfigProto()
configuration.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=configuration)


def runPuyoPuyo():
    puyoInst.rungame()

    running.pop()


def doMoves(movementList,movementQueue):
    for item in movementList:
        try:
            movementQueue.put(item)
        except TypeError:
            print(item)


def bestMoves(board,block,nextPiece):
    movementTracker = 0
    scores = {}
    gameOverList = []
    for movements in movementsList:
        simulatedBoardScores, gameOver = simulateBoard(board,block,nextPiece,movements)
        scores[movementTracker] = simulatedBoardScores
        gameOverList.append(gameOver)
        movementTracker+=1
    return scores,gameOverList

def simulateBoard(board,block,nextPiece,movements):
    simulatedPuyoPuyo.board= deepcopy(board)
    simulatedPuyoPuyo.currentpuyoblock = deepcopy(block)
    simulatedPuyoPuyo.nextpuyoblock = deepcopy(nextPiece)
    for move in movements:
        numberOfLinesCleared=aiSimulationMovements[move]()
    simulatedPuyoPuyo.currentpuyoblock = simulatedPuyoPuyo.getnewpuyo()
    return boardScoring(simulatedPuyoPuyo.board,numberOfLinesCleared),not simulatedPuyoPuyo.isvalidmovement("down")

def boardScoring(board,numberOfLinesCleared):
    puyosNearEachOtherSameColour, puyoStacks = puyosNearEachOther(board)
    sumHeight,maxHeight = heights(board)
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





numberOfGames=10000
trainOnEpisode = 1
epochs = 3
batchSize = 32
renderOnEpisodeCount=50
epsilon =1
memoryBufferSize=10000
logging = True


movementsList=[['drop'], ['left', 'drop'], ['left', 'left', 'drop'],  ['right', 'drop'], ['right', 'right', 'drop'], ['right', 'right', 'right', 'drop'], ['right', 'right', 'right', 'right', 'drop'], ['rotate', 'drop'], ['rotate', 'left', 'drop'], ['rotate', 'left', 'left', 'drop'],  ['rotate', 'right', 'drop'], ['rotate', 'right', 'right', 'drop'], ['rotate', 'right', 'right', 'right', 'drop'], ['rotate', 'right', 'right', 'right', 'right', 'drop'],  ['rotate', 'rotate', 'drop'], ['rotate', 'rotate', 'left', 'drop'], ['rotate', 'rotate', 'left', 'left', 'drop'],  ['rotate', 'rotate', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'right', 'right', 'drop'],  ['rotate', 'rotate', 'rotate', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'left', 'drop'],   ['rotate', 'rotate', 'rotate', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'drop']]
currentBoardQueue,currentPieceQueue,nextPieceQueue,movementQueue,resultQueue, =[],[],[],[],[]
puyoPuyoAgent=aiNNPuyoPuyoTrainingVersion.PuyoPuyoAgent(memoryBufferSize, epsilon)
simulatedPuyoPuyo = PuyoPuyoSimulationTrainingVersion.puyo_puyo()
aiSimulationMovements = {
    'drop': simulatedPuyoPuyo.drop,
    'left': simulatedPuyoPuyo.moveleftAi,
    'right': simulatedPuyoPuyo.moverightAi,
    'rotate': simulatedPuyoPuyo.rotate,
}
#puyoPuyoAgent.model.load_weights("NeuralNetworkPuyoPuyoModelsWIP\episode2600.h5")

pygame.init()
for episode in range(numberOfGames):
    currentBoardQueue = queue.Queue()
    currentPieceQueue= queue.Queue()
    nextPieceQueue= queue.Queue()
    movementQueue= queue.Queue()
    resultQueue= queue.Queue()

    print("episode:",episode)
    screen = pygame.display.set_mode((1920, 1080))
    puyoInst = puyo_puyo(screen,renderOnEpisodeCount,episode,currentBoardQueue,currentPieceQueue,nextPieceQueue,movementQueue,resultQueue)

    aiMovements = {
        'drop': puyoInst.drop,
        'left': puyoInst.moveleftAi,
        'right': puyoInst.moverightAi,
        'rotate': puyoInst.rotate,
    }
    running=[1]

    t1=Thread(target=runPuyoPuyo)
    t1.start()

    overAllscore=0
    currentScore=(0,0)#currentScore,Lines Cleared

    counter=0
    while len(running):


        if not currentBoardQueue.empty() and not currentPieceQueue.empty() and not nextPieceQueue.empty():
            tempBoard = currentBoardQueue.get()
            tempBlock = currentPieceQueue.get()
            tempQueue = nextPieceQueue.get()

            currentBoardScore = boardScoring(tempBoard,currentScore[1])
            scores, gameOver = bestMoves(tempBoard, tempBlock,tempQueue)
            bestMoveIndex, bestScore = puyoPuyoAgent.bestMoves(scores.values())
            doMoves(movementsList[bestMoveIndex],movementQueue)

            while resultQueue.empty() and len(running):
                pass

            newScore= resultQueue.get()
            overAllScoreChange = 1+(newScore[1]*2)
            currentScore=newScore
            print(episode, ":", counter,newScore[0])
            if gameOver[bestMoveIndex]:
                overAllscore-=10
            #if bestScore[4]>=8:
            #    overAllscore-=1+(bestScore[4]-8)

            puyoPuyoAgent.addToMovesMemory(currentBoardScore, bestScore, overAllscore, gameOver[bestMoveIndex])
            counter+=1


    if logging:
        f = open("logs\\trainingLogMovesDone05-05-21.txt","a")
        f.write(str(counter)+"\n")
        f.close()
        f = open("logs\\trainingLogScores05-05-21.txt","a")
        f.write(str(newScore[0])+"\n")
        f.close()
    if episode % trainOnEpisode == 0:
        puyoPuyoAgent.train(batchSize,epochs)
    if episode%20==0 and episode>300:
        string = "NeuralNetworkPuyoPuyoModelsWIP\episode"+str(episode)+".h5"
        puyoPuyoAgent.model.save(string)
    time.sleep(0.5)

puyoPuyoAgent.model.save("NeuralNetworkPuyoPuyoModelsWIP\Final.h5")



