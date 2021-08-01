
import pygame 
import sys
import os
import random
import MultiplayerScript
from PuyoPuyo import LaunchPuyoScript
from Tetris import LaunchTetrisScript
from Tetris import Shapes


def main(): 
    global screen, smallfont, largefont, mediumfont, tinyfont, evensmallerfont, Audioflag, optionr
    pygame.init()
    directory = os.path.dirname(__file__)
    f = open(directory + "\options.txt", "r")
    optionr = f.readlines()
    if (optionr[1].strip().split("=")[1]).strip() == "1":
        pygame.mixer.music.load(directory + "\data\puyotheme.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1, 0.0, 0)
        Audioflag = True
    elif (optionr[1].strip().split("=")[1]).strip() == "0":
        pygame.mixer.music.load(directory + "\data\puyotheme.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1, 0.0, 0)
        pygame.mixer.music.pause()
        Audioflag = False

    size = (optionr[0].strip().split("=")[1]).strip().split("x")
    screen = pygame.display.set_mode((int(size[0]),int(size[1])))
    f.close()

    evensmallerfont = pygame.font.SysFont("Corbel",15)
    tinyfont = pygame.font.SysFont("Corbel",25)
    smallfont = pygame.font.SysFont("Corbel",35)
    mediumfont = pygame.font.SysFont("Corbel",50)
    largefontsmaller = pygame.font.SysFont("Corbel",70)
    largefont = pygame.font.SysFont("Corbel",90)
    color = (255,255,255)  # white
    color_light = (170,170,170) # light shade of the button 
    color_dark = (100,100,100) # dark shade of the button

    pygame.display.set_caption("Puyo Puyo Tetris")
    logo = pygame.image.load(directory +"\data\puyologo32x32.ico")
    pygame.display.set_icon(logo)
    

    
    Titletext = largefont.render("Puyo-Puyo Tetris" , True , (0,0,0))
    Singletext = smallfont.render("Single-Player" , True , color)
    Multitext = smallfont.render("Multi-Player" , True , color)
    Optitext = smallfont.render("Options" , True , color)
    Quittext = smallfont.render("Quit Game" , True , color)
    Howtotext = smallfont.render("How to Play!", True , (0,0,0))

    HowtoImage = pygame.image.load(directory + "\data\howtoplay.png")

    
    colourlist =  [(155, 0, 0),(0, 155, 0),(0, 0, 155),(155, 155, 0),(128, 0, 128)]
    colour = random.choice(colourlist)
    tetinst = Shapes.Shapes(0,0,{})
    
    while True:
        width,height = screen.get_width(),screen.get_height()
        Singlebutton = pygame.Rect(width/2 - Singletext.get_width() + 55, height/2 - Singletext.get_height() - 50, Singletext.get_width() + 25, Singletext.get_height())
        Multibutton = pygame.Rect(width/2 - Singletext.get_width() + 55, height/2 - Multitext.get_height(), Singletext.get_width() + 25, Multitext.get_height())
        Optibutton = pygame.Rect(width/2 - Singletext.get_width() + 55, height/2 - Optitext.get_height() + 50, Singletext.get_width() + 25, Optitext.get_height())
        Quitbutton = pygame.Rect(width/2 - Singletext.get_width() + 55, height/2 - Quittext.get_height()+ 100, Singletext.get_width()+ 25, Quittext.get_height())
        HowtoButton = pygame.Rect(HowtoImage.get_rect(topleft=(width/3.75 - Howtotext.get_width() + 65 , height/2 - Howtotext.get_height()-50)))

        boardboxsize = (max(screen.get_width(),screen.get_height())/2)/8
        boxsize = int((max(screen.get_width(),screen.get_height())/2)/18)
        pixelx = width/2 - Titletext.get_width()/1.5
        pixely = height/2 - Titletext.get_height()/0.35
        pixelx2 = width/2 + Titletext.get_width()/1.8
        pixely2 = height/2 - Titletext.get_height()/0.29


        checkforquit()
        for event in pygame.event.get(): 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if Singlebutton.collidepoint(mouse_pos):
                    rungames("single")
                elif Multibutton.collidepoint(mouse_pos):
                    rungames("multi")
                elif Optibutton.collidepoint(mouse_pos):
                    Options()
                    pygame.display.update()
                elif Quitbutton.collidepoint(mouse_pos):
                    sys.exit()
                elif HowtoButton.collidepoint(mouse_pos):
                    How_to_play()
                    
        # fills the screen with a color 
        screen.fill((255, 255, 255))

        pygame.draw.circle(screen,(colour), (pixelx, pixely),boardboxsize/2)
        pygame.draw.circle(screen,(255, 255, 255), (pixelx - boardboxsize/5, pixely + boardboxsize/20),boardboxsize/5)
        pygame.draw.circle(screen,(0, 0, 0), (pixelx - boardboxsize/5, pixely + boardboxsize/20),boardboxsize/5,1)
        pygame.draw.circle(screen,(0, 0, 0), (pixelx - boardboxsize/5, pixely + boardboxsize/20),boardboxsize/7)

        pygame.draw.circle(screen,(255, 255, 255), (pixelx + boardboxsize/5, pixely + boardboxsize/20),boardboxsize/5)
        pygame.draw.circle(screen,(0, 0, 0), (pixelx + boardboxsize/5, pixely + boardboxsize/20),boardboxsize/5,1)
        pygame.draw.circle(screen,(0, 0, 0), (pixelx + boardboxsize/5, pixely + boardboxsize/20),boardboxsize/7)

        shapeY=0
        check = tetinst.currentRotation()
        for i in range(4):
                for j in range(4):
                    if check == [0,1,2,3]:
                        check = [1,4,5,6]
                    elif check == [1,2,5,6]:
                        check = [0,1,4,5]
                    if (i*4+j) in check:
                        pygame.draw.rect(screen,(0,0,0), [((pixelx2)+(boxsize*j)),((pixely2)+(boxsize*i)+(boxsize*shapeY*4)),boxsize,boxsize],2)
                        #pygame.draw.rect(screen,(0,0,0),[((1920/2)+(11*(34/2))+35*j),((1080/2)-(23*(35/2))+(35*i)+(35*shapeY*4)),50,50],1)
                        pygame.draw.rect(screen, (tetinst.colour),[((pixelx2)+boxsize*j)+1,((pixely2)+(boxsize*i)+(boxsize*shapeY*4))+1,boxsize-1,boxsize-1])
        shapeY+=1


        pygame.draw.rect(screen, (100,100,100), Singlebutton)
        pygame.draw.rect(screen, (0,0,0), Singlebutton,2)

        pygame.draw.rect(screen, (100,100,100), Multibutton)
        pygame.draw.rect(screen, (0,0,0), Multibutton,2)

        pygame.draw.rect(screen, (100,100,100), Optibutton)
        pygame.draw.rect(screen, (0,0,0), Optibutton,2)

        pygame.draw.rect(screen, (100,100,100), Quitbutton)
        pygame.draw.rect(screen, (0,0,0), Quitbutton,2)

        pygame.draw.rect(screen, (100,100,100), HowtoButton)

        screen.blit(Titletext , (width/2 - Titletext.get_width()/2, height/2 - Titletext.get_height()/0.3 ))
        screen.blit(Singletext , (width/2 - Singletext.get_width() + 65, height/2 - Singletext.get_height() - 50 ))
        screen.blit(Multitext , (width/2 - Multitext.get_width() + 60, height/2 - Multitext.get_height() ))
        screen.blit(Optitext , (width/2 - Optitext.get_width() + 28, height/2 - Optitext.get_height() + 50))
        screen.blit(Quittext , (width/2 - Quittext.get_width() + 50, height/2 - Quittext.get_height() + 100))
        screen.blit(Howtotext,(width/3.75 - Howtotext.get_width() + 65 , height/2 - Howtotext.get_height()+ 150))
        screen.blit(HowtoImage,(width/3.75 - Howtotext.get_width() + 65 , height/2 - Howtotext.get_height()-50))
        pygame.display.update()


def checkforquit():
        for event in pygame.event.get(pygame.QUIT):
                sys.exit()
        for event in pygame.event.get(pygame.KEYUP):
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            pygame.event.post(event)

def rungames(version): #version either "single" or multi"
    directory = os.path.dirname(__file__)
    width,height = screen.get_width(),screen.get_height()
    PuyoImg = pygame.image.load(directory + "\data\Puyo-Puyo.png")
    TetImg = pygame.image.load(directory + "\data\Tetris.png")
    ReturnImg = pygame.image.load(directory + "\data\Return.png")
    Returnbutton = pygame.Rect(ReturnImg.get_rect())

    if version == "single":
        Titletext = largefont.render("Singleplayer" , True , (0,0,0))
        prompt = mediumfont.render("Please Choose a Game to Play!" , True , (0,0,0))
        if width <= 1366:
            Puyobutton = pygame.Rect(PuyoImg.get_rect(topleft=(width/2 - width/3, height/2 - height/3)))
            Tetrisbutton = pygame.Rect(TetImg.get_rect(topleft = (width/2 + width/12, height/2 - height/3)))
        else:
            Puyobutton = pygame.Rect(PuyoImg.get_rect(topleft=(width/2 - width/3.5, height/2 - height/3)))
            Tetrisbutton = pygame.Rect(TetImg.get_rect(topleft = (width/2 + width/10, height/2 - height/3)))
        
        while True:
            checkforquit()
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if Puyobutton.collidepoint(mouse_pos):
                        LaunchPuyoScript.main(screen,"single")
                        return
                    elif Tetrisbutton.collidepoint(mouse_pos):
                        LaunchTetrisScript.main(screen)
                        return
                    elif Returnbutton.collidepoint(mouse_pos):
                        return

            screen.fill((255,255,255))
            
            pygame.draw.rect(screen, (100,100,100), Puyobutton)
            pygame.draw.rect(screen, (100,100,100), Tetrisbutton)

            
            if width <= 1366:
                screen.blit(Titletext , (width/1.85 - Titletext.get_width(), height/8 - Titletext.get_height()))
                screen.blit(PuyoImg, [width/2 - width/3,height/2 - height/3])
                screen.blit(TetImg, [width/2 + width/12, height/2 - height/3])
                screen.blit(prompt , (width/1.75 - Titletext.get_width(), height/1.05 - Titletext.get_height()))
            else:
                screen.blit(Titletext , (width/1.65 - Titletext.get_width(), height/8 - Titletext.get_height()))
                screen.blit(PuyoImg, [width/2 - width/3.5,height/2 - height/3])
                screen.blit(TetImg, [width/2 + width/10, height/2 - height/3])
                screen.blit(prompt , (width/1.75 - Titletext.get_width(), height/1.2 - Titletext.get_height()))
            screen.blit(ReturnImg,(0,0))

        

            pygame.display.update()


    else:
        width,height = screen.get_width(),screen.get_height()
        Titletext = largefont.render("Multiplayer" , True , (255,255,255))
        Player1text = smallfont.render("Player1", True, (255,255,255))
        Player2text = smallfont.render("Player2", True, (255,255,255))
        puyo_puyotext = smallfont.render("Puyo Puyo", True, (255,255,255))
        Tetristext = smallfont.render("Tetris", True, (255,255,255))
        startgametext = mediumfont.render("Start Game", True, (255,255,255))
        Player1Gametext = smallfont.render("Player1 Choose a Game", True, (255,255,255))
        Player2Gametext = smallfont.render("Player2 Choose a Game", True, (255,255,255))
        AiGametext = tinyfont.render("Click To Make This Player an AI", True, (255,255,255))

        Howtotext = smallfont.render("Multi-Player Info!", True , (0,0,0))

        HowtoImage = pygame.image.load(directory + "\data\howtoplay.png")
        if width == 1280 or width == 1366:
            HowtoImagerect = (HowtoImage.get_rect(topleft = (width/2.4,height/3)))
        elif width == 1600:
            HowtoImagerect = (HowtoImage.get_rect(topleft = (width/2.3,height/3)))
        else:
            HowtoImagerect = (HowtoImage.get_rect(topleft = (width/2.2,height/3)))

        buttonp11 = pygame.Rect((width/3.2 - Tetristext.get_width()/1.5) , height/2.8 , width/50, width/50) #Player1 Tetris button
        buttonp12 = pygame.Rect((width/6 - puyo_puyotext.get_width()/2),height/2.8 ,width/50, width/50)  #Player1 Puyo button

        buttonp21 = pygame.Rect((width/1.18 - Tetristext.get_width()/1.5) , height/2.8 , width/50, width/50) #Player2 Tetris button
        buttonp22 = pygame.Rect((width/1.35 - puyo_puyotext.get_width()/2),height/2.8 ,width/50, width/50)  #Player2 Puyo button
        buttonAIP2 = pygame.Rect((width/1.17 - AiGametext.get_width()/2),height/1.5 ,width/50, width/50)  #Player2 Puyo button
        buttonAIP1 = pygame.Rect((width/3.4 - AiGametext.get_width()/2),height/1.5 ,width/50, width/50)  #Player2 Puyo button
        startgamebutton = pygame.Rect((width/1.95 - startgametext.get_width()/1.3) , height/1.2 ,startgametext.get_width() *1.2, startgametext.get_height() *1.2)

       
        if width == 1920:
            Multiplayerbox = pygame.Rect(width/2.5 - Titletext.get_width()/15 - 7, height/8 - Titletext.get_height() -5 , Titletext.get_width()+ Titletext.get_width()/6, Titletext.get_height() + Titletext.get_height()/2.5)
        elif width == 1600:
            Multiplayerbox = pygame.Rect(width/2.8 - Titletext.get_width()/15 - 7, height/8 - Titletext.get_height() -5 , Titletext.get_width()+ Titletext.get_width()/6, Titletext.get_height() + Titletext.get_height()/2.5)
        elif width == 1366:
            Multiplayerbox = pygame.Rect(width/2.9 - Titletext.get_width()/15 - 7, height/8 - Titletext.get_height() -5 , Titletext.get_width()+ Titletext.get_width()/6, Titletext.get_height() + Titletext.get_height()/2.5)
        else:
             Multiplayerbox = pygame.Rect(width/3 - Titletext.get_width()/15 - 7, height/8 - Titletext.get_height() , Titletext.get_width()+ Titletext.get_width()/6, Titletext.get_height() + Titletext.get_height()/2.5)

        player1box = pygame.Rect(width/4 - Player1text.get_width() -4, height/6 - Player1text.get_height(), Player1text.get_width()+ Player1text.get_width()/10, Player1text.get_height() + Player1text.get_height()/8.5)
        player2box = pygame.Rect(width/1.25 - Player2text.get_width() -4 , height/6 - Player2text.get_height(), Player2text.get_width()+ Player2text.get_width()/10, Player2text.get_height() + Player2text.get_height()/8.5)

        Player1optionsbox = pygame.Rect(width/6.3 - Player1text.get_width(), height/3.5, width/4, width/8)
        Player2optionsbox = pygame.Rect(width/1.4 - Player2text.get_width(), height/3.5, width/4, width/8)

        Ai1box = pygame.Rect(width/6.3 - Player1text.get_width(), height/1.55, width/4, Player1Gametext.get_height() * 3)
        Ai2box = pygame.Rect(width/1.4 - Player2text.get_width(), height/1.55, width/4, Player2Gametext.get_height() * 3)


        P1Tetris = False
        P1Puyo = False
        P2Tetris = False
        P2Puyo = False
        AiflagP1 = False
        AiflagP2 = False

        Game_neededP1 = True
        Game_neededP2 = True
        while True:
            checkforquit()
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if Returnbutton.collidepoint(mouse_pos):
                            return
                    elif HowtoImagerect.collidepoint(mouse_pos):
                            How_to_play("multi")
                    elif buttonp11.collidepoint(mouse_pos):
                        P1Tetris = True
                        P1Puyo = False
                    elif buttonp12.collidepoint(mouse_pos):
                        P1Puyo = True
                        P1Tetris = False
                    elif buttonp21.collidepoint(mouse_pos):
                        P2Tetris = True
                        P2Puyo = False
                    elif buttonp22.collidepoint(mouse_pos):
                        P2Puyo = True
                        P2Tetris = False
                    elif buttonAIP2.collidepoint(mouse_pos):
                        AiflagP2 = not AiflagP2
                    elif buttonAIP1.collidepoint(mouse_pos):
                        AiflagP1 = not AiflagP1
                    elif startgamebutton.collidepoint(mouse_pos):
                        if Game_neededP1 == False and Game_neededP2 == False:
                            if AiflagP1 == False and AiflagP2 == False:
                                if P1Puyo and P2Puyo:
                                    MultiplayerScript.main(screen,"P1P","P2P")
                                elif P1Puyo and P2Tetris:
                                    MultiplayerScript.main(screen,"P1P","P2T")
                                elif P1Tetris and P2Tetris:
                                    MultiplayerScript.main(screen,"P1T","P2T")
                                else:
                                    MultiplayerScript.main(screen,"P1T","P2P")
                            else:
                                if P1Puyo and P2Puyo:
                                    MultiplayerScript.main(screen, "P1P", "P2P",AiflagP1,AiflagP2)
                                elif P1Puyo and P2Tetris:
                                    MultiplayerScript.main(screen, "P1P", "P2T",AiflagP1,AiflagP2)
                                elif P1Tetris and P2Tetris:
                                    MultiplayerScript.main(screen, "P1T", "P2T",AiflagP1,AiflagP2)
                                else:
                                    MultiplayerScript.main(screen, "P1T", "P2P",AiflagP1,AiflagP2)

            if P1Tetris or P1Puyo:
                Game_neededP1 = False
            if P2Tetris or P2Puyo:
                Game_neededP2 = False
                     
            screen.fill((255,255,255))
            screen.blit(ReturnImg,(0,0))
            
            
            pygame.draw.rect(screen, (100,100,100),Multiplayerbox)
            pygame.draw.rect(screen, (0,0,0),Multiplayerbox,2)

            
            pygame.draw.rect(screen, (100,100,100),player1box)
            pygame.draw.rect(screen, (0,0,0),player1box,2)
           
            pygame.draw.rect(screen, (100,100,100),player2box)
            pygame.draw.rect(screen, (0,0,0),player2box,2)

            pygame.draw.rect(screen, (100,100,100),Player1optionsbox)
            pygame.draw.rect(screen, (0,0,0),Player1optionsbox,2)

            pygame.draw.rect(screen, (100,100,100),Player2optionsbox)
            pygame.draw.rect(screen, (0,0,0),Player2optionsbox,2)

            pygame.draw.rect(screen, (100,100,100),Ai1box)
            pygame.draw.rect(screen, (0,0,0),Ai1box,2)

            pygame.draw.rect(screen, (100,100,100),Ai2box)
            pygame.draw.rect(screen, (0,0,0),Ai2box,2)

            if width == 1366 or width == 1280:
                screen.blit(Titletext , (width/2.9 , height/8 - Titletext.get_height() +5 ))
            elif width == 1600:
                screen.blit(Titletext , (width/2.8 , height/8 - Titletext.get_height()))
            else:
                screen.blit(Titletext , (width/2.5 , height/8 - Titletext.get_height()))

            screen.blit(AiGametext , (width/4.8 - AiGametext.get_width()/2,height/1.4))
            if AiflagP1 == False:
                pygame.draw.rect(screen, (255,255,255),buttonAIP1,2)
            else:
                pygame.draw.rect(screen, (0,0,0),buttonAIP1)
                pygame.draw.rect(screen, (255,255,255),buttonAIP1,2)

            screen.blit(AiGametext , (width/1.3 - AiGametext.get_width()/2,height/1.4))
            if AiflagP2 == False:
                pygame.draw.rect(screen, (255,255,255),buttonAIP2,2)
            else:
                pygame.draw.rect(screen, (0,0,0),buttonAIP2)
                pygame.draw.rect(screen, (255,255,255),buttonAIP2,2)

            screen.blit(Player1text , (width/4 - Player1text.get_width(), height/6 - Player1text.get_height())) 
            #Player1 Options display

            screen.blit(Tetristext , (width/3 - Player1text.get_width(), height/3 - Player1text.get_height()))
            screen.blit(puyo_puyotext , (width/6 - Player1text.get_width(), height/3 - Player1text.get_height()))
            if P1Tetris == True:
                pygame.draw.rect(screen, (0,0,0),buttonp11)
                pygame.draw.rect(screen, (255,255,255),buttonp11 ,2)

            if P1Puyo == False:
                pygame.draw.rect(screen, (255,255,255),buttonp12 ,2)

            if P1Puyo == True:
                pygame.draw.rect(screen, (0,0,0),buttonp12)
                pygame.draw.rect(screen, (255,255,255),buttonp12 ,2)
                
            if P1Tetris == False:
                pygame.draw.rect(screen, (255,255,255),buttonp11,2)


            screen.blit(Player2text , (width/1.25 - Player2text.get_width(), height/6 - Player2text.get_height()))
            screen.blit(Tetristext , (width/1.15 - Player2text.get_width(), height/3 - Player2text.get_height()))
            screen.blit(puyo_puyotext , (width/1.38 - Player2text.get_width(), height/3 - Player2text.get_height()))

            if P2Tetris == True:
                pygame.draw.rect(screen, (0,0,0),buttonp21)
                pygame.draw.rect(screen, (255,255,255),buttonp21,2)

            if P2Puyo == False:
                pygame.draw.rect(screen, (255,255,255),buttonp22 ,2)

            if P2Puyo == True:
                pygame.draw.rect(screen, (0,0,0),buttonp22)
                pygame.draw.rect(screen, (255,255,255),buttonp22 ,2)
                
            if P2Tetris == False:
                pygame.draw.rect(screen, (255,255,255),buttonp21,2)

            
            #Players Game needed display
            if Game_neededP1:
                if width == 1366:
                    screen.blit(Player1Gametext , (width/3 - Player1Gametext.get_width(), height/2 - Player1Gametext.get_height()))
                elif width == 1280:
                    screen.blit(Player1Gametext , (width/2.9 - Player1Gametext.get_width(), height/2 - Player1Gametext.get_height()))
                else:
                    screen.blit(Player1Gametext , (width/3.2 - Player1Gametext.get_width(), height/2 - Player1Gametext.get_height()))    
            if Game_neededP2:
                if width == 1366 or width == 1280:
                    screen.blit(Player2Gametext , (width/1.12 - Player1Gametext.get_width(), height/2 - Player1Gametext.get_height()))
                else:
                    screen.blit(Player2Gametext , (width/1.15 - Player1Gametext.get_width(), height/2 - Player1Gametext.get_height()))

            if width == 1280 or width == 1366:
                pygame.draw.rect(screen, (0,0,0),HowtoImagerect)
                screen.blit(HowtoImage,(width/2.4,height/3))
                screen.blit(Howtotext,(width/2.4,height/1.8))
            elif width == 1600:
                pygame.draw.rect(screen, (0,0,0),HowtoImagerect)
                screen.blit(HowtoImage,(width/2.3,height/3))
                screen.blit(Howtotext,(width/2.3,height/1.8))
            else:
                pygame.draw.rect(screen, (0,0,0),HowtoImagerect)
                screen.blit(HowtoImage,(width/2.2,height/3))
                screen.blit(Howtotext,(width/2.2,height/2))

            pygame.draw.rect(screen, (100,100,100),startgamebutton)
            pygame.draw.rect(screen, (0,0,0),startgamebutton ,2)
            screen.blit(startgametext,((width/1.9 - startgametext.get_width()/1.3) , height/1.18))
            pygame.display.update()




def How_to_play(value="single"):
    width,height = screen.get_width(),screen.get_height()
    directory = os.path.dirname(__file__)
    ReturnImg = pygame.image.load(directory + "\data\Return.png")
    Returnbutton = pygame.Rect(ReturnImg.get_rect())
    Puyotitle = mediumfont.render("Puyo-Puyo", True , (0,0,0))
    Tetristitle = mediumfont.render("Tetris", True , (0,0,0))
    Player1title = mediumfont.render("Multiplayer", True , (0,0,0))

    
    while True:
        checkforquit()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if Returnbutton.collidepoint(mouse_pos):
                        return
        screen.fill((255,255,255))
        screen.blit(ReturnImg,(0,0))
        if value == "single":
            Puyotextrender(Puyotitle,width,height)
            TetristextRender(Tetristitle,width,height)
        else:
            Multiplayertextrender(Player1title,width,height)
        pygame.display.update()

def Options():
    global screen,Audioflag,optionr
    width,height = screen.get_width(),screen.get_height()
    directory = os.path.dirname(__file__)
    ReturnImg = pygame.image.load(directory + "\data\Return.png")
    AudioOnImg = pygame.image.load(directory + "\data\AudioOn.png")
    AudioOffImg = pygame.image.load(directory + "\data\AudioOff.png")


    Returnbutton = pygame.Rect(ReturnImg.get_rect())


    Screensizetext = mediumfont.render("Screen Size",True,(0,0,0))
    Audiotext = mediumfont.render("Audio On/Off",True,(0,0,0))

    Fullscreentext = smallfont.render("Fullscreen", True ,(255,255,255))
    text1920x1080 = smallfont.render("1920x1080", True ,(255,255,255))
    text1600x900 = smallfont.render("1600x900", True , (255,255,255))
    text1366x768 = smallfont.render("1366x768", True , (255,255,255))
    text1280x720 = smallfont.render("1280x720", True , (255,255,255))


    screensizelist = [(1920,1080),(1600,900),(1366,768),(1280,720)]# (width,height)
    while True:
        checkforquit()
        for event in pygame.event.get():
             if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if Returnbutton.collidepoint(mouse_pos):
                    return
                elif text1920x1080_button.collidepoint(mouse_pos):
                    width,height = screensizelist[0]
                    screen = pygame.display.set_mode((width,height))
                    optionr[0] = "Windowsize = " + str(width) + "x" + str(height)+"\n"
                
                elif text1600x900_button.collidepoint(mouse_pos):
                    width,height = screensizelist[1]
                    screen = pygame.display.set_mode((width,height))
                    optionr[0] = "Windowsize = " + str(width) + "x" + str(height)+"\n"

                elif text1366x768_button.collidepoint(mouse_pos):
                    width,height = screensizelist[2]
                    screen = pygame.display.set_mode((width,height))
                    optionr[0] = "Windowsize = " + str(width) + "x" + str(height)+"\n"

                elif text1280x720_button.collidepoint(mouse_pos):
                    width,height = screensizelist[3]
                    screen = pygame.display.set_mode((width,height))
                    optionr[0] =  "Windowsize = " + str(width) + "x" + str(height)+"\n"

                elif fullscreen_button.collidepoint(mouse_pos):
                    pygame.display.toggle_fullscreen()
                    width,height = screen.get_width(),screen.get_height()
                    optionr[0] = "Windowsize = " + str(width) + "x" + str(height)+"\n"

                elif Audiobutton.collidepoint(mouse_pos):
                    if Audioflag:
                        Audioflag = False
                        pygame.mixer.music.pause()
                        optionr[1] = "Audio = 0"
                    else:
                        Audioflag = True
                        pygame.mixer.music.unpause()
                        optionr[1] = "Audio = 1"
                    print(optionr)

                
        Audiobutton = pygame.Rect(AudioOnImg.get_rect(topleft = (width/2.15 , height/1.4)))
        text1920x1080_button = pygame.Rect(width/6 - text1920x1080.get_width() , height/2 - text1920x1080.get_height() - 50, text1920x1080.get_width() * 1.5, text1600x900.get_height() * 1.5 )
        text1600x900_button = pygame.Rect(width/3 - text1600x900.get_width() , height/2 - text1600x900.get_height() - 50, text1920x1080.get_width() * 1.5, text1600x900.get_height()* 1.5)
        text1366x768_button = pygame.Rect(width/1.5 - text1366x768.get_width() , height/2 - text1366x768.get_height() - 50, text1920x1080.get_width() * 1.5, text1366x768.get_height()* 1.5)
        text1280x720_button = pygame.Rect(width - text1280x720.get_width() - width/6.5 , height/2 - text1280x720.get_height() - 50, text1920x1080.get_width() * 1.5, text1280x720.get_height()* 1.5)

        fullscreen_button = pygame.Rect(width/2 - text1366x768.get_width() , height/2 - text1366x768.get_height() + 50 , text1920x1080.get_width() * 1.5, text1366x768.get_height()* 1.5)

        screen.fill((255,255,255))
        pygame.draw.rect(screen,(100,100,100),Audiobutton)
        screen.blit(ReturnImg,(0,0))
        if Audioflag:
            screen.blit(AudioOnImg,(width/2.15 , height/1.4 , AudioOnImg.get_width() + 25, AudioOnImg.get_height()))
        else:
             screen.blit(AudioOffImg,(width/2.15 , height/1.4 , AudioOffImg.get_width() + 25, AudioOffImg.get_height()))

        screen.blit(Screensizetext,(width/1.8 - Screensizetext.get_width() + 10, height/3 - Screensizetext.get_height(), Screensizetext.get_width() + 25, Screensizetext.get_height()))
        screen.blit(Audiotext,(width/1.85 - Screensizetext.get_width() + 10, height/1.4 - Screensizetext.get_height(), Screensizetext.get_width() + 25, Screensizetext.get_height()))



        pygame.draw.rect(screen, (100,100,100), fullscreen_button)
        pygame.draw.rect(screen, (0,0,0), fullscreen_button,2)

        pygame.draw.rect(screen, (100,100,100), text1920x1080_button)
        pygame.draw.rect(screen, (0,0,0), text1920x1080_button,2)

        pygame.draw.rect(screen, (100,100,100), text1600x900_button)
        pygame.draw.rect(screen, (0,0,0), text1600x900_button,2)

        pygame.draw.rect(screen, (100,100,100), text1366x768_button)
        pygame.draw.rect(screen, (0,0,0), text1366x768_button,2)

        pygame.draw.rect(screen, (100,100,100), text1280x720_button)
        pygame.draw.rect(screen, (0,0,0), text1280x720_button,2)


        screen.blit(Fullscreentext, (width/2 - text1366x768.get_width() *0.7 , height/2 - text1366x768.get_height() + 60 , text1366x768.get_width() + 25, text1366x768.get_height()))
        screen.blit(text1920x1080,(width/6 - text1920x1080.get_width() *0.75 , height/2 - text1920x1080.get_height() - 40, text1920x1080.get_width() + 25, text1920x1080.get_height()))
        screen.blit(text1600x900,(width/3 - text1920x1080.get_width() *0.65, height/2 - text1920x1080.get_height() - 40, text1920x1080.get_width() + 25, text1920x1080.get_height()))
        screen.blit(text1366x768,(width/1.5 - text1366x768.get_width() *0.65, height/2 - text1366x768.get_height() - 40, text1366x768.get_width() + 25, text1366x768.get_height()))
        screen.blit(text1280x720,(width * 0.85 - text1280x720.get_width()*0.7, height/2 - text1280x720.get_height() - 40, text1280x720.get_width() + 25, text1280x720.get_height()))

        pygame.display.update()
        f = open(directory + "\options.txt", "w")
        f.writelines(optionr)
        f.close()


def Puyotextrender(Puyotitle,width,height):

    text1 = "Puyo Puyo is a real time puzzle game based\non a vertical board filled with pairs of slime\nshaped objects called Puyo. Each set of Puyo\ncan be made up of one or more colours.\n(Red, Green, Blue, Yellow, Purple)"
    text2 = "Puyo fall from the top of the board towards\nthe bottom. They can be moved by the player\nfrom side to side, downwards and can be rotated.\nUpon reaching the bottom of the board or another\npuyo the current Puyo set stops and any puyo of\nthe set with nothing below it falls."
    text3 = "The way the game is played is to match puyo\nof the same colour beside each other, should\n4 or more of the same colour connect they pop\nand any puyo above them fall and the process\nrepeats. If any of the falling puyo make a new match,\nthis is called a chain. The aim is to get the longest\nchains of puyo possible as they give more points.\nShould the board fill up to the top with puyo the\ngame ends."
    controls = "LEFT = A or Left Arrow\nRIGHT = D or Right Arrow\nDOWN = S or Down Arrow\nROTATE = W or Up Arrow\nDROP = Left Control"
    if width < 1600:
        screen.blit(Puyotitle,(width/3 - Puyotitle.get_width() , height/18))
        render_multi_line_text(text1,width/3 - Puyotitle.get_width() ,height/7,15)
        render_multi_line_text(text2,width/3 - Puyotitle.get_width() ,height/3.5,15)
        render_multi_line_text(text3,width/3 - Puyotitle.get_width() ,height/2.2,15)
        screen.blit(tinyfont.render("Single Player Control Defaults:", True, (0,0,0)), (width/3 - Puyotitle.get_width() ,height/1.4))
        render_multi_line_text(controls,width/3 - Puyotitle.get_width() ,height/1.33,15)
    else:
        screen.blit(Puyotitle,(width/3.5 - Puyotitle.get_width() , height/18))
        render_multi_line_text(text1,width/4 - Puyotitle.get_width() ,height/7,25)
        render_multi_line_text(text2,width/4 - Puyotitle.get_width() ,height/3.5,25)
        render_multi_line_text(text3,width/4 - Puyotitle.get_width() ,height/2.2,25)
        screen.blit(smallfont.render("Single Player Control Defaults:", True, (0,0,0)), (width/4 - Puyotitle.get_width() ,height/1.4))
        render_multi_line_text(controls,width/4 - Puyotitle.get_width() ,height/1.3,25)

def Multiplayertextrender(Puyotitle,width,height):

    text1 = "The Multi-Player version of the game is split into several different parts based around the two games and the AI opponent.\nEach Player selects the game they want to play by clicking on the small square below the words Puyo Puyo or Tetris with \nplayer 1 on the left and player 2 on the right."
    text2 = "Once each player selects their prefered game the game can be started by clicking on the Start Game button at the bottom\nmiddle of the screen. Should you wish to have one or more of the games played by an AI, then you can select which player(s)\nwill be played by an AI by clicking on the small square button on either side of the board depending on which player is\nwanted to be an AI. The game can then be started as normal by clicking the Start game button in the middle of the screen."
    controls1 = "LEFT = A Key\nRIGHT = D Key\nDOWN = S Key\nROTATE = W Key\nDROP = Left Control\n"
    controls12 = "FOR TETRIS ONLY:\nRESERVE = Left Shift"
    controls2 = "LEFT = Left Arrow\nRIGHT = Right Arrow\nDOWN = Down Arrow\nROTATE = Up Arrow\nDROP = Right Control"
    controls22 = "FOR TETRIS ONLY:\nRESERVE = Right Shift"
    
    screen.blit(Puyotitle,(width/1.8 - Puyotitle.get_width() , height/18))
    if width < 1600:
        render_multi_line_text(text1,width/4.5 - Puyotitle.get_width() ,height/7,25)
        render_multi_line_text(text2,width/4.5 - Puyotitle.get_width() ,height/3.5,25)
        screen.blit(smallfont.render("Player 1 Control Defaults:", True, (0,0,0)), (width/3 - Puyotitle.get_width() ,height/1.75))
        render_multi_line_text(controls1,width/2.8 - Puyotitle.get_width() ,height/1.6,25)
        render_multi_line_text(controls12,width/2.8- Puyotitle.get_width() ,height/1.2,25)
        screen.blit(smallfont.render("Player2 Control Defaults:", True, (0,0,0)), (width - Puyotitle.get_width()- width/3,height/1.75))
        render_multi_line_text(controls2,width - Puyotitle.get_width()- width/3.2,height/1.6,25)
        render_multi_line_text(controls22,width - Puyotitle.get_width()- width/3.2,height/1.2,25)

    else:
        render_multi_line_text(text1,width/3.8 - Puyotitle.get_width() ,height/7,25)
        render_multi_line_text(text2,width/3.8 - Puyotitle.get_width() ,height/3.5,25)
        screen.blit(smallfont.render("Player 1 Control Defaults:", True, (0,0,0)), (width/3.8 - Puyotitle.get_width() ,height/1.75))
        render_multi_line_text(controls1,width/3.6 - Puyotitle.get_width() ,height/1.6,25)
        render_multi_line_text(controls12,width/3.6 - Puyotitle.get_width() ,height/1.28,25)
        screen.blit(smallfont.render("Player2 Control Defaults:", True, (0,0,0)), (width - Puyotitle.get_width()- width/3,height/1.75))
        render_multi_line_text(controls2,width - Puyotitle.get_width()- width/3.2,height/1.6,25)
        render_multi_line_text(controls22,width - Puyotitle.get_width()- width/3.2,height/1.28,25)

def TetristextRender(Tetristitle,width,height):
    
    text1 = "Tetris is a real time puzzle game based on a\nvertical board filled with tetrimino blocks.\nEach block can come in 7 different configurations.\n(Line, J-Block, T-Block, S-Block, L-Block, Z-Block, Square)"
    text2 = "Tetris blocks fall from the top of the board towards\nthe bottom. They can be moved by the player\nfrom side to side, downwards and can be rotated.\nUpon reaching the bottom of the board or another\nblock the current block stops."
    text3 = "The way the game is played is to create lines\nof these blocks accross the board filling a full\nhorizontal line, should this happen the line(s)\nfilled disappear and the blocks above move down.\nThe aim is to get as many lines as possible as they\ngive more points. Should the board fill up to the\ntop with blocks the game ends."
    controls = "LEFT = Left Arrow\nRIGHT = Right Arrow\nDOWN = Down Arrow\nROTATE = Up Arrow\nRESERVE = Right Shift\nDROP = Right Control"
    
    screen.blit(Tetristitle,(width/2.2 + width/4 - Tetristitle.get_width() , height/18))
    if width < 1600:
        render_multi_line_text(text1,width - Tetristitle.get_width()- width/3,height/7,15)
        render_multi_line_text(text2,width - Tetristitle.get_width()- width/3,height/3.75,15)
        render_multi_line_text(text3,width - Tetristitle.get_width()- width/3,height/2.4,15)
        screen.blit(tinyfont.render("Single Player Control Defaults:", True, (0,0,0)), (width - Tetristitle.get_width()- width/3,height/1.5))
        render_multi_line_text(controls,width - Tetristitle.get_width()- width/3,height/1.35,15)
    
    else:
        render_multi_line_text(text1,width - Tetristitle.get_width()- width/3,height/7,25)
        render_multi_line_text(text2,width - Tetristitle.get_width()- width/3,height/3.75,25)
        render_multi_line_text(text3,width - Tetristitle.get_width()- width/3,height/2.4,25)
        screen.blit(smallfont.render("Single Player Control Defaults:", True, (0,0,0)), (width - Tetristitle.get_width()- width/3,height/1.5))
        render_multi_line_text(controls,width - Tetristitle.get_width()- width/3,height/1.4,25)


def render_multi_line_text(text, x, y, fsize):
    if fsize == 15:
        lines = text.splitlines()
        for i, l in enumerate(lines):
            screen.blit(evensmallerfont.render(l, True, (0,0,0)), (x, y + fsize*i))
    else:
        lines = text.splitlines()
        for i, l in enumerate(lines):
            screen.blit(tinyfont.render(l, True, (0,0,0)), (x, y + fsize*i))

if __name__ == "__main__":
    main()
