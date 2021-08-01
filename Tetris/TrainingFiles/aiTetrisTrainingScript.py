from multiprocessing import Process
from threading import Thread
from copy import deepcopy
import tensorflow as tf
import pygame
import time
import TetrisTrainingVersion
import boardSimulationTrainingVersion
import random
import itertools
import queue
from aiNNTetrisTrainingVersion import TetrisAgent

#physical_devices = tf.config.list_physical_devices('GPU')
#tf.config.experimental.set_memory_growth(physical_devices[0], True)
commands = ["rotate","left","right","down"]
configuration = tf.compat.v1.ConfigProto()
configuration.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=configuration)

def tetrisScript(currentBoardQueue,currentPieceQueue,currentReservedQueue,nextPieceQueue,movementsQueue,resultsQueue,toRenderQueue,gameOverQueue):
    render = toRenderQueue.get()
    if render:
        pygame.init()
        screen = pygame.display.set_mode((0,0),pygame.RESIZABLE)
        pygame.display.set_caption("Tetris Game")
    clock = pygame.time.Clock()
    count =0

    while not gameOverQueue.empty():
        if tetrisInst.currentBlock is None and not tetrisInst.gameOver:
            tetrisInst.newBlock()
            #New board state, put the new information onto the queue system
            if not tetrisInst.gameOver:
                currentPieceQueue.put(tetrisInst.currentBlock)
                nextPieceQueue.put(tetrisInst.nextShapes)
                currentBoardQueue.put(tetrisInst.field)
                currentReservedQueue.put(tetrisInst.reserved)
        if render:
            screen.fill((255, 255, 255))
        count+=1
        if not movementsQueue.empty():
            while not movementsQueue.empty():
                keysDict[movementsQueue.get()]()
        elif ( count>=tetrisInst.speedCheck() or tetrisInst.down) and not tetrisInst.gameOver:
            count=0
            result=tetrisInst.goDown()
        if tetrisInst.gameOver:
            if render:
                gameOverText = pygame.font.SysFont("Calibri" ,100, True, False).render("Game Over", True,(0,0,0))
                screen.blit(gameOverText,[(1980/2)-250,30])
            gameOverQueue.get()
        if render:
            text = pygame.font.SysFont("Calibri" ,25, True, False).render("Score: "+str(tetrisInst.score), True,(0,0,0))
            next = pygame.font.SysFont("Calibri" ,25, True, False).render("Next: ", True,(0,0,0))
            levelText = pygame.font.SysFont("Calibri" ,25, True, False).render("Level: "+str(tetrisInst.level), True,(0,0,0))
            linesText = pygame.font.SysFont("Calibri" ,25, True, False).render("Lines: "+str(tetrisInst.linesCleared), True,(0,0,0))
            screen.blit(text,[0,0])
            screen.blit(next,[(1920/2)+(10*(36/2)),(1080/2)-(25*(35/2))])
            screen.blit(levelText,[0,50])
            screen.blit(linesText,[0,100])
        if render:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or ( event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    gameOverQueue.get()
                if (event.type==pygame.KEYDOWN and event.key in keysDict.keys()) and not tetrisInst.gameOver:
                    keysDict[event.key]()

                if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    tetrisInst.down=False
            tetrisInst.drawQueue(screen)#drawQueue.append(deepcopy.copy(tetrisInst.reserved))
            tetrisInst.drawField(screen)
            tetrisInst.drawReserve(screen)
            if tetrisInst.currentBlock is not None:
                try:
                    tetrisInst.drawBlock(screen)
                except:
                    print("error in drawing")
            pygame.display.flip()
        clock.tick(60)
        if not tetrisInst.down:
            time.sleep(1.0/60)
    if render:
        pygame.quit()

def numberOfHoles(board):
    #Here we calculate how many holes there are in a board
    #A hole is defined by a blank space with a filled space directly above it
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
    #We calculate the bumpiness(difference in height of adjacent columns) and the sum height of all the columns
    for column in zip(*board):#the zip(*board) allows us to go by column by column instead of row by row
        i = 0
        while i < len(board) and column[i] == 0:
            i += 1
        totalHeight+=len(board)-i
        columnHeights.append(len(board)-i)
    for i in range(len(columnHeights)-1):
        bumpiness+=(abs(columnHeights[i]-columnHeights[i+1]))
    return [totalHeight,bumpiness]

def penalityCalc(board,linesCleared):
    # Here we calculate how good this particular end result is
    temp = bumpinessAndTotalHeight(board)
    return [numberOfHoles(board),temp[0], temp[1],linesCleared]



def simulateBoard(simulation,tempBlock,tempBoard,tempReserved,listItem,tempNextBlocks,score,level):
    #Do a deepcopy to ensure we always start off with the same objects
    simulation.currentBlock=deepcopy(tempBlock)
    simulation.field=deepcopy(tempBoard)
    simulation.reserved = deepcopy(tempReserved)
    simulation.nextShapes = deepcopy(tempNextBlocks)
    simulation.score=score
    simulation.level = level
    for item in listItem:
        if item!="":
            #The last command will always be a "drop" which returns how many lines were cleared and if it caused the Ai to lose
            gameOverAndLinesCleared = keysDictAI[item]()

    return penalityCalc(simulation.field,gameOverAndLinesCleared[0]), gameOverAndLinesCleared[1], simulation.score

def doMoves(movements,movementsQueue):
    #This function here signals to the game what inputs to do that the Ai decided it should do
    for move in movements:
        movementsQueue.put(move)

#movementsList=[['drop'], ['left', 'drop'], ['left', 'left', 'drop'], ['left', 'left', 'left', 'drop'], ['left', 'left', 'left', 'left', 'drop'], ['left', 'left', 'left', 'left', 'left', 'drop'], ['right', 'drop'], ['right', 'right', 'drop'], ['right', 'right', 'right', 'drop'], ['right', 'right', 'right', 'right', 'drop'], ['right', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'drop'], ['rotate', 'left', 'drop'], ['rotate', 'left', 'left', 'drop'], ['rotate', 'left', 'left', 'left', 'drop'], ['rotate', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'left', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'right', 'drop'], ['rotate', 'right', 'right', 'drop'], ['rotate', 'right', 'right', 'right', 'drop'], ['rotate', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'right', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'drop'], ['rotate', 'rotate', 'left', 'drop'], ['rotate', 'rotate', 'left', 'left', 'drop'], ['rotate', 'rotate', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'left', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'right', 'drop']]
movementsList=[['drop'], ['left', 'drop'], ['left', 'left', 'drop'], ['left', 'left', 'left', 'drop'], ['left', 'left', 'left', 'left', 'drop'], ['left', 'left', 'left', 'left', 'left', 'drop'], ['right', 'drop'], ['right', 'right', 'drop'], ['right', 'right', 'right', 'drop'], ['right', 'right', 'right', 'right', 'drop'], ['right', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'drop'], ['rotate', 'left', 'drop'], ['rotate', 'left', 'left', 'drop'], ['rotate', 'left', 'left', 'left', 'drop'], ['rotate', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'left', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'right', 'drop'], ['rotate', 'right', 'right', 'drop'], ['rotate', 'right', 'right', 'right', 'drop'], ['rotate', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'right', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'drop'], ['rotate', 'rotate', 'left', 'drop'], ['rotate', 'rotate', 'left', 'left', 'drop'], ['rotate', 'rotate', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'left', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'right', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'left', 'left', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'drop'], ['rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'drop'],['reserve', 'left', 'drop'],['reserve', 'left', 'left', 'drop'],['reserve', 'left', 'left', 'left', 'drop'],['reserve', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'left', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'right', 'drop'],['reserve', 'right', 'right', 'drop'],['reserve', 'right', 'right', 'right', 'drop'],['reserve', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'right', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'drop'],['reserve', 'rotate', 'left', 'drop'],['reserve', 'rotate', 'left', 'left', 'drop'],['reserve', 'rotate', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'left', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'right', 'drop'],['reserve', 'rotate', 'right', 'right', 'drop'],['reserve', 'rotate', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'right', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'drop'],['reserve', 'rotate', 'rotate', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'left', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'left', 'left', 'left', 'left', 'left', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'drop'],['reserve', 'rotate', 'rotate', 'rotate', 'right', 'right', 'right', 'right', 'right', 'drop']]
simulation = boardSimulationTrainingVersion.TetrisSim(None, None, None)
keysDictAI = {
            "rotate":simulation.Rotates,
            "down":simulation.Down,
            "right":simulation.Right,
            "left":simulation.Left,
            "drop":simulation.Drop,
            "reserve":simulation.Reserve
}

numberOfGames=2000
trainOnEpisode = 1
epochs = 3
batchSize = 32
renderOnEpisodeCount=1500
epsilon=1
memoryBufferSize=10000
logging = True
tetrisAgent = TetrisAgent(memoryBufferSize,epsilon)
#tetrisAgent.model.load_weights("NeuralNetworkTetrisModelsWIP\\episode200.h5")

for episode in range(0,numberOfGames):
    currentBoardQueue = queue.Queue()
    currentPieceQueue = queue.Queue()
    currentReservedQueue = queue.Queue()
    nextPieceQueue = queue.Queue()
    movementsQueue = queue.Queue()
    resultsQueue = queue.Queue()
    toRenderQueue = queue.Queue()
    gameOverQueue = queue.Queue()

    gameOverQueue.put("1")

    counter=0
    score = 0
    oldScore = 0
    tetrisInst = TetrisTrainingVersion.Tetris(resultsQueue)
    currentBoard = []
    keysDict = {
        pygame.K_UP: tetrisInst.Rotate,
        pygame.K_DOWN: tetrisInst.pressDown,
        pygame.K_RIGHT: tetrisInst.goRight,
        pygame.K_LEFT: tetrisInst.goLeft,
        pygame.K_SPACE: tetrisInst.pressDown,
        pygame.K_LSHIFT: tetrisInst.useReserved,
        "rotate": tetrisInst.Rotate,
        "down": tetrisInst.pressDown,
        "right": tetrisInst.goRight,
        "left": tetrisInst.goLeft,
        "drop": tetrisInst.goDrop,
        "reserve": tetrisInst.useReserved
    }

    currentBoardScores=[0,0,0,0]
    currentScore = 0
    currentLevel=0
    linesCleared=0
    overAllScore=0

    temp = episode%renderOnEpisodeCount==0
    toRenderQueue.put(temp)
    t = Thread(target=tetrisScript, args=(currentBoardQueue,currentPieceQueue,currentReservedQueue,nextPieceQueue,movementsQueue,resultsQueue,toRenderQueue,gameOverQueue,))
    t.start()
    print("episode:",episode)
    while not gameOverQueue.empty():
        if not currentBoardQueue.empty() and not currentPieceQueue.empty() and not nextPieceQueue.empty():
            #Get all the information about the board from the queue system
            tempBoard= currentBoardQueue.get()
            tempBlock = currentPieceQueue.get()
            tempNextBlocks = nextPieceQueue.get()
            tempReserved = currentReservedQueue.get()

            currentBoardScores = penalityCalc(tempBoard, linesCleared)

            counter+=1

            simulatedGameOverList=[]
            scores={}
            if tempReserved==None:
                movementsQueue.put("reserve")
            else:
                movementTracker=0
                #print("got to the for loop")
                for listItem in movementsList:
                    tempSimulatedBoard, gameOver, score = simulateBoard(simulation,tempBlock,tempBoard,tempReserved,listItem,tempNextBlocks,currentScore, currentLevel)
                    simulatedGameOverList.append((gameOver,score))
                    scores[movementTracker] = tempSimulatedBoard
                    movementTracker+=1

                bestMoveIndex, bestScore = tetrisAgent.bestMoves(scores.values())
                doMoves(movementsList[bestMoveIndex],movementsQueue)
                while resultsQueue.empty() and not gameOverQueue.empty():
                    pass

                #It gathers the results of it's input through another queue system
                tempNewResults = resultsQueue.get()

                linesCleared = tempNewResults[0]
                #Here it calculates the reward it wil receive from this result
                #It receives 1 point for placing an object, and a multiplicative for how many lines/puyos it cleared
                #This is to incentivise it clear more lines/puyos in one go
                overAllScore = 1 + linesCleared*2
                #If this resulted in the Ai losing the game then punish it to avoid these moves later on
                if simulatedGameOverList[bestMoveIndex][0]:
                    overAllScore-= 5
                #print(episode, ": ",counter,overAllScore,linesCleared)
                #And once this is done, add all of this to its memory bank
                tetrisAgent.addToMovesMemory(currentBoardScores,bestScore,overAllScore,simulatedGameOverList[bestMoveIndex][0])

        if(temp):
            time.sleep(1)
    if logging:
        f = open("logs\\trainingLogMovesDone05-05-21.txt", "a")
        f.write(str(counter) + "\n")
        f.close()
        f = open("logs\\trainingLogScores05-05-21.txt", "a")
        f.write(str(tempNewResults[1]) + "\n")
        f.close()

    if episode % trainOnEpisode == 0:
        tetrisAgent.train(batchSize,epochs)
    if episode % 100==0:
        string = "NeuralNetworkTetrisModelsWIP\episode"+str(episode)+".h5"
        tetrisAgent.model.save(string)

tetrisAgent.model.save("NeuralNetworkTetrisModelsWIP\Final.h5")
