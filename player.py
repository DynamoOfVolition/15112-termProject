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

    def __init__(self, name, rowStart, colStart, rowStop, colStop):
        self.name = name
        self.rowStart = rowStart
        self.colStart = colStart
        self.rowStop = rowStop
        self.colStop = colStop
        self.path = []
        self.rad = 0
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

    def randomMove(self):
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

    def followMove(self, other):
    ## self follows other
    ## usage would be: app.snake.followMove(app.qbert)
    ## updates others row and col with legal move that gets it closer to self
        # print("snake is located at== ", (self.rowStart, self.colStart))
        # print("qbert is located at==", (other.rowStart, other.colStart))

        self.moveStart = True

        ## other is above
        if other.rowStart > self.rowStart:
            #self.row += 1
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
        return ((self.rowStop, self.colStop) == (other.rowStop, other.colStop))

    def bounceIteration(self, other):
    ## other is only necessary for call to followMove
    ## self is enemy, other is qbert
        if (self.drawCount == 1):  
                self.drawCount += 1   
                if self.name != 'snake':
                    self.randomMove() 
                else:
                    self.followMove(other)
        elif self.drawCount > 1 and self.drawCount < 11:
            self.drawCount += 1
        else:
            self.drawCount = 1
            self.rowStart = self.rowStop
            self.colStart = self.colStop

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
            self.name == 'redEnemy' or self.name == 'greenEnemy' or
            self.name == 'snake'):
            (x, y) = Player.cubicBezier(t, p0, p1, p2)
        else:
            (x, y) = p2 

        canvas.create_oval(x-r, y-r, x+r, y+r, fill = self.color, width = 0)
