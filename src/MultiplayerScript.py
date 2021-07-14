import pygame
import time
import sys
import math
import Tetris.aiTetrisScript
import PuyoPuyo.aiPuyoPuyoScript
import tensorflow as tf
from queue import Queue
from threading import Thread
from PuyoPuyo import LaunchPuyoScript
from Tetris import LaunchTetrisScript
from Tetris.aiNNTetris import TetrisAgent
from PuyoPuyo.aiNNPuyoPuyo import PuyoPuyoAgent




def main(screen,Player1Game,Player2Game, AIFlagP1=False, AIFlagP2=False):
    print("Playing multiplayer with " + Player1Game + " and " + Player2Game)


    global nusiancequeue1,nusiancequeue2,nl2, nl1
    nusiancequeue1 =[]
    nusiancequeue2 =[]
    nl2, nl1 = 0,0
    if AIFlagP1 or AIFlagP2:
        playGameAi(screen,Player1Game,Player2Game, AIFlagP1, AIFlagP2)
    else:
        playGameNoAi(screen,Player1Game,Player2Game)

def playGameNoAi(screen,Player1Game,Player2Game):
    global nusiancequeue1,nusiancequeue2,nl2, nl1
    P1OK = True
    P2OK = True
    nus1 = 0
    nus2 = 0
    if Player1Game == "P1P" and Player2Game == "P2P":
        p1 = LaunchPuyoScript.main(screen, "multi")
        p2 = LaunchPuyoScript.main(screen, "multi")
        p1.init_game_values()
        p2.init_game_values()
        keysDict = {
            pygame.K_UP: p2.rotate,
            pygame.K_DOWN: p2.movedown,
            pygame.K_RIGHT: p2.moveright,
            pygame.K_LEFT: p2.moveleft,
            pygame.K_RCTRL: p2.drop,

            pygame.K_w: p1.rotate,
            pygame.K_s: p1.movedown,
            pygame.K_d: p1.moveright,
            pygame.K_a: p1.moveleft,
            pygame.K_LCTRL: p1.drop,
        }

        nus1time = 0
        nus2time = 0
        while P1OK and P2OK:
            P1OK, nus1 = puyo_puyoloop(p1, "P1")
            P2OK, nus2 = puyo_puyoloop(p2, "P2")

            for event in pygame.event.get():
                if event.type == pygame.KEYUP:

                    if (event.key == pygame.K_LEFT):
                        p2.movingLeft = False
                    elif (event.key == pygame.K_a):
                        p1.movingLeft = False

                    elif (event.key == pygame.K_RIGHT):
                        p2.movingRight = False
                    elif (event.key == pygame.K_d):
                        p1.movingRight = False

                    elif (event.key == pygame.K_DOWN):
                        p2.movingDown = False
                    elif (event.key == pygame.K_s):
                        p1.movingDown = False

                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()
                if (event.type == pygame.KEYDOWN and event.key in keysDict.keys()):
                    if event.key == pygame.K_LCTRL:
                        tempNus = keysDict[event.key](p1)
                    elif event.key == pygame.K_RCTRL:
                        tempNus = keysDict[event.key](p2)
                    else:
                        tempNus = keysDict[event.key]()
                    if tempNus is not None and event.key == pygame.K_LCTRL:
                        nus1 += tempNus
                    if tempNus is not None and event.key == pygame.K_RCTRL:
                        nus2 += tempNus

            if nus1 != 0:
                nus = calculatenusiancepuyo(nus1, 2)
                if nus != 0:
                    nusiancequeue2.append(nus)  # Get's appended to opposite players nuciuance queue
                if len(nusiancequeue2)==1:
                    nus2time = time.time()
            if nus2 != 0:
                nus = calculatenusiancepuyo(nus2, 1)
                if nus != 0:
                    nusiancequeue1.append(nus)
                if len(nusiancequeue1)==1:
                    nus1time = time.time()

            if time.time() - nus1time > 4 and nusiancequeue1 != []:
                p1.add_nusiance(nusiancequeue1.pop(0))
                print("Adding nus to P1 board")
                nus1time = time.time()

            if time.time() - nus2time > 4 and nusiancequeue2 != []:
                p2.add_nusiance(nusiancequeue2.pop(0))
                print("Adding nus to P2 board")
                nus2time = time.time()



            drawallpuyo(p1, p2, "P1", "P2")
            screen.fill((255, 255, 255))

        if P1OK:
            displayendingtext(screen, "Player 1")
        else:
            displayendingtext(screen, "Player 2")


    elif Player1Game == "P1P" and Player2Game == "P2T":
        p1 = LaunchPuyoScript.main(screen, "multi")
        p2 = LaunchTetrisScript.main(screen, "multi")
        p1.init_game_values()
        p2count = 0
        keysDict = {
            pygame.K_UP: p2.Rotate,
            pygame.K_DOWN: p2.pressDown,
            pygame.K_RIGHT: p2.goRight,
            pygame.K_LEFT: p2.goLeft,
            pygame.K_RSHIFT: p2.useReserved,
            pygame.K_RCTRL: p2.goDrop,

            pygame.K_w: p1.rotate,
            pygame.K_s: p1.movedown,
            pygame.K_d: p1.moveright,
            pygame.K_a: p1.moveleft,
            pygame.K_LCTRL: p1.drop,
        }
        nus1time = 0
        nus2time = 0
        while P1OK and P2OK:
            P1OK, nus1 = puyo_puyoloop(p1, "P1")
            P2OK, p2count, nus2 = tetrisloop(p2, screen, p2count)

            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()
                if (event.type == pygame.KEYDOWN and event.key in keysDict.keys()):
                    if event.key==pygame.K_LCTRL:
                        tempNus=keysDict[event.key](p1)
                    else:
                        tempNus = keysDict[event.key]()
                    if tempNus is not None and event.key== pygame.K_LCTRL:
                        nus1+=tempNus
                    if tempNus is not None and event.key== pygame.K_RCTRL:
                        nus2+=tempNus
                if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    p2.down = False

                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_a):
                        p1.movingLeft = False
                    elif (event.key == pygame.K_d):
                        p1.movingRight = False
                    elif (event.key == pygame.K_s):
                        p1.movingDown = False

            if nus1 != 0:
                nus = calculatenusiancepuyo(nus1, 2)
                if nus != 0:
                    nuschange = calculatenusiancePT(nus, "Puyo")
                    if nuschange != 0:
                        nusiancequeue2.append(nuschange)  # Get's appended to opposite players nuciuance queue
                nus2time = time.time()
            if nus2 != 0:
                nus = calculatenusianceTetris(nus2)
                if nus != 0:
                    nuschange = calculatenusiancePT(nus, "Tetris")
                    nusiancequeue1.append(nuschange)
                nus1time = time.time()

            if time.time() - nus1time > 4 and nusiancequeue1 != []:
                p1.add_nusiance(nusiancequeue1.pop(0))
                print("Adding nus to P1 board")
                nus1time = time.time()

            if time.time() - nus2time > 4 and nusiancequeue2 != []:
                p2.add_nusiance(nusiancequeue2.pop(0))
                print("Adding nus to P2 board")
                nus2time = time.time()


            drawallpuyotetris1(p1, p2, "P1", "P2", screen)
            screen.fill((255, 255, 255))

        if P1OK:
            displayendingtext(screen, "Player 1")
        else:
            displayendingtext(screen, "Player 2")

    elif Player1Game == "P1T" and Player2Game == "P2T":
        p1 = LaunchTetrisScript.main(screen, "multi")
        p2 = LaunchTetrisScript.main(screen, "multi")

        p1count = 0
        p2count = 0
        keysDict = {
            pygame.K_UP: p2.Rotate,
            pygame.K_DOWN: p2.pressDown,
            pygame.K_RIGHT: p2.goRight,
            pygame.K_LEFT: p2.goLeft,
            pygame.K_RSHIFT: p2.useReserved,
            pygame.K_RCTRL: p2.goDrop,

            pygame.K_w: p1.Rotate,
            pygame.K_s: p1.pressDown,
            pygame.K_d: p1.goRight,
            pygame.K_a: p1.goLeft,
            pygame.K_LSHIFT: p1.useReserved,
            pygame.K_LCTRL: p1.goDrop,
        }
        nus1time = 0
        nus2time = 0

        while P1OK and P2OK:
            P1OK, p1count, nus1 = tetrisloop(p1, screen, p1count)
            P2OK, p2count, nus2 = tetrisloop(p2, screen, p2count)

            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()
                if (event.type == pygame.KEYDOWN and event.key in keysDict.keys()):
                    tempNus=keysDict[event.key]()
                    if tempNus is not None and event.key== pygame.K_LCTRL:
                        nus1+=tempNus
                    if tempNus is not None and event.key== pygame.K_RCTRL:
                        nus2+=tempNus
                if event.type == pygame.KEYUP and event.key == pygame.K_s:
                    p1.down = False
                if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    p2.down = False

            if nus1 != 0:
                nus = calculatenusianceTetris(nus1)
                if nus != 0:
                    print(nus)
                    nusiancequeue2.append(nus)  # Get's appended to opposite players nuciuance queue
                if len(nusiancequeue2)==1:
                    nus2time = time.time()
            if nus2 != 0:
                print(nus2)
                nus = calculatenusianceTetris(nus2)
                if nus != 0:
                    print(nus)
                    nusiancequeue1.append(nus)
                if len(nusiancequeue1)==1:
                    nus1time = time.time()

            if time.time() - nus1time > 4 and nusiancequeue1 != []:
                p1.add_nusiance(nusiancequeue1.pop(0))
                print("Adding nus to P1 board")
                nus1time = time.time()

            if time.time() - nus2time > 4 and nusiancequeue2 != []:
                p2.add_nusiance(nusiancequeue2.pop(0))
                print("Adding nus to P2 board")
                nus2time = time.time()



            drawallTetris(p1, p2, "P1", "P2", screen)
            screen.fill((255, 255, 255))

        if P1OK:
            displayendingtext(screen, "Player 1")
        else:
            displayendingtext(screen, "Player 2")

    elif Player1Game == "P1T" and Player2Game == "P2P":

        p1 = LaunchTetrisScript.main(screen, "multi")
        p2 = LaunchPuyoScript.main(screen, "multi")
        p2.init_game_values()
        p1count = 0
        keysDict = {
            pygame.K_UP: p2.rotate,
            pygame.K_DOWN: p2.movedown,
            pygame.K_RIGHT: p2.moveright,
            pygame.K_LEFT: p2.moveleft,
            pygame.K_RCTRL: p2.drop,

            pygame.K_LSHIFT: p1.useReserved,
            pygame.K_w: p1.Rotate,
            pygame.K_s: p1.pressDown,
            pygame.K_d: p1.goRight,
            pygame.K_a: p1.goLeft,
            pygame.K_LCTRL: p1.goDrop,
        }
        nus1time = 0
        nus2time = 0
        while P1OK and P2OK:
            P1OK, p1count, nus1 = tetrisloop(p1, screen, p1count)
            P2OK, nus2 = puyo_puyoloop(p2, "P2")

            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()
                if (event.type == pygame.KEYDOWN and event.key in keysDict.keys()):
                    if event.key==pygame.K_RCTRL:
                        tempNus=keysDict[event.key](p2)
                    else:
                        tempNus = keysDict[event.key]()
                    if tempNus is not None and event.key== pygame.K_LCTRL:
                        nus1+=tempNus
                    if tempNus is not None and event.key== pygame.K_RCTRL:
                        nus2+=tempNus
                if event.type == pygame.KEYUP and event.key == pygame.K_s:
                    p1.down = False

                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_LEFT):
                        p2.movingLeft = False
                    elif (event.key == pygame.K_RIGHT):
                        p2.movingRight = False
                    elif (event.key == pygame.K_DOWN):
                        p2.movingDown = False

            if nus1 != 0:
                nus = calculatenusianceTetris(nus1)
                if nus != 0:
                    nuschange = calculatenusiancePT(nus, "Tetris")
                    nusiancequeue2.append(nuschange)
                if len(nusiancequeue2)==1:
                    nus2time = time.time()

            if nus2 != 0:
                nus = calculatenusiancepuyo(nus2, 2)
                if nus != 0:
                    nuschange = calculatenusiancePT(nus, "Puyo")
                    if nuschange != 0:
                        nusiancequeue1.append(nuschange)  # Get's appended to opposite players nuciuance queue
                if len(nusiancequeue1)==1:
                    nus1time = time.time()

            if time.time() - nus1time > 4 and nusiancequeue1 != []:
                p1.add_nusiance(nusiancequeue1.pop(0))
                print("Adding nus to P1 board")
                nus1time = time.time()

            if time.time() - nus2time > 4 and nusiancequeue2 != []:
                p2.add_nusiance(nusiancequeue2.pop(0))
                print("Adding nus to P2 board")
                nus2time = time.time()



            drawallpuyotetris2(p1, p2, "P1", "P2", screen)
            screen.fill((255, 255, 255))

        if P1OK:
            displayendingtext(screen, "Player 1")
        else:
            displayendingtext(screen, "Player 2")








