import pygame, sys, time, random
from time import sleep

class puyo_puyo:

    def __init__(self,screen,renderOnEpisodeCount=1,episode=1):
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.size = (self.width, self.height)
        self.boardboxsize = (max(self.width,self.height)/2)/12
        self.boardwidth = 6
        self.boardheight = 12
        self.boardblank = "."
        self.textfontnorm = pygame.font.SysFont("Calibri", 32,True)
        self.textfontsmall = pygame.font.SysFont("Calibri", 24,True)
        self.screen = pygame.display.set_mode(self.size,pygame.RESIZABLE)
        self.renderOnEpisodeCount = renderOnEpisodeCount
        self.episodeNumber=episode
        self.xmargin = int((self.width - self.boardwidth * self.boardboxsize) / 2)
        self.ymargin = self.height - (self.boardheight * self.boardboxsize) - 5

        self.movesidewaysfreq = 0.15
        self.movedownfreq = 0.025
        self.fallfreq = 1.2
        self.score = 0 #(10 *pc) * (cp +cb + gb)
        self.board = self.getstartboard()
        


        # RGB Values
        self.bgcolour = (60,25,60)
        self.white   = (255, 255, 255)
        self.black   = (0, 0, 0)
        self.red     = (155, 0, 0)
        self.green   = (0, 155, 0)
        self.blue    = (0, 0, 155)
        self.yellow  = (155, 155, 0)
        self.purple  = (128, 0, 128)
        self.grey    = (128, 128, 128)

        self.puyocombinations = [(self.red,self.red),(self.red,self.green),(self.red,self.blue),(self.red,self.yellow),(self.red,self.purple),
                            (self.green,self.green),(self.green,self.blue),(self.green,self.yellow),(self.green,self.purple),
                            (self.blue,self.blue),(self.blue,self.yellow),(self.blue,self.purple),(self.yellow,self.yellow),(self.yellow,self.purple),
                            (self.purple,self.purple)]


        #3X3 matrice
        #[0,1,2]
        #[3,4,5]
        #[6,7,8]
        # if a puyo is in that pos it has those nums
        self.Puyo_movement_template =[[1,4],[4,5],[4,7],[3,4]]
        self.lastMoveDownTime = 0
        self.lastMoveSidewaysTime = 0
        self.lastFallTime = 0
        self.movingDown = False
        self.movingLeft = False
        self.movingRight = False
        self.currentpuyoblock = 0
        self.nextpuyoblock = 0
        self.justSpawnedFlag=False

    def rungame(self,pos ="Null"):
        running = True
        self.screen.fill(self.white)
        pygame.display.update()

        numpuyo_inchain = 0 #pc
        numchains = 0 #cp
        numcolour_inchain = 0 #cb
        numpuyo_ingroup_inchain_combined = 0 #gb

        self.lastMoveDownTime = time.time()
        self.lastMoveSidewaysTime = time.time()
        self.lastFallTime = time.time()
        self.movingDown = False
        self.movingLeft = False
        self.movingRight = False

        # Not sure if it gets faster over time for puyo puyo

        self.currentpuyoblock = self.getnewpuyo()
        self.nextpuyoblock = self.getnewpuyo()
        #Maybe add two lookahead
        self.currentpuyoblock["y1"] = 0
        self.currentpuyoblock["y2"] = 1
        #Work around

        while running:
            if self.currentpuyoblockcheck():
                return
            self.checkforquit()
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_p):
                        self.pause()
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                        self.movingLeft = False
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                        self.movingRight = False
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                        self.movingDown = False
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                        self.moveleft()
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                        self.moveright()
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w):
                        self.rotate()
                        #maybe add rotation in other direction ie q?
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                        self.movedown()
                    elif (event.key==pygame.K_RCTRL or event.key==pygame.K_LCTRL):
                        self.drop()
            self.held_down_movement()
            self.naturalmovement()
            
            #drawing it all on
            if pos == "Null":
                self.draw_all_on_screen()
            else:
                self.draw_all_on_screen(pos)

    def scoreLines(self,pos):
        final_block = self.addtoboard(self.currentpuyoblock,pos)
        self.currentpuyoblock = None
        values = self.chaincheckandremove(final_block,pos)
        if values != 0:
            #calculate score based on values given back then update score
            #(collist,numchains,numpuyo,groupbonus)
            #(10 *pc) * (cp +cb + gb)
            chain_power = self.cal_chainpower(values[1])
            colour_bonus = self.cal_colbonus(len(values[0]))
            groupbonus = self.cal_colbonus(values[3])
            rhs = chain_power + colour_bonus + groupbonus
            if rhs > 999:
                rhs = 999
            lhs = (10 * values[2])
            self.score += lhs + rhs
            return lhs + rhs
        return 0

    def pause(self):
        self.screen.fill(self.white)
        pygame.mixer.music.pause()
        self.displaypausetext()
        pygame.mixer.music.unpause()
        self.lastMoveDownTime = time.time()
        self.lastMoveSidewaysTime = time.time()
        self.lastFallTime = time.time()
        
    def moveleft(self):
        if self.isvalidmovement("left"):
            self.currentpuyoblock["x1"] -= 1
            self.currentpuyoblock["x2"] -= 1
            self.movingLeft = True
            self.movingRight = False
            self.lastMoveSidewaysTime = time.time()

    def moveleftAi(self):
        if self.isvalidmovement("left"):
            self.currentpuyoblock["x1"] -= 1
            self.currentpuyoblock["x2"] -= 1
            self.lastMoveSidewaysTime = time.time()

    def moveright(self):
        if self.isvalidmovement("right"):
            self.currentpuyoblock["x1"] += 1
            self.currentpuyoblock["x2"] += 1
            self.movingLeft = False
            self.movingRight = True
            self.lastMoveSidewaysTime = time.time()

    def moverightAi(self):
        if self.isvalidmovement("right"):
            self.currentpuyoblock["x1"] += 1
            self.currentpuyoblock["x2"] += 1
            self.lastMoveSidewaysTime = time.time()

    def rotate(self):
        if self.isvalidmovement("rotate"):
            self.currentpuyoblock["rotation"] = self.Puyo_movement_template[(self.Puyo_movement_template.index(self.currentpuyoblock['rotation'])+ 1) % len(self.Puyo_movement_template)]
            #change pos after use the new roation to figure out old one and then move the postions
            if self.currentpuyoblock["rotation"] == [1,4]:
                self.currentpuyoblock["x1"] = self.currentpuyoblock["x2"]
                self.currentpuyoblock["y1"] = self.currentpuyoblock["y2"] - 1
            elif self.currentpuyoblock["rotation"] == [4,5]:
                self.currentpuyoblock["x1"] = self.currentpuyoblock["x2"] + 1
                self.currentpuyoblock["y1"] = self.currentpuyoblock["y2"]
            elif self.currentpuyoblock["rotation"] == [4,7]:
                self.currentpuyoblock["x1"] = self.currentpuyoblock["x2"]
                self.currentpuyoblock["y1"] = self.currentpuyoblock["y2"] + 1
            elif self.currentpuyoblock["rotation"] == [3,4]:
                self.currentpuyoblock["x1"] = self.currentpuyoblock["x2"] - 1
                self.currentpuyoblock["y1"] = self.currentpuyoblock["y2"]
    
    def movedown(self):
        if self.isvalidmovement("down"):
            self.movingDown = True
            self.lastMoveDownTime = time.time()
            self.currentpuyoblock["y1"] = self.currentpuyoblock["y1"] + 1
            self.currentpuyoblock["y2"] = self.currentpuyoblock["y2"] + 1

    def drop(self,pos=None):
        while self.isvalidmovement("down"):
            self.lastMoveDownTime = time.time()
            self.currentpuyoblock["y1"] = self.currentpuyoblock["y1"] + 1
            self.currentpuyoblock["y2"] = self.currentpuyoblock["y2"] + 1
        return self.scoreLines(pos)

    def cal_chainpower(self,num):
        if num == 1:
            return 0
        elif num >= 9:
            return 999
        else:
            return 2 ** (num + 1)

    def cal_colbonus(self,num):
        if num == 1:
            return 0
        elif num == 2:
            return 3
        elif num == 3:
            return 6
        elif num == 4:
            return 12
        elif num == 5:
            return 24
        return 0

    def draw_all_on_screen(self,pos = "Null"):
        if pos == "Null":
            self.screen.fill(self.white)
            self.drawBoard()
            self.drawscore()
            self.drawnextpiece()
            if self.currentpuyoblock != None:
                self.drawcuurentpiece()
            pygame.display.update()
        elif pos == "P1":
            self.drawBoard(pos)
            self.drawscore(pos)
            self.drawnextpiece(pos)
            if self.currentpuyoblock != None:
                self.drawcuurentpiece(pos)
            pygame.display.update()
        elif pos == "P2":
            self.drawBoard(pos)
            self.drawscore(pos)
            self.drawnextpiece(pos)
            if self.currentpuyoblock != None:
                self.drawcuurentpiece(pos)
            pygame.display.update()
            

    def isvalidmovement(self,movementype):
        if not self.currentpuyoblock is None:
            rotation = self.currentpuyoblock["rotation"]
            top = False
            bot = False
            if movementype == "left":
                if rotation == [1,4] or rotation == [4,7]:
                    if (self.currentpuyoblock["x1"]-1) >= 0 and self.board[self.currentpuyoblock["y1"]][self.currentpuyoblock["x1"]-1] == self.boardblank:
                            top = True
                    if (self.currentpuyoblock["x2"]-1) >= 0 and self.board[self.currentpuyoblock["y2"]][self.currentpuyoblock["x2"]-1] == self.boardblank:
                            bot = True
                elif rotation == [4,5]:
                    if (self.currentpuyoblock["x2"]-1) >= 0 and self.board[self.currentpuyoblock["y2"]][self.currentpuyoblock["x2"]-1] == self.boardblank:
                            bot = True
                            top = True
                elif rotation == [3,4]:
                    if (self.currentpuyoblock["x1"]-1) >= 0 and self.board[self.currentpuyoblock["y1"]][self.currentpuyoblock["x1"]-1] == self.boardblank:
                            bot = True
                            top = True
            elif movementype == "right":
                if rotation == [1,4] or rotation == [4,7]:
                    if (self.currentpuyoblock["x1"]+1) <= 5 and self.board[self.currentpuyoblock["y1"]][self.currentpuyoblock["x1"]+1] == self.boardblank:
                            top = True
                    if (self.currentpuyoblock["x2"]+1) <= 5 and self.board[self.currentpuyoblock["y2"]][self.currentpuyoblock["x2"]+1] == self.boardblank:
                            bot = True
                elif rotation == [4,5]:
                    if (self.currentpuyoblock["x1"]+1) <= 5 and self.board[self.currentpuyoblock["y1"]][self.currentpuyoblock["x1"]+1] == self.boardblank:
                            bot = True
                            top = True
                elif rotation == [3,4]:
                    if (self.currentpuyoblock["x2"]+1) <= 5 and self.board[self.currentpuyoblock["y2"]][self.currentpuyoblock["x2"]+1] == self.boardblank:
                            bot = True
                            top = True
            elif movementype == "rotate":
                if rotation == [1,4]: # going to 4,5
                    if (self.currentpuyoblock["x2"]+1) <= 5 and self.board[self.currentpuyoblock["y2"]][self.currentpuyoblock["x2"]+1] == self.boardblank:
                            bot = True
                            top = True
                elif rotation == [4,5]: #going to 4,7
                    if (self.currentpuyoblock["y2"]+1) <= 11 and self.board[self.currentpuyoblock["y2"]+1][self.currentpuyoblock["x2"]] == self.boardblank:
                            bot = True
                            top = True
                elif rotation == [4,7]: #going to 3,4
                    if (self.currentpuyoblock["x2"]-1) >=0 and self.board[self.currentpuyoblock["y2"]][self.currentpuyoblock["x2"]-1] == self.boardblank:
                            bot = True
                            top = True
                elif rotation == [3,4]: #going to 1,4
                    if (self.currentpuyoblock["y2"]-1) >= 0 and self.board[self.currentpuyoblock["y2"]-1][self.currentpuyoblock["x2"]] == self.boardblank:
                            bot = True
                            top = True
            elif movementype == "down":
                if rotation == [1,4]:
                    if (self.currentpuyoblock["y2"]+1) <= 11 and self.board[self.currentpuyoblock["y2"]+1][self.currentpuyoblock["x2"]] == self.boardblank:
                            bot = True
                            top = True
                elif rotation == [4,5] or rotation == [3,4]:
                    if (self.currentpuyoblock["y1"]+1) <= 11 and self.board[self.currentpuyoblock["y1"]+1][self.currentpuyoblock["x1"]] == self.boardblank:
                            top = True
                    if (self.currentpuyoblock["y2"]+1) <= 11 and self.board[self.currentpuyoblock["y2"]+1][self.currentpuyoblock["x2"]] == self.boardblank:
                            bot = True
                elif rotation == [4,7]:
                    if (self.currentpuyoblock["y1"]+1) <= 11 and self.board[self.currentpuyoblock["y1"]+1][self.currentpuyoblock["x1"]] == self.boardblank:
                            bot = True
                            top = True

            if top and bot:
                return True
        return False

    def addtoboard(self,block,pos):
        #checking if needs to fall ie
        #check if either are on over hang if so bring it down
        #add both to board
        if pos == "Null":
            if (block["y1"]+1) <= 11:
                if self.board[block["y1"]+1][block["x1"]] == self.boardblank and (block["y1"]+1,block["x1"]) != (block["y2"],block["x2"]):
                        while (block["y1"]+1) <= 11 and self.board[block["y1"]+1][block["x1"]] == self.boardblank:
                            block["y1"] = block["y1"]+1
            self.board[block["y1"]][block["x1"]] = block["colours"][0]
            if (block["y2"]+1) <= 11 and self.board[block["y2"]+1][block["x2"]] == self.boardblank:
                while (block["y2"]+1) <= 11 and self.board[block["y2"]+1][block["x2"]] == self.boardblank:
                    block["y2"] = block["y2"]+1
            self.board[block["y2"]][block["x2"]] = block["colours"][1]
            self.draw_all_on_screen(pos)
        else:
            if (block["y1"]+1) <= 11:
                if self.board[block["y1"]+1][block["x1"]] == self.boardblank and (block["y1"]+1,block["x1"]) != (block["y2"],block["x2"]):
                        while (block["y1"]+1) <= 11 and self.board[block["y1"]+1][block["x1"]] == self.boardblank:
                            block["y1"] = block["y1"]+1
            self.board[block["y1"]][block["x1"]] = block["colours"][0]
            if (block["y2"]+1) <= 11 and self.board[block["y2"]+1][block["x2"]] == self.boardblank:
                while (block["y2"]+1) <= 11 and self.board[block["y2"]+1][block["x2"]] == self.boardblank:
                    block["y2"] = block["y2"]+1
            self.board[block["y2"]][block["x2"]] = block["colours"][1]
        
        return block    

    def chaincheckandremove(self,block,pos):
        collist = []
        numchains = 0
        numpuyo = 0
        groupbonus = 0

        #find highest y value to see which check first if both same do y1 first
        x1,y1 = block["x1"],block["y1"]
        x2,y2 = block["x2"],block["y2"]
        

        valyfir, valysec = min(y1,y2), 0 # Take min first as its the puyo highest up
        valxfir, valxsec = 0,0
        colourfir, coloursec = 0,0
        if valyfir == y1:
            valxfir = x1
            valysec = y2
            valxsec = x2
            colourfir = block["colours"][0]
            coloursec = block["colours"][1]
        else:
            valxfir = x2
            valysec = y1
            valxsec = x1
            colourfir = block["colours"][1]
            coloursec = block["colours"][0]
        
        # do recursive call for each of the 4 postions around each of val1 val2, if all of the 4 positions dont contain anything ruturn list containing values
        firstflag = False
        secondflag = False
        connectedblocks1 = self.checklocalrecur(valyfir,valxfir,colourfir,[(valyfir,valxfir)])
        connectedblocks1 += [(valyfir,valxfir)]


        if len(connectedblocks1) >= 4:
            firstflag = True
            if colourfir not in collist:
                collist += [colourfir]

        connectedblocks2 = self.checklocalrecur(valysec,valxsec,coloursec,[(valysec,valxsec)])
        connectedblocks2 += [(valysec,valxsec)]

        if len(connectedblocks2) >= 4:
            secondflag = True
            if coloursec not in collist:
                collist += [coloursec]

        if firstflag or secondflag:
            greylist = []
            if firstflag and secondflag:
                greylist = connectedblocks1 + connectedblocks2
                self.removegrey(greylist)
                firstflag = False
                secondflag = False
                firstpop = self.poppuyo(connectedblocks1)
                secondpop = self.poppuyo(connectedblocks2)
                numchains +=2
                numpuyo += firstpop[0] + secondpop[0]
                groupbonus += firstpop[1] + secondpop[1]
                if pos == "Null":
                    self.draw_all_on_screen(pos)

                # both need to be poped, data recorded and screen updated
            elif firstflag:
                greylist = connectedblocks1
                self.removegrey(greylist)
                firstflag = False
                firstpop = self.poppuyo(connectedblocks1)
                numchains +=1
                numpuyo += firstpop[0]
                groupbonus += firstpop[1]
                if pos == "Null":
                    self.draw_all_on_screen(pos)
            elif secondflag:
                greylist = connectedblocks2
                self.removegrey(greylist)
                secondpop = self.poppuyo(connectedblocks2)
                numchains +=1
                numpuyo += secondpop[0]
                groupbonus += secondpop[1]
                if pos == "Null":
                    self.draw_all_on_screen(pos)
            
            #bring all pieces down and check for new chains
            pos_chain_vals = self.move_down_floating()
            if pos == "Null":
                self.draw_all_on_screen(pos)

            pop_vals = []
            pop_valsind = []
            while pos_chain_vals != []:
                for val in pos_chain_vals:
                    if val not in pop_valsind:
                        pops = self.check_indidual_chain(val)
                        if pops != 0:
                            pop_vals += [pops]
                            pop_valsind += pops
                            if self.board[val[0]][val[1]] not in collist:
                                collist += [self.board[val[0]][val[1]]]
                if pop_vals != []:
                    for each in pop_vals:
                        popped = self.poppuyo(each)
                        numchains +=1
                        numpuyo += popped[0]
                        groupbonus += popped[1]
                        if pos == "Null":
                            self.draw_all_on_screen(pos)
                    pos_chain_vals = self.move_down_floating()
                    pop_vals = []
                    pop_valsind = []
                else:
                    pos_chain_vals = []
            if pos == "Null":
                self.draw_all_on_screen(pos)
            return (collist,numchains,numpuyo,groupbonus)

        return 0 #no chains found

    def removegrey(self,list):
        for puyo in list: # each puyo is a tuple of (y,x)
            if puyo[0] + 1 <= 11:#down
                if self.board[puyo[0] + 1][puyo[1]] == self.grey:
                    self.board[puyo[0] + 1][puyo[1]] = self.boardblank

            if puyo[0] - 1 >= 0:#up
                if self.board[puyo[0] - 1][puyo[1]] == self.grey:
                    self.board[puyo[0] - 1][puyo[1]] = self.boardblank

            if puyo[1] - 1 >= 0:#left
                if self.board[puyo[0]][puyo[1]- 1] == self.grey:
                    self.board[puyo[0]][puyo[1]- 1] = self.boardblank

            if puyo[1] + 1 <= 5 :#right
                if self.board[puyo[0]][puyo[1]+ 1] == self.grey:
                    self.board[puyo[0]][puyo[1]+ 1] = self.boardblank

    def move_down_floating(self):
        positions = []
        y = 10
        x = 5
        while y >=0:
            while x >=0:
                if self.board[y+1][x] == self.boardblank and self.board[y][x] != self.boardblank:
                    oldy, oldx = y,x
                    newy, newx = y,x
                    while (newy+1) <= 11 and self.board[newy+1][newx] == self.boardblank:
                        newy = newy+1
                    positions += [(newy,newx)]
                    self.board[newy][newx] = self.board[oldy][oldx]
                    self.board[oldy][oldx] = self.boardblank
                x -= 1
            y -= 1
            x = 5
        return positions

    def check_indidual_chain(self,val):
        connectedblocks = self.checklocalrecur(val[0],val[1],self.board[val[0]][val[1]],[(val[0],val[1])])
        connectedblocks += [(val[0],val[1])]
        if len(connectedblocks) >= 4:
            return connectedblocks
        return 0 

    def poppuyo(self,puyolist):
        numpuyo = 0
        for tup in puyolist:
            numpuyo += 1
            self.board[tup[0]][tup[1]] = "."
        groupbonus = 0
        if numpuyo == 4:
            groupbonus = 0
        elif numpuyo == 5:
            groupbonus = 2
        elif numpuyo == 6:
            groupbonus = 3
        elif numpuyo == 7:
            groupbonus = 4
        elif numpuyo == 8:
            groupbonus = 5
        elif numpuyo == 9:
            groupbonus = 6
        elif numpuyo == 10:
            groupbonus = 7
        else:
            groupbonus = 10
        return((numpuyo,groupbonus))

    def checklocalrecur(self,y,x,colour,poschecked =[]):
        values = [] #up,down,left,right

        if y-1 >=0 and (y-1,x) not in poschecked :#up
            poschecked += [(y-1,x)]
            if self.board[y-1][x] == colour:
                values += [(y-1,x)]
                values += self.checklocalrecur(y-1,x,colour,poschecked)

        if y+1 <=11 and (y+1,x) not in poschecked:#down
            poschecked += [(y+1,x)]
            if self.board[y+1][x] == colour:
                values += [(y+1,x)]
                values += self.checklocalrecur(y+1,x,colour,poschecked)

        if x-1 >=0 and (y,x-1) not in poschecked:#left
            poschecked += [(y,x-1)]
            if self.board[y][x-1] == colour:
                values += [(y,x-1)]
                values += self.checklocalrecur(y,x-1,colour,poschecked)


        if x+1 <=5 and (y,x+1) not in poschecked:#right
            poschecked += [(y,x+1)]
            if self.board[y][x+1] == colour:
                values += [(y,x+1)]
                values += self.checklocalrecur(y,x+1,colour,poschecked)

        return values

    def displayopeningtext(self):
        pygame.mixer.music.load("data/puyotheme.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1, 0.0, 0)
        self.screen.fill(self.white)
        pygame.display.update()
        text = "Press button to Start Game"
        running = True
        while running:
            self.width, self.height = pygame.display.get_surface().get_size()
            textstodisplay = self.textfontnorm.render(text,True, self.black)
            textstodisplayRect = textstodisplay.get_rect()
            textstodisplayRect.center = (self.width // 2, self.height // 2)
            self.screen.blit(textstodisplay,textstodisplayRect)

            for event in pygame.event.get():
                if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                    running = False
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()

    def displayendingtext(self):
        text = "Game Over"
        textscore = "You scored: " + str(self.score) + " points!"

        text2 = "Press button to close"
        running = True
        self.screen.fill(self.white)
        pygame.display.update()
        while running:
            self.width, self.height = pygame.display.get_surface().get_size()
            textstodisplay = self.textfontnorm.render(text,True, self.black)
            textstodisplayRect = textstodisplay.get_rect()
            textstodisplayRect.center = (self.width // 2, self.height // 2)
            self.screen.blit(textstodisplay,textstodisplayRect)

            self.width, self.height = pygame.display.get_surface().get_size()
            textstodisplay = self.textfontnorm.render(textscore,True, self.black)
            textstodisplayRect = textstodisplay.get_rect()
            textstodisplayRect.center = (self.width // 2, self.height // 1.8)
            self.screen.blit(textstodisplay,textstodisplayRect)

            textstodisplay = self.textfontsmall.render(text2,True, self.black)
            textstodisplayRect = textstodisplay.get_rect()
            textstodisplayRect.center = (self.width // 2, self.height // 1.6)
            self.screen.blit(textstodisplay,textstodisplayRect)

            for event in pygame.event.get():
                if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                    return
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()

    def displaypausetext(self):
        running = True
        while running:
            text = "Paused"
            text2 = "Press button to close"
            self.width, self.height = pygame.display.get_surface().get_size()
            textstodisplay = self.textfontnorm.render(text,True, self.black)
            textstodisplayRect = textstodisplay.get_rect()
            textstodisplayRect.center = (self.width // 2, self.height // 2)
            self.screen.blit(textstodisplay,textstodisplayRect)

            textstodisplay = self.textfontsmall.render(text2,True, self.black)
            textstodisplayRect = textstodisplay.get_rect()
            textstodisplayRect.center = (self.width // 2, self.height // 1.8)
            self.screen.blit(textstodisplay,textstodisplayRect)
            for event in pygame.event.get():
                if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                    running = False
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()

    def getstartboard(self):
        board = []
        for i in range(self.boardheight):
            board.append([self.boardblank] * self.boardwidth)
        return board

    def getnewpuyo(self):
        colours= random.choice(self.puyocombinations)
        puyoblock = {"colours" : colours,
                    "rotation" : self.Puyo_movement_template[0], #[1,4]
                    "x1": int(self.boardwidth / 2) -1,
                    "y1": -1,
                    "x2": int(self.boardwidth / 2) -1,
                    "y2": 0
                    }
        return puyoblock

    def checkforquit(self):
        for event in pygame.event.get(pygame.QUIT):
                sys.exit()
        for event in pygame.event.get(pygame.KEYUP):
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            pygame.event.post(event)

    def drawBoard(self,pos = "Null"):
        if pos == "Null":
            self.updatescreensize()
            #pygame.draw.rect(self.screen, (94, 70, 94),(self.xmargin - (self.boardboxsize/2) - 4,self.ymargin - (self.boardboxsize/2)- 3,(self.boardwidth * self.boardboxsize) + 8, (self.boardheight * self.boardboxsize) + 5))
            pygame.draw.rect(self.screen, self.black,(self.xmargin - (self.boardboxsize/2) - 4,self.ymargin - (self.boardboxsize/2)- 3,(self.boardwidth * self.boardboxsize) + 8, (self.boardheight * self.boardboxsize) + 5),4)

            for y in range(self.boardheight):
                for x in range(self.boardwidth):
                    if self.board[y][x] != self.boardblank:
                            self.drawpuyo(y, x)
        elif pos == "P1":
            pygame.draw.rect(self.screen, self.black,((self.xmargin - (self.boardboxsize/2) - 4)/2,(self.ymargin - (self.boardboxsize/2)- 3),((self.boardwidth * self.boardboxsize) + 8), ((self.boardheight * self.boardboxsize) + 5)),4)

            for y in range(self.boardheight):
                for x in range(self.boardwidth):
                    if self.board[y][x] != self.boardblank:
                            self.drawpuyo(y, x,None,None,None,pos)

        elif pos == "P2":
            pygame.draw.rect(self.screen, self.black,((self.xmargin - (self.boardboxsize/2) - 4)/0.6,(self.ymargin - (self.boardboxsize/2)- 3),((self.boardwidth * self.boardboxsize) + 8), ((self.boardheight * self.boardboxsize) + 5)),4)

            for y in range(self.boardheight):
                for x in range(self.boardwidth):
                    if self.board[y][x] != self.boardblank:
                            self.drawpuyo(y, x,None,None,None,pos)

    def drawpuyo(self,y,x,pixely=None, pixelx=None,colour=None,pos="Null"):
        if pixely == None and pixelx == None:
            pixely, pixelx = self.coords_to_pixelyx(y, x,pos)
        if colour == None:
            colour = self.board[y][x]
        pygame.draw.circle(self.screen,colour, (pixelx, pixely),self.boardboxsize/2)
        pygame.draw.circle(self.screen,self.white, (pixelx - self.boardboxsize/5, pixely + self.boardboxsize/20),self.boardboxsize/5)
        pygame.draw.circle(self.screen,self.black, (pixelx - self.boardboxsize/5, pixely + self.boardboxsize/20),self.boardboxsize/5,1)
        pygame.draw.circle(self.screen,self.black, (pixelx - self.boardboxsize/5, pixely + self.boardboxsize/20),self.boardboxsize/7)


        pygame.draw.circle(self.screen,self.white, (pixelx + self.boardboxsize/5, pixely + self.boardboxsize/20),self.boardboxsize/5)
        pygame.draw.circle(self.screen,self.black, (pixelx + self.boardboxsize/5, pixely + self.boardboxsize/20),self.boardboxsize/5,1)
        pygame.draw.circle(self.screen,self.black, (pixelx + self.boardboxsize/5, pixely + self.boardboxsize/20),self.boardboxsize/7)


    def coords_to_pixelyx(self,y, x,pos):
        if pos == "Null":
            return (self.ymargin + (y * self.boardboxsize)), (self.xmargin + (x * self.boardboxsize))
        elif pos == "P1":
            return (self.ymargin + (y * self.boardboxsize)), (self.xmargin/1.875 + (x * self.boardboxsize))
        elif pos == "P2":
            return (self.ymargin + (y * self.boardboxsize)), (self.xmargin/0.615 + (x * self.boardboxsize))

    def drawnextpiece(self,pos = "Null"):
        if pos == "Null":
            self.drawpuyo(0,0, pixelx=self.width/1.5, pixely=self.height/10, colour=(self.nextpuyoblock["colours"][0]))
            self.drawpuyo(0,0, pixelx=self.width/1.5, pixely=(self.height/10 + (self.boardboxsize)), colour=(self.nextpuyoblock["colours"][1]))
        elif pos == "P1":
            self.drawpuyo(0,0, pixelx=self.width/10, pixely=self.height/10, colour=(self.nextpuyoblock["colours"][0]))
            self.drawpuyo(0,0, pixelx=self.width/10, pixely=(self.height/10 + (self.boardboxsize)), colour=(self.nextpuyoblock["colours"][1]))
        elif pos == "P2":
            self.drawpuyo(0,0, pixelx=self.width/1.1, pixely=self.height/10, colour=(self.nextpuyoblock["colours"][0]))
            self.drawpuyo(0,0, pixelx=self.width/1.1, pixely=(self.height/10 + (self.boardboxsize)), colour=(self.nextpuyoblock["colours"][1]))

    def drawcuurentpiece(self,pos="Null"):
            if pos == "Null":
                self.drawpuyo(self.currentpuyoblock["y1"],self.currentpuyoblock["x1"],None,None,(self.currentpuyoblock["colours"][0]))
                self.drawpuyo(self.currentpuyoblock["y2"],self.currentpuyoblock["x2"],None,None,(self.currentpuyoblock["colours"][1]))
            elif pos == "P1" or pos == "P2":
                self.drawpuyo(self.currentpuyoblock["y1"],self.currentpuyoblock["x1"],None,None,(self.currentpuyoblock["colours"][0]),pos)
                self.drawpuyo(self.currentpuyoblock["y2"],self.currentpuyoblock["x2"],None,None,(self.currentpuyoblock["colours"][1]),pos)

    def drawscore(self,pos="Null"):
        scoreren = self.textfontsmall.render('Score: %s' % self.score, True, self.black)
        scorerect = scoreren.get_rect()
        if pos == "Null":
            scorerect.topleft = (self.width/1.6, 20)
            self.screen.blit(scoreren, scorerect)
        elif pos == "P1":
            scorerect.topleft = (self.width/25, 20)
            self.screen.blit(scoreren, scorerect)
        elif pos == "P2":
            scorerect.topleft = (self.width/1.15, 20)
            self.screen.blit(scoreren, scorerect)


    def updatescreensize(self):
        
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.xmargin = int((self.width - self.boardwidth * self.boardboxsize) / 2)
        self.ymargin = self.height - (self.boardheight * self.boardboxsize) - 5
        if max(self.width,self.height) >= 2 * min(self.width,self.height):
            self.boardboxsize = min(self.width,self.height)/15
        else:
            self.boardboxsize = (max(self.width,self.height)/2)/12

    def currentpuyoblockcheck(self,boardQueue=[],blockQueue=[],AiFlag=False):
        if self.currentpuyoblock == None:
                self.currentpuyoblock = self.nextpuyoblock
                self.nextpuyoblock = self.getnewpuyo()

                if not self.isvalidmovement("down"):
                    return True
                self.currentpuyoblock["y1"]=0
                self.currentpuyoblock["y2"]=1
                self.justSpawnedFlag=True
                if AiFlag:
                    boardQueue.put(self.board)
                    blockQueue.put(self.currentpuyoblock)
                self.lastfalltime = time.time()
                self.lastMoveDownTime = time.time()

                #make the game end if no more valid position

                return False

    def held_down_movement(self):
        # holding down keys
        if (self.movingLeft or self.movingRight) and time.time() - self.lastMoveSidewaysTime > self.movesidewaysfreq:
            if self.isvalidmovement("left") and self.movingLeft:
                self.currentpuyoblock["x1"] -= 1
                self.currentpuyoblock["x2"] -= 1
            elif self.isvalidmovement("right") and self.movingRight:
                self.currentpuyoblock["x1"] += 1
                self.currentpuyoblock["x2"] += 1
            self.lastMoveSidewaysTime = time.time()
        
        if self.movingDown and time.time() - self.lastMoveDownTime > self.movedownfreq and self.isvalidmovement("down"):
            self.currentpuyoblock["y1"] = self.currentpuyoblock["y1"] + 1
            self.currentpuyoblock["y2"] = self.currentpuyoblock["y2"] + 1
            self.lastMoveDownTime = time.time()

    def naturalmovement(self,pos = "Null"):
        #pieces falling naturally and then if they cant the at bottom or connected so add to board 
        if time.time() - self.lastFallTime > self.fallfreq:
            if not self.isvalidmovement("down"):
                return self.scoreLines(pos)

                    
            else:

                if not self.justSpawnedFlag:
                    self.currentpuyoblock["y1"] += 1
                    self.currentpuyoblock["y2"] += 1

                else:
                    self.justSpawnedFlag=False
                self.lastFallTime = time.time()
        return 0
            
        
    def init_game_values(self):
        self.screen.fill(self.white)
        pygame.display.update()

        numpuyo_inchain = 0 #pc
        numchains = 0 #cp
        numcolour_inchain = 0 #cb
        numpuyo_ingroup_inchain_combined = 0 #gb

        self.lastMoveDownTime = time.time()
        self.lastMoveSidewaysTime = time.time()
        self.lastFallTime = time.time()
        self.movingDown = False
        self.movingLeft = False
        self.movingRight = False

        # Not sure if it gets faster over time for puyo puyo

        self.currentpuyoblock = self.getnewpuyo()
        self.nextpuyoblock = self.getnewpuyo()
        #Maybe add two lookahead
        self.currentpuyoblock["y1"] = 0
        self.currentpuyoblock["y2"] = 1

    def add_nusiance(self,amount):
        i = 0
        while i < amount:
            pos = random.randrange(6)
            self.placegrey(pos)
            i+=1

    def placegrey(self,pos):
        i = 0
        while (i+1) <= 11 and self.board[i+1][pos] == self.boardblank:
            i += 1
        self.board[i][pos] = self.grey

    def drawnus(self,pos,value):
        if pos == "P1":
            pygame.draw.circle(self.screen,self.grey,(self.width/6.5, self.height/1.1),self.boardboxsize/2)
            num = self.textfontnorm.render(str(value),True, self.black)
            numrect = num.get_rect()
            numrect.topleft = (self.width/6.7, self.height/1.12)
            self.screen.blit(num,numrect)
        if pos == "P2":
            pygame.draw.circle(self.screen,self.grey,(self.width/1.15, self.height/1.1),self.boardboxsize/2)
            num = self.textfontnorm.render(str(value),True, self.black)
            numrect = num.get_rect()
            numrect.topleft = (self.width/1.155, self.height/1.12)
            self.screen.blit(num,numrect)
        
