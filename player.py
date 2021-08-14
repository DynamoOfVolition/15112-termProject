import random
from cmu_112_graphics import *

class Player(object):
    
    @staticmethod
    def cubicBezier(t, p0, p1, p2):
    ## Bezier curve function and code adapted from 
    ## https://towardsdatascience.com/bézier-curve-bfffdadea212

    ## returns a point along a cubic bezier curve 
        px = (1-t)**2*p0[0] + 2*t*(1-t)*p1[0] + t**2*p2[0]
        py = (1-t)**2*p0[1] + 2*t*(1-t)*p1[1] + t**2*p2[1]
        return (px, py)

    @staticmethod
    def distance(x0,y0,x1,y1):
        return ((x0-x1)**2 + (y0-y1)**2)**0.5
    
    @staticmethod
    def findMaxDir(directionCnt):
        maxDir = ''
        maxLen = 0
        currLen = 0

        for key in directionCnt:
            currLen = directionCnt[key]
            if currLen > maxLen:
                maxLen = currLen
                maxDir = key
        return maxDir  

    @staticmethod
    def generateCubeList(row, col, direction):
    ## takes location of player and a direction (UR, UL, LR, LL) and 
    ## returns set of (row, col) along that direction
    ## not dependent on enemies or qberts path, only returns information about 
    ## the board itself
        l = []
        if direction == 'LL':
            if row != 0:
                for i in range(0, row):
                    l.append((i, col))
            else:
                return None
        elif direction == 'UR':
            if row != 6:
                for i in range(row+1, 7-col):
                    l.append((i, col))
            else:
                return None
        elif direction == 'LR':
            if row != 0:
                for i in range(row-1, -1, -1):
                        l.append((i, row+col-i))
            else:
                return None
        elif direction == 'UL':
            if row != 6:
                for i in range(row+1, row+ col+1):
                    l.append((i,row+col-i))
            else:
                return None
        return l
    
    def __init__(self, name, rowStart, colStart, rowStop, colStop):
        self.name = name
        self.rowStart = rowStart
        self.colStart = colStart
        self.rowStop = rowStop
        self.colStop = colStop
        self.path = []
        self.rad = 0
        self.autoPlay = False
        self.color = ''
        self.alive = True
        self.drawCount = 1
        self.moveStart = False
        l = [n / 100.0 for n in range(0,101,10)]
        self.bezierIncrements = {}
        for i in l:   
            self.bezierIncrements[int(i*10+1)] = l[int(i*10)]

    def __repr__(self):
        return f'{self.name}'

    def randomMove(self, other, app):
    ## piece makes a single random move depending on it's current location
        ## on top cube
        if self.rowStart== 6: 
            rowIncrement = random.choice([-1,0])
            self.rowStop = self.rowStart + rowIncrement
            if rowIncrement == 0:
                self.colStop = self.colStart
            else:
                self.colStop = self.colStart + 1
        ## not on top cube 
        else: 
            ## on left edge
            if self.colStart== 0: 
                ## left-bottom corner special case
                if self.rowStart== 0:
                    self.rowStop = self.rowStart + 1
                    self.colStop = self.colStart
                else:
                    rowIncrement = random.choice([-1,1])
                    self.rowStop = self.rowStart + rowIncrement
                    if rowIncrement == 1:
                        self.colStop = self.colStart
                    else:
                        self.colStop = self.colStart + random.choice([0,1])
            ## on right edge 
            elif self.onRightEdge(): 
                ## right-bottom corner special case 
                if self.rowStart== 0:
                    self.rowStop = self.rowStart + 1
                    self.colStop = self.colStart - 1
                else:
                    rowIncrement = random.choice([-1,1])
                    self.rowStop = self.rowStart + rowIncrement
                    if rowIncrement == 1:
                        self.colStop = self.colStart - 1
                    else:
                        self.colStop = self.colStart + random.choice([0,1])

            ## not on left or right edge
            elif not self.onRightEdge() and self.colStart!= 0: 
                ## bottom row except corners
                if self.rowStart== 0:
                    self.rowStop = self.rowStart + 1
                    self.colStop = self.colStart + random.choice([-1,0])

                ## middle of pyramid
                else:
                    rowIncrement = random.choice([-1,1])
                    self.rowStop = self.rowStart + rowIncrement

                    if rowIncrement == 1:
                        self.colStop = self.colStart + random.choice([-1,0])
                    else:
                        self.colStop = self.colStart + random.choice([0,1])
        self.moveStart = False

        ## test for collision
        if (self.isCollision(other)):
            app.score -=10

    def followMove(self, other, app):
    ## self follows other
    ## usage would be: app.snake.followMove(self)
    ## updates others row and col with legal move that gets it closer to self
        # print("snake is located at== ", (self.rowStart, self.colStart))
        # print("qbert is located at==", (other.rowStart, other.colStart))

        self.moveStart = True

        ## other is above
        if other.rowStart > self.rowStart:
            self.rowStop = self.rowStart + 1

            ## other is to the left
            if other.colStart < self.colStart:
                self.colStop = self.colStart - 1
            ## other is to the right
            else:
                self.colStop = self.colStart

        ## other is below
        elif other.rowStart < self.rowStart:
            self.rowStop = self.rowStart - 1

            ## other is to the left
            if other.colStart< self.colStart:
                self.colStop = self.colStart
                
            ## other is to the right
            else:
                self.colStop = self.colStart + 1

        ## self and other on same row
        else:
            ## self and other on bottom row
            if other.rowStart== 0:
                self.rowStop = self.rowStart + 1

                ## other is to the left
                if other.colStart < self.colStart:
                    self.colStop = self.colStart - 1

                ## other is to the right
                elif other.colStart > self.colStart: # OK
                    self.colStop = self.colStart

                ## same cube but not on corners
                elif (other.colStart == self.colStart and 
                     other.colStart!= 6 and other.colStart!= 0):
                    self.colStop = self.colStart + random.choice([-1,0]) # OK

                ## same cube but on corner
                elif other.colStart== self.colStart and other.colStart== 6: # OK
                    self.colStop = self.colStart - 1

                elif other.colStart== self.colStart and other.colStart== 0: # OK
                    self.colStop = self.colStart   

            ## self and other on top row (cube)
            elif self.rowStart == other.rowStart == 6: # OK
                self.rowStop = self.rowStart - 1
                colIncrement = random.choice([0,1])
                self.colStop = self.colStart + colIncrement

            ## self and other on same row, not on bottom or top cube
            else:
                rowIncrement = random.choice([-1,1])
                self.rowStop = self.rowStart + rowIncrement # OK

                ## other is to the left
                if other.colStart < self.colStart: # OK
                    if rowIncrement == -1:
                        self.colStop = self.colStart + random.choice([0,1])
                    else:
                        self.colStop = self.colStart - 1

                ## other is to the right
                elif other.colStart > self.colStart: # OK
                    if rowIncrement == -1:
                        self.colStop = self.colStart + 1
                    else:
                        self.colStop = self.colStart

                ## on same row and column (on same cube actually)
                elif other.colStart == self.colStart:
                    ## on left edge
                    if other.colStart == 0:
                        if rowIncrement == -1:
                            self.colStop = self.colStart + random.choice([0,1])
                        else:
                            self.colStop = self.colStart 
                    ## on right edge
                    elif self.onRightEdge():
                        if rowIncrement == -1:
                            self.colStop = self.colStart + random.choice([0,1])
                        else:
                            self.colStop = self.colStart - 1
                    else:
                        ## not on left or right edge
                        if rowIncrement == -1:
                            self.colStop = self.colStart + random.choice([0,1])
                        else:
                            self.colStop = self.colStart + random.choice([-1,0])
        
        ## test for collision
        if (self.isCollision(other)):
            app.score -=10

    def onRightEdge(self):
        onRightEdge = ((self.rowStart== 6 and self.colStart== 0) or
                       (self.rowStart== 5 and self.colStart== 1) or
                       (self.rowStart== 4 and self.colStart== 2) or
                       (self.rowStart== 3 and self.colStart== 3) or
                       (self.rowStart== 2 and self.colStart== 4) or
                       (self.rowStart== 1 and self.colStart== 5) or
                       (self.rowStart== 0 and self.colStart== 6))
        return onRightEdge

    def isCollision(self, other):
    ## checks for collision (same row col location)
        return ((self.rowStop, self.colStop) == (other.rowStop, other.colStop))

    def bounceIteration(self, other, app):
    ## performs one iteration along the path from start to stop location
        if (self.drawCount == 1):  
                self.drawCount += 1   
                if self.name == 'redEnemy' or self.name == 'greenEnemy':
                    self.randomMove(other, app) 
                elif self.name == 'snake':
                    self.followMove(other, app)
                else:
                    self.autoplay(other, app)

        elif self.drawCount > 1 and self.drawCount < 11:
            self.drawCount += 1
        else:
            self.drawCount = 1
            self.rowStart = self.rowStop
            self.colStart = self.colStop
    
    
    
    def getDirection(self, app):
    ## in the case where there are no untouched cubes along any legal direction,
    ## increment row,col along direction with closest untouched cube

        ## loop through all cubes and find untouched cube with lowest distance
        ## increment row,col along that direction
        ## app.cubeTopMapping --> app.cubeTopMapping[(row,col)] = (cx, cy)

        curDist = 0
        bestDist = 0
        bestRC = ()
        curRC = ()

        for row in range(0,7):
            for col in range(0,7-row):
                if (row,col) in self.path:
                    pass



    def autoplay(self, other, app):
    ## update qberts location (rowStop, colStop) based on path 
    ## in general, want to move along path with most untouched squares 
        nLR = nLL = 0    
        dirCnt = {}  #dirCnt[direction] = count (num untouched cubes along dir )
        row = self.rowStart
        col = self.colStart
        qbertPath = set(self.path)
    
        ## 0 find set of all untouched cubes
        #openCubes = app.allCubes.difference(set(self.path))

        ## 1. find direction with most untouched cubes 
        ## look in each direction and count number of untouched squares

        ## qbert on left side:
        if self.colStart == 0:
            ## left bottom corner cube (hard-coded as only one choice to move)
            if self.rowStart == 0:
                self.rowStop = 1
                self.colStop = 0
            ## top cube  - row hardcoded, column chosen by best path 
            ## can't get stuck on top cube bc there is randomness 
            elif self.rowStart == 6:
                self.rowStop = 5
                ## if first move, pick colStop at random
                if len(self.path) == 0:
                    print ("here!")
                    inc = random.choice([0,1])
                    print("increment = ", inc)
                    self.colStop = col + inc
                ## if not first move, pick based on best path
                else:
                    cubesLL = Player.generateCubeList(6,0,'LL')
                    cubesLR = Player.generateCubeList(6,0,'LR')
                    nLL = len(cubesLL) - len(qbertPath.intersection(set(cubesLL)))
                    nLR = len(cubesLR) - len(qbertPath.intersection(set(cubesLR)))
                    if nLL > nLR:
                        self.colStop = 0
                    elif nLL < nLR:
                        self.colStop = 1
                    else:
                        self.colStop = col + random.choice([0,1])
            ## on left side, not top or bottom cube - DONE
            else:
                cubesLL = Player.generateCubeList(row, col, 'LL')
                cubesUR = Player.generateCubeList(row, col, 'UR')
                cubesLR = Player.generateCubeList(row, col, 'LR')
                dirCnt['LL'] = len(cubesLL) - \
                            len(qbertPath.intersection(set(cubesLL)))
                dirCnt['UR'] = len(cubesUR) - \
                            len(qbertPath.intersection(set(cubesUR)))
                dirCnt['LR'] = len(cubesLR) - \
                            len(qbertPath.intersection(set(cubesLR)))
                ## if there are no untouched cubes along legal directions
                if not any(v > 0 for v in iter(dirCnt.values())):
                    self.getDirection(app)
                ## else get direction with most untouched cubes, if tie, random
                else:
                    maxDir = Player.findMaxDir(dirCnt)
                    if maxDir == 'LL':
                        self.rowStop = self.rowStart - 1
                        self.colStop = self.colStart
                    elif maxDir == 'UR':
                        self.rowStop = self.rowStart + 1
                        self.colStop = self.colStart
                    elif maxDir == 'LR':
                        self.rowStop = self.rowStart - 1
                        self.colStop = self.colStart + 1
        ## qbert on right side
        elif self.onRightEdge():
            ## right bottom corner cube - DONE
            if self.rowStart == 0:
                self.rowStop = 1
                self.colStop = self.colStart - 1
            ## on right side, not top or bottom cube
            else:
                cubesLL = Player.generateCubeList(row, col, 'LL')
                cubesUL = Player.generateCubeList(row, col, 'UL')
                cubesLR = Player.generateCubeList(row, col, 'LR')
                dirCnt['LL'] = len(cubesLL) - \
                            len(qbertPath.intersection(set(cubesLL)))
                dirCnt['UL'] = len(cubesUL) - \
                            len(qbertPath.intersection(set(cubesUL)))
                dirCnt['LR'] = len(cubesLR) - \
                            len(qbertPath.intersection(set(cubesLR)))
                maxDir =Player.findMaxDir(dirCnt)
                if maxDir == 'LL':
                    self.rowStop = self.rowStart - 1
                    self.colStop = self.colStart
                elif maxDir == 'UL':
                    self.rowStop = self.rowStart + 1
                    self.colStop = self.colStart - 1
                elif maxDir == 'LR':
                    self.rowStop = self.rowStart - 1
                    self.colStop = self.colStart + 1
        ## bottom row
        elif self.rowStart == 0:
            cubesUL = Player.generateCubeList(row, col, 'UL')
            cubesUR = Player.generateCubeList(row, col, 'UR')
            dirCnt['UL'] = len(cubesUL) - \
                        len(qbertPath.intersection(set(cubesUL)))
            dirCnt['UR'] = len(cubesUR) - \
                        len(qbertPath.intersection(set(cubesUR)))
            maxDir =Player.findMaxDir(dirCnt)
            if maxDir == 'UL':
                    self.rowStop = self.rowStart + 1
                    self.colStop = self.colStart - 1
            elif maxDir == 'UR':
                    self.rowStop = self.rowStart + 1
                    self.colStop = self.colStart 
        ## interior
        else:
            cubesLL = Player.generateCubeList(row, col, 'LL')
            cubesUL = Player.generateCubeList(row, col, 'UL')
            cubesLR = Player.generateCubeList(row, col, 'LR')
            cubesUR = Player.generateCubeList(row, col, 'UR')
            dirCnt['LL'] = len(cubesLL) - \
                        len(qbertPath.intersection(set(cubesLL)))
            dirCnt['UL'] = len(cubesUL) - \
                        len(qbertPath.intersection(set(cubesUL)))
            dirCnt['LR'] = len(cubesLR) - \
                        len(qbertPath.intersection(set(cubesLR)))
            dirCnt['UR'] = len(cubesUR) - \
                        len(qbertPath.intersection(set(cubesUR)))
            maxDir =Player.findMaxDir(dirCnt)
            if maxDir == 'LL':
                self.rowStop = self.rowStart - 1
                self.colStop = self.colStart
            elif maxDir == 'UL':
                self.rowStop = self.rowStart + 1
                self.colStop = self.colStart - 1
            elif maxDir == 'LR':
                self.rowStop = self.rowStart - 1
                self.colStop = self.colStart + 1
            elif maxDir == 'UR':
                self.rowStop = self.rowStart + 1
                self.colStop = self.colStart 
    
        ## 4. if nothing along any direction, identify closest open 
        ## square and go to it
            #self.closestOpen()

        ## increment score 
        if (self.rowStop, self.colStop) not in self.path:
            app.score += 50

        ## check for collision
        ## test for collision
        if (self.isCollision(other)):
            app.score -=10

        ## add location to path
        # if ((self.rowStop, self.colStop) != 
        #     (self.rowStart, self.colStart) and
        #     (self.rowStop, self.colStop) not in self.path):
        #     self.path.append((self.rowStop, self.colStop))   
        # print("start: ", (self.rowStart, self.colStart)) 
        # print("stop: ", (self.rowStop, self.colStop)) 
        # print(self.path)

  
    def drawPlayer(self, app, canvas):
        r = self.rad
        xStart, yStart = app.cubeTopMapping[(self.rowStart, 
                                             self.colStart)]
        xStop, yStop = app.cubeTopMapping[(self.rowStop, 
                                           self.colStop)]

        ## control point depends on if traveling up or down a row
        if yStart < yStop:
            xIntm, yIntm = (xStop, yStart)
        else:
            xIntm, yIntm = (xStart, yStop)

        p0 = (xStart, yStart)
        p1 = (xIntm, yIntm)
        p2 = (xStop, yStop)
        t = self.bezierIncrements[self.drawCount]

        if ((self.name == 'qbert' and self.moveStart) or 
            (self.name == 'qbert' and not self.moveStart and self.autoPlay) or
            self.name == 'redEnemy' or self.name == 'greenEnemy' or
            self.name == 'snake'):
            (x, y) = Player.cubicBezier(t, p0, p1, p2)
        else:
            (x, y) = p2 

        canvas.create_oval(x-r, y-r, x+r, y+r, fill = self.color, width = 0)