def playGameAi(screen,Player1Game,Player2Game,aiFlagP1,aiFlagP2):

    queueBoardStatesP1, queueCurrentPieceP1, movementQueueP1, queueReservedPieceP1, queueBoardStatesP2, queueCurrentPieceP2, movementQueueP2, queueReservedPieceP2 = Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(),Queue()
    gameOver, loadingScreenP1,loadingScreenP2 = Queue(), Queue(),Queue()
    gameOver.put(1)

    global nusiancequeue1,nusiancequeue2,nl2, nl1
    P1OK = True
    P2OK = True
    nus1 = 0
    nus2 = 0
    tetrisMoveSpeed=8
    puyoMoveSpeed=15
    puyoMoveSpeedAgainstItself=150
    if aiFlagP1:
        p1MoveCounter=0
    if aiFlagP2:
        p2MoveCounter=0
    if Player1Game == "P1P" and Player2Game == "P2P":
        #Creates and loads ai for each respective game if the user requested it
        if aiFlagP1:
            loadingScreenP1.put(1)
            threadAiP1 = Thread(target=PuyoPuyo.aiPuyoPuyoScript.playPuyo, args=(queueBoardStatesP1,queueCurrentPieceP1,gameOver,movementQueueP1,loadingScreenP1,),daemon=True)
            threadAiP1.start()
        if aiFlagP2:
            loadingScreenP2.put(1)
            threadAiP2 = Thread(target=PuyoPuyo.aiPuyoPuyoScript.playPuyo, args=(queueBoardStatesP2,queueCurrentPieceP2,gameOver,movementQueueP2,loadingScreenP2,),daemon=True)
            threadAiP2.start()
        #We made a loading screen to let the Ais load
        loadingScreen(screen,loadingScreenP1,loadingScreenP2)
        p1 = LaunchPuyoScript.main(screen, "multi")
        p2 = LaunchPuyoScript.main(screen, "multi")
        p1.init_game_values()
        p2.init_game_values()
        #These dictionaries contain functions that let users manipulate the games
        keysDict = {
            pygame.K_UP: p2.rotate,
            pygame.K_DOWN: p2.movedown,
            pygame.K_RIGHT: p2.moveright,
            pygame.K_LEFT: p2.moveleft,
            pygame.K_RCTRL: p2.drop,

            pygame.K_w: p1.rotate,
            pygame.K_s: p1.movedown,
            pygame.K_d: p1.moveright,
            pygame.K_a: p1.moveleft,
            pygame.K_LCTRL: p1.drop,
        }
        keysDictP1={
            "drop": p1.drop,
            "left": p1.moveleftAi,
            "right": p1.moverightAi,
            "rotate": p1.rotate,
        }
        keysDictP2={
            "drop": p2.drop,
            "left": p2.moveleftAi,
            "right": p2.moverightAi,
            "rotate": p2.rotate,
        }
        nus1time = 0
        nus2time = 0
        queueBoardStatesP1.put(p1.board)
        queueCurrentPieceP1.put(p1.currentpuyoblock)
        queueBoardStatesP2.put(p2.board)
        queueCurrentPieceP2.put(p2.currentpuyoblock)
        while P1OK and P2OK:
            P1OK, nus1 = puyo_puyoloop(p1, "P1",queueBoardStatesP1,queueCurrentPieceP1, aiFlagP1)
            P2OK, nus2 = puyo_puyoloop(p2, "P2",queueBoardStatesP2,queueCurrentPieceP2, aiFlagP2)
            if aiFlagP1:
                p1MoveCounter += 1
            if aiFlagP2:
                p2MoveCounter += 1


            for event in pygame.event.get():
                if event.type == pygame.KEYUP:

                    if (event.key == pygame.K_LEFT):
                        p2.movingLeft = False
                    elif (event.key == pygame.K_a):
                        p1.movingLeft = False

                    elif (event.key == pygame.K_RIGHT):
                        p2.movingRight = False
                    elif (event.key == pygame.K_d):
                        p1.movingRight = False

                    elif (event.key == pygame.K_DOWN):
                        p2.movingDown = False
                    elif (event.key == pygame.K_s):
                        p1.movingDown = False

                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    gameOver.get()
                    sys.exit()
                if (event.type == pygame.KEYDOWN and event.key in keysDict.keys()):
                    if event.key == pygame.K_LCTRL:
                        tempNus = keysDict[event.key](p1)
                    elif event.key == pygame.K_RCTRL:
                        tempNus = keysDict[event.key](p2)
                    else:
                        tempNus=keysDict[event.key]()
                    if tempNus is not None and event.key == pygame.K_LCTRL:
                        nus1 += tempNus
                    if tempNus is not None and event.key == pygame.K_RCTRL:
                        nus2 += tempNus
            if aiFlagP1 and not movementQueueP1.empty() and p1MoveCounter>puyoMoveSpeedAgainstItself:
                tempMovement = movementQueueP1.get()
                if tempMovement!="drop":
                    keysDictP1[tempMovement]()
                else:
                    tempNus=keysDictP1[tempMovement](p1)
                    nus1+=tempNus
                p1MoveCounter=0
            if aiFlagP2 and not movementQueueP2.empty()and p2MoveCounter>puyoMoveSpeedAgainstItself:
                tempMovement = movementQueueP2.get()
                if tempMovement != "drop":
                    keysDictP2[tempMovement]()
                else:
                    tempNus=keysDictP2[tempMovement](p2)
                    nus2+=tempNus
                p2MoveCounter=0

            if nus1 != 0:
                nus = calculatenusiancepuyo(nus1, 2)
                if nus != 0:
                    nusiancequeue2.append(nus)  # Get's appended to opposite players nuciuance queue
                if len(nusiancequeue2)==1:
                    nus2time = time.time()
            if nus2 != 0:
                nus = calculatenusiancepuyo(nus2, 1)
                if nus != 0:
                    nusiancequeue1.append(nus)
                if len(nusiancequeue1)==1:
                    nus1time = time.time()

            if time.time() - nus1time > 4 and nusiancequeue1 != []:
                p1.add_nusiance(nusiancequeue1.pop(0))
                print("Adding nus to P1 board")
                nus1time = time.time()

            if time.time() - nus2time > 4 and nusiancequeue2 != []:
                p2.add_nusiance(nusiancequeue2.pop(0))
                print("Adding nus to P2 board")
                nus2time = time.time()

            drawallpuyo(p1, p2, "P1", "P2")
            screen.fill((255, 255, 255))

        gameOverScreen(screen, gameOver,P1OK)


    elif Player1Game == "P1P" and Player2Game == "P2T":
        if aiFlagP1:
            loadingScreenP1.put(1)
            threadAiP1 = Thread(target=PuyoPuyo.aiPuyoPuyoScript.playPuyo, args=(queueBoardStatesP1,queueCurrentPieceP1,gameOver,movementQueueP1,loadingScreenP1),daemon=True)
            threadAiP1.start()
        if aiFlagP2:
            loadingScreenP2.put(1)
            threadAiP2 = Thread(target=Tetris.aiTetrisScript.playTetris, args=(queueBoardStatesP2,queueCurrentPieceP2,queueReservedPieceP2,gameOver,movementQueueP2,loadingScreenP2,),daemon=True)
            threadAiP2.start()
        loadingScreen(screen, loadingScreenP1, loadingScreenP2)
        p1 = LaunchPuyoScript.main(screen, "multi")
        p2 = LaunchTetrisScript.main(screen, "multi")
        p1.init_game_values()
        p2count = 0
        keysDictP2={
            "rotate": p2.Rotate,
            "down": p2.pressDown,
            "right": p2.goRight,
            "left": p2.goLeft,
            "drop": p2.goDrop,
            "reserve": p2.useReserved
        }
        keysDictP1={
            "drop": p1.drop,
            "left": p1.moveleftAi,
            "right": p1.moverightAi,
            "rotate": p1.rotate,
        }
        keysDict = {
            pygame.K_UP: p2.Rotate,
            pygame.K_DOWN: p2.pressDown,
            pygame.K_RIGHT: p2.goRight,
            pygame.K_LEFT: p2.goLeft,
            pygame.K_RSHIFT: p2.useReserved,
            pygame.K_RCTRL: p2.goDrop,

            pygame.K_w: p1.rotate,
            pygame.K_s: p1.movedown,
            pygame.K_d: p1.moveright,
            pygame.K_a: p1.moveleft,
            pygame.K_LCTRL: p1.drop,
        }
        nus1time = 0
        nus2time = 0
        queueBoardStatesP1.put(p1.board)
        queueCurrentPieceP1.put(p1.currentpuyoblock)
        while P1OK and P2OK:
            P1OK, nus1 = puyo_puyoloop(p1, "P1",queueBoardStatesP1,queueCurrentPieceP1, aiFlagP1)#
            P2OK, p2count, nus2 = tetrisloop(p2, screen, p2count,aiFlagP2,queueBoardStatesP2,queueCurrentPieceP2,queueReservedPieceP2)#
            if aiFlagP1:
                p1MoveCounter += 1
            if aiFlagP2:
                p2MoveCounter += 1

            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    gameOver.get()
                    sys.exit()
                if (event.type == pygame.KEYDOWN and event.key in keysDict.keys()):
                    if event.key==pygame.K_LCTRL:
                        tempNus=keysDict[event.key](p1)
                    else:
                        tempNus = keysDict[event.key]()
                    if tempNus is not None and event.key== pygame.K_LCTRL:
                        nus1+=tempNus
                    if tempNus is not None and event.key== pygame.K_RCTRL:
                        nus2+=tempNus
                if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    p2.down = False

                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_a):
                        p1.movingLeft = False
                    elif (event.key == pygame.K_d):
                        p1.movingRight = False
                    elif (event.key == pygame.K_s):
                        p1.movingDown = False
            #p1 is puyo p2 tetrus
            if aiFlagP2 and not movementQueueP2.empty()and p2MoveCounter>tetrisMoveSpeed:
                tempMovement= movementQueueP2.get()
                tempNusp2=keysDictP2[tempMovement]()
                p2MoveCounter=0
                if tempNusp2 is not None:
                    nus2+=tempNusp2
            if aiFlagP1 and not movementQueueP1.empty()and p1MoveCounter>puyoMoveSpeed:
                tempMovement = movementQueueP1.get()
                if tempMovement!="drop":
                    keysDictP1[tempMovement]()
                else:
                    tempNusp1=keysDictP1[tempMovement](p1)
                    nus1+=tempNusp1
                p1MoveCounter=0


            if nus1 != 0:
                nus = calculatenusiancepuyo(nus1, 2)
                if nus != 0:
                    nuschange = calculatenusiancePT(nus, "Puyo")
                    if nuschange != 0:
                        nusiancequeue2.append(nuschange)  # Get's appended to opposite players nuciuance queue
                if len(nusiancequeue2) == 1:
                    nus2time = time.time()
            if nus2 != 0:
                nus = calculatenusianceTetris(nus2)
                if nus != 0:
                    nuschange = calculatenusiancePT(nus, "Tetris")
                    nusiancequeue1.append(nuschange)
                if len(nusiancequeue1) == 1:
                    nus1time = time.time()

            if time.time() - nus1time > 4 and nusiancequeue1 != []:
                p1.add_nusiance(nusiancequeue1.pop(0))
                print("Adding nus to P1 board")
                nus1time = time.time()

            if time.time() - nus2time > 4 and nusiancequeue2 != []:
                p2.add_nusiance(nusiancequeue2.pop(0))
                print("Adding nus to P2 board")
                nus2time = time.time()


            drawallpuyotetris1(p1, p2, "P1", "P2", screen)
            screen.fill((255, 255, 255))
        gameOverScreen(screen,gameOver,P1OK)

    elif Player1Game == "P1T" and Player2Game == "P2T":
        if aiFlagP1:
            loadingScreenP1.put(1)
            threadAiP1 = Thread(target=Tetris.aiTetrisScript.playTetris, args=(queueBoardStatesP1,queueCurrentPieceP1,queueReservedPieceP1,gameOver,movementQueueP1,loadingScreenP1,),daemon=True)
            threadAiP1.start()
        if aiFlagP2:
            loadingScreenP2.put(1)
            threadAiP2 = Thread(target=Tetris.aiTetrisScript.playTetris, args=(queueBoardStatesP2,queueCurrentPieceP2,queueReservedPieceP2,gameOver,movementQueueP2,loadingScreenP2,),daemon=True)
            threadAiP2.start()
        loadingScreen(screen, loadingScreenP1, loadingScreenP2)
        p1 = LaunchTetrisScript.main(screen, "multi")
        p2 = LaunchTetrisScript.main(screen, "multi")
        p1count = 0
        p2count = 0
        keysDict = {
            pygame.K_UP: p2.Rotate,
            pygame.K_DOWN: p2.pressDown,
            pygame.K_RIGHT: p2.goRight,
            pygame.K_LEFT: p2.goLeft,
            pygame.K_RSHIFT: p2.useReserved,
            pygame.K_RCTRL: p2.goDrop,

            pygame.K_w: p1.Rotate,
            pygame.K_s: p1.pressDown,
            pygame.K_d: p1.goRight,
            pygame.K_a: p1.goLeft,
            pygame.K_LSHIFT: p1.useReserved,
            pygame.K_LCTRL: p1.goDrop
        }
        keysDictP1={
            "rotate": p1.Rotate,
            "down": p1.pressDown,
            "right": p1.goRight,
            "left": p1.goLeft,
            "drop": p1.goDrop,
            "reserve": p1.useReserved
        }
        keysDictP2={
            "rotate": p2.Rotate,
            "down": p2.pressDown,
            "right": p2.goRight,
            "left": p2.goLeft,
            "drop": p2.goDrop,
            "reserve": p2.useReserved
        }
        nus1time = 0
        nus2time = 0

        while P1OK and P2OK:
            P1OK, p1count, nus1 = tetrisloop(p1, screen, p1count,aiFlagP1,queueBoardStatesP1,queueCurrentPieceP1,queueReservedPieceP1)
            P2OK, p2count, nus2 = tetrisloop(p2, screen, p2count,aiFlagP2,queueBoardStatesP2,queueCurrentPieceP2,queueReservedPieceP2)
            if aiFlagP1:
                p1MoveCounter += 1
            if aiFlagP2:
                p2MoveCounter += 1
            if aiFlagP1 and not movementQueueP1.empty() and p1MoveCounter > tetrisMoveSpeed:
                #tempMovement = movementQueueP1.get()
                # These dictionaries are linked to commands to manipulate the games such as move left or rotate
                tempNusP1=keysDictP1[tempMovement]()
                p1MoveCounter = 0
                if tempNusP1 is not None:
                    nus1+=tempNusP1
            if aiFlagP2 and not movementQueueP2.empty() and p2MoveCounter > tetrisMoveSpeed:
                tempMovement = movementQueueP2.get()
                tempNusP2=keysDictP2[tempMovement]()
                p2MoveCounter = 0
                if tempNusP2 is not None:
                    nus2+=tempNusP2
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    gameOver.get()
                    sys.exit()
                if (event.type == pygame.KEYDOWN and event.key in keysDict.keys()):
                    tempNus=keysDict[event.key]()
                    if tempNus is not None and event.key== pygame.K_LCTRL:
                        nus1+=tempNus
                    if tempNus is not None and event.key== pygame.K_RCTRL:
                        nus2+=tempNus
                if event.type == pygame.KEYUP and event.key == pygame.K_s:
                    p1.down = False
                if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    p2.down = False

            if nus1 != 0:
                nus = calculatenusianceTetris(nus1)
                if nus != 0:
                    nusiancequeue2.append(nus)  # Get's appended to opposite players nuciuance queue
                if len(nusiancequeue2)==1:
                    nus2time = time.time()
            if nus2 != 0:
                nus = calculatenusianceTetris(nus2)
                if nus != 0:
                    nusiancequeue1.append(nus)
                if len(nusiancequeue1)==1:
                    nus1time = time.time()

            if time.time() - nus1time > 4 and nusiancequeue1 != []:
                p1.add_nusiance(nusiancequeue1.pop(0))
                print("Adding nus to P1 board")
                nus1time = time.time()

            if time.time() - nus2time > 4 and nusiancequeue2 != []:
                p2.add_nusiance(nusiancequeue2.pop(0))
                print("Adding nus to P2 board")
                nus2time = time.time()


            #Here the game checks if there is any input from the Ai to do, if there is do it

            drawallTetris(p1, p2, "P1", "P2", screen)
            screen.fill((255, 255, 255))
        gameOverScreen(screen,gameOver,P1OK)

    elif Player1Game == "P1T" and Player2Game == "P2P":
        if aiFlagP1:
            loadingScreenP1.put(1)
            threadAiP1 = Thread(target=Tetris.aiTetrisScript.playTetris, args=(queueBoardStatesP1,queueCurrentPieceP1,queueReservedPieceP1,gameOver,movementQueueP1,loadingScreenP1,),daemon=True)
            threadAiP1.start()
        if aiFlagP2:
            loadingScreenP2.put(1)
            threadAiP2 = Thread(target=PuyoPuyo.aiPuyoPuyoScript.playPuyo, args=(queueBoardStatesP2,queueCurrentPieceP2,gameOver,movementQueueP2,loadingScreenP2,),daemon=True)
            threadAiP2.start()
        loadingScreen(screen,loadingScreenP1,loadingScreenP2)
        p1 = LaunchTetrisScript.main(screen, "multi")
        p2 = LaunchPuyoScript.main(screen, "multi")
        p2.init_game_values()
        p1count = 0
        keysDict = {
            pygame.K_UP: p2.rotate,
            pygame.K_DOWN: p2.movedown,
            pygame.K_RIGHT: p2.moveright,
            pygame.K_LEFT: p2.moveleft,
            pygame.K_RCTRL: p2.drop,

            pygame.K_LSHIFT: p1.useReserved,
            pygame.K_w: p1.Rotate,
            pygame.K_s: p1.pressDown,
            pygame.K_d: p1.goRight,
            pygame.K_a: p1.goLeft,
            pygame.K_LCTRL: p1.goDrop,
        }
        keysDictP1={
            "rotate": p1.Rotate,
            "down": p1.pressDown,
            "right": p1.goRight,
            "left": p1.goLeft,
            "drop": p1.goDrop,
            "reserve": p1.useReserved
        }
        keysDictP2={
            "drop": p2.drop,
            "left": p2.moveleftAi,
            "right": p2.moverightAi,
            "rotate": p2.rotate,
        }
        nus1time = 0
        nus2time = 0
        if aiFlagP2:
            queueBoardStatesP2.put(p2.board)
            queueCurrentPieceP2.put(p2.currentpuyoblock)
        while P1OK and P2OK:
            P1OK, p1count, nus1 = tetrisloop(p1, screen, p1count,aiFlagP1,queueBoardStatesP1,queueCurrentPieceP1,queueReservedPieceP1)
            P2OK, nus2 = puyo_puyoloop(p2, "P2",queueBoardStatesP2,queueCurrentPieceP2, aiFlagP2)
            if aiFlagP1:
                p1MoveCounter+=1
            if aiFlagP2:
                p2MoveCounter+=1
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    gameOver.get()
                    sys.exit()
                if (event.type == pygame.KEYDOWN and event.key in keysDict.keys()):
                    if event.key == pygame.K_RCTRL:
                        tempNus = keysDict[event.key](p2)
                    else:
                        tempNus = keysDict[event.key]()
                    if tempNus is not None and event.key == pygame.K_LCTRL:
                        nus1 += tempNus
                    if tempNus is not None and event.key == pygame.K_RCTRL:
                        nus2 += tempNus
                if event.type == pygame.KEYUP and event.key == pygame.K_s:
                    p1.down = False

                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_LEFT):
                        p2.movingLeft = False
                    elif (event.key == pygame.K_RIGHT):
                        p2.movingRight = False
                    elif (event.key == pygame.K_DOWN):
                        p2.movingDown = False
            if aiFlagP1 and not movementQueueP1.empty() and p1MoveCounter>tetrisMoveSpeed:
                tempMovement = movementQueueP1.get()
                tempNusp1 = keysDictP1[tempMovement]()
                p1MoveCounter = 0
                if tempNusp1 is not None:
                    nus1 += tempNusp1
            if aiFlagP2 and not movementQueueP2.empty() and p2MoveCounter>puyoMoveSpeed:
                tempMovement = movementQueueP2.get()
                if tempMovement!="drop":
                    keysDictP2[tempMovement]()
                else:
                    tempNusp2=keysDictP2[tempMovement](p2)
                    nus2+=tempNusp2
                p2MoveCounter=0
            if nus1 != 0:
                nus = calculatenusianceTetris(nus1)
                if nus != 0:
                    nuschange = calculatenusiancePT(nus, "Tetris")
                    nusiancequeue2.append(nuschange)
                if len(nusiancequeue2)==1:
                    nus2time = time.time()

            if nus2 != 0:
                nus = calculatenusiancepuyo(nus2, 2)
                if nus != 0:
                    nuschange = calculatenusiancePT(nus, "Puyo")
                    if nuschange != 0:
                        nusiancequeue1.append(nuschange)  # Get's appended to opposite players nuciuance queue
                if len(nusiancequeue1)==1:
                    nus1time = time.time()

            if time.time() - nus1time > 4 and nusiancequeue1 != []:
                p1.add_nusiance(nusiancequeue1.pop(0))
                print("Adding nus to P1 board")
                nus1time = time.time()

            if time.time() - nus2time > 4 and nusiancequeue2 != []:
                p2.add_nusiance(nusiancequeue2.pop(0))
                print("Adding nus to P2 board")
                nus2time = time.time()


            drawallpuyotetris2(p1, p2, "P1", "P2", screen)
            screen.fill((255, 255, 255))
        gameOverScreen(screen,gameOver,P1OK)


