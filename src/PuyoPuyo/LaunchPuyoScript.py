import pygame
import time
from . import puyo_puyo

def main(screen,Gamevalue = "single",pos = "Null"):#gamevalue is single or multi, Pos is postion for multiplayer either P1 or P2
    
    pygame.display.set_caption("Puyo Puyo Tetris")
    
    puyoinst = puyo_puyo.puyo_puyo(screen)
    if Gamevalue == "single":   
        while True:
            puyoinst.rungame()
            puyoinst.displayendingtext()
            return
    else:
        return puyoinst
if __name__ == "__main__":
    main()