import random

class Player(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.path = []
        self.alive = True
    
    def randomMove(self):
    ## piece makes a single random move depending on it's current location
        ## on top cube
        if self.row == 6: 
            rowIncrement = random.choice([-1,0])
            self.row += rowIncrement
            if rowIncrement == 0:
                self.col += 0
            else:
                self.col += 1
        ## not on top cube 
        else: 
            ## on left edge
            if self.col == 0: 
                ## left-bottom corner special case
                if self.row == 0:
                    self.row += 1
                    self.col += 0
                else:
                    rowIncrement = random.choice([-1,1])
                    self.row += rowIncrement
                    if rowIncrement == 1:
                        self.col += 0
                    else:
                        self.col += random.choice([0,1])
            ## on right edge 
            elif self.onRightEdge(): 
                ## right-bottom corner special case
                if self.row == 0:
                    self.row += 1
                    self.col -= 1
                else:
                    rowIncrement = random.choice([-1,1])
                    self.row += rowIncrement
                    if rowIncrement == 1:
                        self.col -= 1
                    else:
                        self.col += random.choice([0,1])
            ## not on left or right edge
            elif not self.onRightEdge() and self.col != 0: 
                ## bottom row except corners
                if self.row == 0:
                    self.row += 1
                    self.col += random.choice([-1,0])
                ## middle of pyramid
                else:
                    rowIncrement = random.choice([-1,1])
                    self.row += rowIncrement
                    if rowIncrement == 1:
                        self.col += random.choice([-1,0])
                    else:
                        self.col += random.choice([0,1])
        
    def followMove(self, other):
    ## updates others row and col with legal move that gets it closer to self
        print("snake is located at== ", (other.row, other.col))
        print("qbert is located at==", (self.row, self.col))
        ## self is above
        if self.row > other.row:
            other.row += 1

            ## self is to the left
            if self.col < other.col:
                other.col -= 1
            ## self is to the right
            else:
                other.col += 0

        ## self is below
        elif self.row < other.row:
            other.row -= 1

            ## self is to the left
            if self.col < other.col:
                other.col += 0
            ## self is to the right
            else:
                other.col += random.choice([0,1])

        ## self and other on same row
        else:
            ## self and other on bottom row
            if self.row == 0:
                other.row += 1
                ## self is to the left
                if self.col < other.col:
                    other.col -= 1
                ## self is to the right
                elif self.col > other.col:
                    other.col += 0
                ## same cube but not on corners
                elif self.col == other.col and self.col != 6 and self.col != 0:
                    other.col += random.choice([0,1])
                ## same cube but on corner
                elif self.col == other.col and self.col == 6:
                    other.col -= 1
                elif self.col == other.col and self.col == 0:
                    other.col += 0            
            ## self and other not on bottom row
            else:
                rowIncrement = random.choice([-1,1])
                other.row += rowIncrement

                ## self is to the left
                if self.col < other.col:
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