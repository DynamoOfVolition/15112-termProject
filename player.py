import random

class Player(object):
    def __init__(self, rowStart, colStart, rowStop, colStop, cx, cy):
        self.rowStart = rowStart
        self.colStart = colStart
        self.rowStop = rowStop
        self.colStop = colStop
        self.cx = cx
        self.cy = cy
        self.path = []
        self.alive = True
        self.drawCount = 1
        self.moveStart = False
        l = [n / 100.0 for n in range(0, 101, 10)]
        self.bezierIncrements = {}
        for i in l:   
            self.bezierIncrements[int(i*10+1)] = l[int(i*10)]

         
    
    def randomMove(self):
    ## piece makes a single random move depending on it's current location
        ## on top cube
        if self.rowStart== 6: 
            rowIncrement = random.choice([-1,0])
            self.rowStart+= rowIncrement
            if rowIncrement == 0:
                self.colStart+= 0
            else:
                self.colStart+= 1
        ## not on top cube 
        else: 
            ## on left edge
            if self.colStart== 0: 
                ## left-bottom corner special case
                if self.rowStart== 0:
                    self.rowStart+= 1
                    self.colStart+= 0
                else:
                    rowIncrement = random.choice([-1,1])
                    self.rowStart+= rowIncrement
                    if rowIncrement == 1:
                        self.colStart+= 0
                    else:
                        self.colStart+= random.choice([0,1])
            ## on right edge 
            elif self.onRightEdge(): 
                ## right-bottom corner special case
                if self.rowStart== 0:
                    self.rowStart+= 1
                    self.colStart-= 1
                else:
                    rowIncrement = random.choice([-1,1])
                    self.rowStart+= rowIncrement
                    if rowIncrement == 1:
                        self.colStart-= 1
                    else:
                        self.colStart+= random.choice([0,1])
            ## not on left or right edge
            elif not self.onRightEdge() and self.colStart!= 0: 
                ## bottom row except corners
                if self.rowStart== 0:
                    self.rowStart+= 1
                    self.colStart+= random.choice([-1,0])
                ## middle of pyramid
                else:
                    rowIncrement = random.choice([-1,1])
                    self.rowStart+= rowIncrement
                    if rowIncrement == 1:
                        self.colStart+= random.choice([-1,0])
                    else:
                        self.colStart+= random.choice([0,1])
        
    def followMove(self, other):
    ## updates others row and col with legal move that gets it closer to self
        #print("snake is located at== ", (other.row, other.col))
        #print("qbert is located at==", (self.row, self.col))
        ## self is above
        if self.rowStart > other.row:
            other.row += 1

            ## self is to the left
            if self.colStart< other.col:
                other.col -= 1
            ## self is to the right
            else:
                other.col += 0

        ## self is below
        elif self.rowStart< other.row:
            other.row -= 1

            ## self is to the left
            if self.colStart< other.col:
                other.col += 0
            ## self is to the right
            else:
                other.col += random.choice([0,1])

        ## self and other on same row
        else:
            ## self and other on bottom row
            if self.rowStart== 0:
                other.row += 1
                ## self is to the left
                if self.colStart< other.col:
                    other.col -= 1
                ## self is to the right
                elif self.colStart> other.col:
                    other.col += 0
                ## same cube but not on corners
                elif self.colStart== other.col and self.colStart!= 6 and self.colStart!= 0:
                    other.col += random.choice([0,1])
                ## same cube but on corner
                elif self.colStart== other.col and self.colStart== 6:
                    other.col -= 1
                elif self.colStart== other.col and self.colStart== 0:
                    other.col += 0            
            ## self and other not on bottom row
            else:
                rowIncrement = random.choice([-1,1])
                other.row += rowIncrement

                ## self is to the left
                if self.colStart< other.col:
                    if rowIncrement == -1:
                        other.col += 0
                    else:
                        other.col -= 1

                ## self is to the right
                else:
                    if rowIncrement == -1:
                        other.col += 1
                    else:
                        other.col += 0


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