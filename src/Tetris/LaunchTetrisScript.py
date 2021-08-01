import pygame
import time
from . import Tetris
#from . import Shapes

def main(screen,gamevalue="single"):
    if gamevalue == "single":
        width,height = screen.get_width(),screen.get_height()
        pygame.init()
        print(pygame.display.get_surface())
        pygame.display.set_caption("Puyo Puyo Tetris")
        tetrisInst = Tetris.Tetris()
        clock = pygame.time.Clock()
        keysDict = {
            pygame.K_UP:tetrisInst.Rotate,
            pygame.K_DOWN:tetrisInst.pressDown,
            pygame.K_RIGHT:tetrisInst.goRight,
            pygame.K_LEFT:tetrisInst.goLeft,
            pygame.K_RSHIFT:tetrisInst.useReserved,
            pygame.K_RCTRL:tetrisInst.goDrop
        }
        count =0
        run = True
        while run:
            if tetrisInst.currentBlock is None:
                tetrisInst.newBlock()
            screen.fill((255, 255, 255))
            count+=1
            if tetrisInst.linesCleared>=10+(10*tetrisInst.level):
                tetrisInst.level+=1
            elif ( count>=tetrisInst.speedCheck() or tetrisInst.down) and not tetrisInst.gameOver:
                count=0
                tetrisInst.goDown()
            if tetrisInst.gameOver:
                gameOverText = pygame.font.SysFont("Calibri" ,40, True, False).render("Game Over", True,(0,0,0))
                screen.blit(gameOverText,[width/2.5,height/20])
                for event in pygame.event.get():
                    if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                        return

            text = pygame.font.SysFont("Calibri" ,25, True, False).render("Score: "+str(tetrisInst.score), True,(0,0,0))
            next = pygame.font.SysFont("Calibri" ,25, True, False).render("Next: ", True,(0,0,0))
            levelText = pygame.font.SysFont("Calibri" ,25, True, False).render("Level: "+str(tetrisInst.level), True,(0,0,0))
            linesText = pygame.font.SysFont("Calibri" ,25, True, False).render("Lines: "+str(tetrisInst.linesCleared), True,(0,0,0))
            screen.blit(text,[0,0])
            screen.blit(next,[width/1.7,height/12])
            screen.blit(levelText,[0,50])
            screen.blit(linesText,[0,100])
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or ( event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False

                if (event.type==pygame.KEYDOWN and event.key in keysDict.keys()):
                    keysDict[event.key]()
                if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    tetrisInst.down=False
            #START HERE
            tetrisInst.drawQueue(screen)
            tetrisInst.drawField(screen)
            tetrisInst.drawReserve(screen)
            if tetrisInst.currentBlock is not None:
                tetrisInst.drawBlock(screen)
            if not tetrisInst.down:
                time.sleep(1.0/60)#
            pygame.display.flip()
            clock.tick(60)
    elif gamevalue == "multi":
        return Tetris.Tetris()


    

if __name__ == '__main__':
    main()