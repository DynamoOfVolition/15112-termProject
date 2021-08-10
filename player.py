import random

class Player(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.path = []
        self.alive = True
    
    def randomMove(self):
    ## piece makes a single random move depending on it's current location
        ## if on bottom row, (jump off screen and) appear in new random spot OK
        if self.row == 0: # case 1
            randRow = random.randint(3,5)
            randCol = random.randint(0,6-randRow)
            self.row = randRow
            self.col = randCol
        ## else not on bottom row
        else:
            ## not on bottom row, on top cube: OK
            if self.row == 6: # case 2
                rowIncrement = random.choice([-1,0])
                self.row += rowIncrement
                if rowIncrement == 0:
                    self.col += 0
                else:
                    self.col += 1
            ## not on bottom row, not on top cube 
            else: 
                ## not on bottom row, not on top cube, on left edge
                if self.col == 0: # case 3
                    rowIncrement = random.choice([-1,1])
                    self.row += rowIncrement
                    if rowIncrement == 1:
                        self.col += 0
                    else:
                        self.col += random.choice([0,1])
                ## not on bottom row, not on top cube, on right edge 
                elif self.onRightEdge(): # case 4
                    rowIncrement = random.choice([-1,1])
                    self.row += rowIncrement
                    if rowIncrement == 1:
                        self.col -= 1
                    else:
                        self.col += random.choice([0,1])
                ## not on bottom row, not on top cube, not on left or right edge
                elif not self.onRightEdge() and self.col != 0: # case 5
                    rowIncrement = random.choice([-1,1])
                    self.row += rowIncrement
                    if rowIncrement == 1:
                        self.col += random.choice([-1,0])
                    else:
                        self.col += random.choice([0,1])
        
    def onRightEdge(self):
        onRightEdge = ((self.row == 6 and self.col == 0) or
                       (self.row == 5 and self.col == 1) or
                       (self.row == 4 and self.col == 2) or
                       (self.row == 3 and self.col == 3) or
                       (self.row == 2 and self.col == 4) or
                       (self.row == 1 and self.col == 5) or
                       (self.row == 0 and self.col == 6))
        return onRightEdge

    def isCollision(self, other):
        return ((self.row, self.col) == (other.row, other.col))