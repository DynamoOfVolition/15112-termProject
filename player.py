import random
from cmu_112_graphics import *

class Player(object):
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
    ## updates others row and col with legal move that gets it closer to self
        # print("snake is located at== ", (other.rowStart, other.colStart))
        # print("qbert is located at==", (self.rowStart, self.colStart))

        other.moveStart = True

        ## self is above
        if self.rowStart > other.rowStart:
            #other.row += 1
            other.rowStop = other.rowStart + 1

            ## self is to the left
            if self.colStart < other.colStart:
                #other.col -= 1
                other.colStop = other.colStart - 1
            ## self is to the right
            else:
                #other.col += 0
                other.colStop = other.colStart

        ## self is below
        elif self.rowStart < other.rowStart:
            #other.row -= 1
            other.rowStop = other.rowStart - 1

            ## self is to the left
            if self.colStart< other.colStart:
                #other.col += 0
                other.colStop = other.colStart
                
            ## self is to the right
            else:
                #other.col += random.choice([0,1])
                other.colStop = other.colStart + random.choice([0,1])

        ## self and other on same row
        else:
            ## self and other on bottom row
            if self.rowStart== 0:
                #other.row += 1
                other.rowStop = other.rowStart + 1
                ## self is to the left
                if self.colStart< other.colStart:
                    #other.col -= 1
                    other.colStop = other.colStart - 1
                ## self is to the right
                elif self.colStart> other.colStart:
                    #other.col += 0
                    other.colStop = other.colStart
                ## same cube but not on corners
                elif (self.colStart== other.colStart and 
                     self.colStart!= 6 and self.colStart!= 0):
                    other.colStop = other.colStart + random.choice([0,1])
                ## same cube but on corner
                elif self.colStart== other.colStart and self.colStart== 6:
                    #other.col -= 1
                    other.colStop = other.colStart - 1
                elif self.colStart== other.colStart and self.colStart== 0:
                    #other.col += 0 
                    other.colStop = other.colStart   

            ## self and other on top cube
            elif other.rowStart == self.rowStart == 6:
                other.rowStop = other.rowStart - 1
                colIncrement = random.choice([0,1])
                other.colStop = other.colStart + colIncrement

            ## self and other not on bottom or top cube
            else:
                rowIncrement = random.choice([-1,1])
                #other.row += rowIncrement
                other.rowStop = other.rowStart + random.choice([-1,1])
                ## self is to the left
                if self.colStart< other.colStart:
                    if rowIncrement == -1:
                        #other.col += 0
                        other.colStop = other.colStart
                    else:
                        #other.col -= 1
                        other.colStop = other.colStart - 1

                ## self is to the right
                else:
                    if rowIncrement == -1:
                        #other.col += 1
                        other.colStop = other.colStart + 1
                    else:
                        #other.col += 0
                        other.colStop = other.colStart


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

    def bounceIteration(self):
        if (self.drawCount == 1):  
                self.drawCount += 1   
                self.randomMove()      
        elif self.drawCount > 1 and self.drawCount < 11:
            self.drawCount += 1
        else:
            self.drawCount = 1
            self.rowStart = self.rowStop
            self.colStart = self.colStop

    @staticmethod
    def cubicBezier(t, p0, p1, p2):
    ## Bezier curve function and code adapted from 
    ## https://towardsdatascience.com/bézier-curve-bfffdadea212

    ## returns a point along a cubic bezier curve 
        px = (1-t)**2*p0[0] + 2*t*(1-t)*p1[0] + t**2*p2[0]
        py = (1-t)**2*p0[1] + 2*t*(1-t)*p1[1] + t**2*p2[1]
        return (px, py)

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
            self.name == 'redEnemy' or self.name == 'greenEnemy'):
            (x, y) = Player.cubicBezier(t, p0, p1, p2)
        else:
            (x, y) = p2 

        canvas.create_oval(x-r, y-r, x+r, y+r, fill = self.color, width = 0)