def puyo_puyoloop(instance,pos,boardQueue=None,pieceQueue=None,AiFlag=False):
    nus = 0
    if instance.currentpuyoblockcheck(boardQueue,pieceQueue, AiFlag):
        return (False,nus)
    instance.checkforquit()
    instance.held_down_movement()
    nus = instance.naturalmovement(pos)
    
    return (True,nus)


def tetrisloop(tetrisInst,screen,count, aiFlag=False,queueBoardStatesP1=None,queueCurrentPieceP1=None,queueReservedPieceP1=None, ):
    amount = 0
    if tetrisInst.currentBlock is None:
        tetrisInst.newBlock()
        if aiFlag:
            queueBoardStatesP1.put(tetrisInst.field)
            queueCurrentPieceP1.put(tetrisInst.currentBlock)
            queueReservedPieceP1.put(tetrisInst.reserved)


    count+=1
    if tetrisInst.linesCleared>=10+(10*tetrisInst.level):
        tetrisInst.level+=1
    
    elif ( count>= tetrisInst.speedCheck() or tetrisInst.down) and not tetrisInst.gameOver:
        count=0
        amount = tetrisInst.goDown()
    if tetrisInst.gameOver:

        return False, count,0

    return True, count, amount

def loadingScreen(screen,loadingScreenP1,loadingScreenP2):
    textfontnorm = pygame.font.SysFont("Corbel", 48)
    loadingtext = textfontnorm.render("Game Loading",True, (0,0,0))
 

    loadingtextRect = loadingtext.get_rect()

    loadingtextRect.center = (screen.get_width() // 2, screen.get_height()  // 1.8)
    sec2 = time.time()
    count = 0
    while time.time() - sec2 < 4 or (not loadingScreenP1.empty() and not loadingScreenP2.empty()):
        screen.fill((255,255,255))
        pygame.draw.circle(screen,(0,0,0), (screen.get_width() // 1.68 , screen.get_height()  // 1.8),5)
        if count >= 400:
            pass
            pygame.draw.circle(screen,(0,0,0), (screen.get_width() // 1.68 + 15 , screen.get_height()  // 1.8),5)
        if count >= 800:
            pass
            pygame.draw.circle(screen,(0,0,0), (screen.get_width() // 1.68 + 30 , screen.get_height()  // 1.8),5)

        screen.blit(loadingtext,loadingtextRect)
        pygame.display.update()
        count+=1
        if count >= 1000:
            count = 0

def gameOverScreen(screen,gameOver,P1OK):
    gameOver.get()
    if P1OK:
        displayendingtext(screen, "Player 1")
    else:
        displayendingtext(screen, "Player 2")

def displayendingtext(screen,Player):
    text = "Game Over"
    textscore = Player + " Won the Game!"

    text2 = "Press the Enter Key to close"
    running = True
    screen.fill((255,255,255))
    pygame.display.update()
    width = screen.get_width()
    height  = screen.get_height()

    textfontnorm = pygame.font.SysFont("Corbel", 32)
    textfontsmall = pygame.font.SysFont("Corbel", 24)

    while running:
        swidth, height = pygame.display.get_surface().get_size()
        textstodisplay = textfontnorm.render(text,True, (0,0,0))
        textstodisplayRect = textstodisplay.get_rect()
        textstodisplayRect.center = (width // 2, height // 2)
        screen.blit(textstodisplay,textstodisplayRect)

        width, height = pygame.display.get_surface().get_size()
        textstodisplay = textfontnorm.render(textscore,True, (0,0,0))
        textstodisplayRect = textstodisplay.get_rect()
        textstodisplayRect.center = (width // 2, height // 1.8)
        screen.blit(textstodisplay,textstodisplayRect)

        textstodisplay = textfontsmall.render(text2,True, (0,0,0))
        textstodisplayRect = textstodisplay.get_rect()
        textstodisplayRect.center = (width // 2, height // 1.6)
        screen.blit(textstodisplay,textstodisplayRect)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.type == pygame.MOUSEBUTTONUP:
                    return
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()

def drawallpuyo(instance,instance2,pos,pos2):
    global nusiancequeue1,nusiancequeue2
    instance.drawBoard(pos)
    instance.drawscore(pos)
    instance.drawnextpiece(pos)
    if instance.currentpuyoblock != None:
        instance.drawcuurentpiece(pos)
    if nusiancequeue1 != []:
        instance.drawnus(pos,nusiancequeue1[0])

    instance2.drawBoard(pos2)
    instance2.drawscore(pos2)
    instance2.drawnextpiece(pos2)
    if instance2.currentpuyoblock != None:
        instance2.drawcuurentpiece(pos2)
    if nusiancequeue2 != []:
        instance.drawnus(pos2,nusiancequeue2[0])

    pygame.display.update()

def drawallpuyotetris1(instance,tetrisInst,pos,pos2,screen):
    global nusiancequeue1,nusiancequeue2
    width,height = screen.get_width(),screen.get_height()
    instance.drawBoard(pos)
    instance.drawscore(pos)
    instance.drawnextpiece(pos)
    if instance.currentpuyoblock != None:
        instance.drawcuurentpiece(pos)
    if nusiancequeue1 != []:
        instance.drawnus(pos,nusiancequeue1[0])


    Score = pygame.font.SysFont("Calibri" ,25, True, False).render("Score: "+str(tetrisInst.score), True,(0,0,0))
    levelText = pygame.font.SysFont("Calibri" ,25, True, False).render("Level: "+str(tetrisInst.level), True,(0,0,0))
    linesText = pygame.font.SysFont("Calibri" ,25, True, False).render("Lines: "+str(tetrisInst.linesCleared), True,(0,0,0))
    next = pygame.font.SysFont("Calibri" ,25, True, False).render("Next: ", True,(0,0,0))

    screen.blit(Score,[width/1.75,0])
    screen.blit(levelText,[width/1.75,height/30])
    screen.blit(linesText,[width/1.75,height/15])
    screen.blit(next,[width/1.15,height/12])

    tetrisInst.drawQueue(screen,pos2)
    tetrisInst.drawField(screen,pos2)
    tetrisInst.drawReserve(screen,pos2)
    if tetrisInst.currentBlock is not None:
        tetrisInst.drawBlock(screen,pos2)

    if nusiancequeue2 != []:
        tetrisInst.drawnus(pos2,nusiancequeue2[0],screen)
    
    if not tetrisInst.down:
        time.sleep(1.0/60)
    pygame.display.update()

def drawallpuyotetris2(tetrisInst,instance,pos,pos2,screen):
    width,height = screen.get_width(),screen.get_height()
    instance.drawBoard(pos2)
    instance.drawscore(pos2)
    instance.drawnextpiece(pos2)
    if instance.currentpuyoblock != None:
        instance.drawcuurentpiece(pos2)
    if nusiancequeue2 != []:
        instance.drawnus(pos2,nusiancequeue2[0])
    
    Score = pygame.font.SysFont("Calibri" ,25, True, False).render("Score: "+str(tetrisInst.score), True,(0,0,0))
    levelText = pygame.font.SysFont("Calibri" ,25, True, False).render("Level: "+str(tetrisInst.level), True,(0,0,0))
    linesText = pygame.font.SysFont("Calibri" ,25, True, False).render("Lines: "+str(tetrisInst.linesCleared), True,(0,0,0))
    next = pygame.font.SysFont("Calibri" ,25, True, False).render("Next: ", True,(0,0,0))

    screen.blit(Score,[0,0])
    screen.blit(levelText,[0,height/30])
    screen.blit(linesText,[0,height/15])
    screen.blit(next,[width/3,height/12])

    tetrisInst.drawQueue(screen,pos)
    tetrisInst.drawField(screen,pos)
    tetrisInst.drawReserve(screen,pos)
    if tetrisInst.currentBlock is not None:
        tetrisInst.drawBlock(screen,pos)

    if nusiancequeue1 != []:
        tetrisInst.drawnus(pos,nusiancequeue1[0],screen)

    if not tetrisInst.down:
        time.sleep(1.0/60)
    pygame.display.update()

def drawallTetris(tetrisInst1,tetrisInst2,pos,pos2,screen):
    global nusiancequeue1,nusiancequeue2
    width,height = screen.get_width(),screen.get_height()
    
    Score = pygame.font.SysFont("Calibri" ,25, True, False).render("Score: "+str(tetrisInst1.score), True,(0,0,0))
    levelText = pygame.font.SysFont("Calibri" ,25, True, False).render("Level: "+str(tetrisInst1.level), True,(0,0,0))
    linesText = pygame.font.SysFont("Calibri" ,25, True, False).render("Lines: "+str(tetrisInst1.linesCleared), True,(0,0,0))
    next = pygame.font.SysFont("Calibri" ,25, True, False).render("Next: ", True,(0,0,0))

    screen.blit(Score,[0,0])
    screen.blit(levelText,[0,height/30])
    screen.blit(linesText,[0,height/15])
    screen.blit(next,[width/3,height/12])

    tetrisInst1.drawQueue(screen,pos)
    tetrisInst1.drawField(screen,pos)
    tetrisInst1.drawReserve(screen,pos)
    if tetrisInst1.currentBlock is not None:
        tetrisInst1.drawBlock(screen,pos)
    #if not tetrisInst1.down:
        #time.sleep(1.0/60)
    if nusiancequeue1 != []:
        tetrisInst1.drawnus(pos,nusiancequeue1[0],screen)

    Score = pygame.font.SysFont("Calibri" ,25, True, False).render("Score: "+str(tetrisInst2.score), True,(0,0,0))
    levelText = pygame.font.SysFont("Calibri" ,25, True, False).render("Level: "+str(tetrisInst2.level), True,(0,0,0))
    linesText = pygame.font.SysFont("Calibri" ,25, True, False).render("Lines: "+str(tetrisInst2.linesCleared), True,(0,0,0))
    next = pygame.font.SysFont("Calibri" ,25, True, False).render("Next: ", True,(0,0,0))

    screen.blit(Score,[width/1.75,0])
    screen.blit(levelText,[width/1.75,height/30])
    screen.blit(linesText,[width/1.75,height/15])
    screen.blit(next,[width/1.15,height/12])

    tetrisInst2.drawQueue(screen,pos2)
    tetrisInst2.drawField(screen,pos2)
    tetrisInst2.drawReserve(screen,pos2)
    if tetrisInst2.currentBlock is not None:
        tetrisInst2.drawBlock(screen,pos2)

    if nusiancequeue2 != []:
        tetrisInst2.drawnus(pos2,nusiancequeue2[0],screen)
    
    if not tetrisInst2.down and not tetrisInst1.down:
        time.sleep(1.0/60)
    pygame.display.update()

def calculatenusiancepuyo(nus,num):
    global nl2, nl1
    if num == 1:
        np = nus/40 + nl1 
        nc = math.floor(np)
        nl1 = np - nc
    elif num == 2:
        np = nus/40 + nl2 
        nc = math.floor(np)
        nl2 = np - nc
    return nc

def calculatenusianceTetris(nus):
    if nus == 4:
        return nus
    else:
        return nus - 1

def calculatenusiancePT(nus,player):#if player given is tetris it converts to puyo and if player is puyo converts to tetris
    if player == "Tetris":
        if nus != 4:
            return 4 + nus -1
        elif nus == 4:
            return 8
    elif player == "Puyo":
        if nus < 2:
            return 0
        if nus >= 152:
            return 24
        else:
            tetrislinescal ={
            range(2,3):1,
            range(3,4):2,
            range(4,5):3,
            range(5,8):4,
            range(8,13):5,
            range(13,16):6,
            range(16,20):7,
            range(20,24):8,
            range(24,28):9,
            range(28,33):10,
            range(33,38):11,
            range(38,43):12,
            range(43,49):13,
            range(49,55):14,
            range(55,61):15,
            range(61,68):16,
            range(68,75):17,
            range(75,83):18,
            range(83,92):19,
            range(92,102):20,
            range(102,113):21,
            range(113,125):22,
            range(125,138):23,
            range(138,152):24
        }
            for key in tetrislinescal:
                if nus in key:
                    return tetrislinescal[key]
            return 0
