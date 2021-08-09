from cmu_112_graphics import *
import random

class Player(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.path = []
    
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

def setTopColor(app, row, col):
## returns the color of the top of the cube located at row, col
## colors depends on round and level
    if app.level == 1:
        if app.round == 1:
            if (row, col) in app.qbert.path:
                return('yellow')
            else:
                return(app.defaultTopColor)

def createCubeTopDict(app):
## creates a dict mapping cube row, column location to top center point of cube
## (row, col) --> (cx, cy).  
## Used for locating game players.
    cubeTopDict = dict()
    for row in range(0,7):
        for col in range(0,7-row):
            cx = 0.26*app.width + 0.08*app.width*col + 0.04*app.height*row
            cy = 0.65*app.height - 0.06*app.height*row - app.cubHt/2
            if (row,col) not in cubeTopDict:
                cubeTopDict[(row,col)] = []
            cubeTopDict[(row,col)] = (cx,cy)
    return cubeTopDict 
    
def appStarted(app):
    app.timerDelay = 800

    app.pauseGame = False
    ## score 
    app.score = 0
    app.level = 1
    app.round = 1
    ## cube 
    app.defaultTopColor = 'RoyalBlue3'
    app
    app.cubWd = app.width//12
    app.cubHt = app.height//12
    app.cubeTopMapping = createCubeTopDict(app)
    ## ... coords of top corner of top cube surface
    # cx = app.width//2
    # cy = app.height//2 - 3*app.cubHt

    ## create qbert instance and initialize path attribute
    app.qbert = Player(6, 0)
    app.qbert.path.append((6,0))

    ## create red Blob instance, initialize starting location 
    ## in random location in top chunk of board
    randRow = random.randint(1,5)
    randCol = random.randint(0,6-randRow)
    app.redEnemy = Player(randRow, randCol)
    app.redEnemy.path.append((randRow, randCol))


def updateScore(app):
    if (app.qbert.row, app.qbert.col) not in app.qbert.path:
        app.score += 25

def keyPressed(app, event):
## recall app.cubeTopDict[(row,col)] = (cx,cy)
## update app.qbert.row and app.qbert.col
    previousRow = app.qbert.row
    previousCol = app.qbert.col
    if event.key == 'p':
        app.pauseGame = not app.pauseGame
    if not app.pauseGame:
        if event.key == 'i':
            if not app.qbert.onRightEdge():
                app.qbert.row += 1
                updateScore(app)
        elif event.key == 'u':
            if app.qbert.col != 0:
                app.qbert.row += 1
                app.qbert.col -= 1
                updateScore(app)
        elif event.key == 'j':
            if app.qbert.row > 0:
                app.qbert.row -= 1
                app.qbert.col += 1
                updateScore(app)
        elif event.key == 'h':
            if app.qbert.row > 0:
                app.qbert.row -= 1
                updateScore(app)
        ## store cube top that qbert has touched - make sure not to double count
        ## current cube if qbert is trying to make illegal move
        if (app.qbert.row, app.qbert.col) != (previousRow, previousCol):
            app.qbert.path.append((app.qbert.row, app.qbert.col))
        #print(app.qbert.path)

def timerFired(app):
    if not app.pauseGame:
        app.redEnemy.randomMove()

def drawBackground(app, canvas):
## draw backsplash including score, level and round
    dy = app.height//28
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    canvas.create_text(app.width//8, app.height//10, 
                       text = f'Score {app.score}', 
                       fill = 'violet red', 
                       font = 'Helvetica 20 bold')
    canvas.create_text(app.width - app.width//8, app.height//8, 
                       text = f'Level: {app.level}', 
                       fill = 'green',
                       font = 'Helvetica 18 bold',
                       anchor = 'e')
    canvas.create_text(app.width - app.width//8, app.height//8 + dy , 
                       text = f'Round: {app.round}',
                       #fill = 'HotPink1',
                       fill = 'DeepPink2',
                       font = 'Helvetica 18 bold',
                       anchor = 'e')

def drawCube(app, canvas, cx, cy, row, col):
## draw a single cube centered at the point (cx,cy):
## each cube consists of 3 polygons, based on 7 total points:
    pt1X = cx - app.cubWd/2
    pt1Y = cy - app.cubHt/4
    pt2X = cx
    pt2Y = cy - app.cubHt/2
    pt3X = cx + app.cubWd/2
    pt3Y = pt1Y
    pt4X = cx
    pt4Y = cy
    pt5X = pt4X
    pt5Y = pt4Y + app.cubHt/2
    pt6X = pt1X
    pt6Y = pt1Y + app.cubHt/2
    pt7X = pt3X
    pt7Y = pt6Y

    topColor = setTopColor(app, row, col)

    ## top
    canvas.create_polygon(pt1X, pt1Y, pt2X, pt2Y, pt3X, pt3Y, pt4X, pt4Y,
                          fill = topColor)
    ## left side
    canvas.create_polygon(pt1X, pt1Y, pt4X, pt4Y, pt5X, pt5Y, pt6X, pt6Y,
                          fill = 'SeaGreen3')
    ## right side
    canvas.create_polygon(pt4X, pt4Y, pt3X, pt3Y, pt7X, pt7Y, pt5X, pt5Y,
                          fill = 'PaleGreen4')
    ## label row, col for debugging
    canvas.create_text(pt4X + app.cubWd/4, pt4Y, text = f'({row}, {col})')

def drawPyramid(app, canvas):
## draw pyramid of cubes starting from bottom row and working up
## double for-loop structure and cx, cy positioning adapted from:
## https://github.com/Wireframe-Magazine/Wireframe-42/blob/master/source-code-qbert/qbert.py
 
    for row in range(0, 7):
        for col in range(0,7-row):
            cx = 0.26*app.width + 0.08*app.width*col + 0.04*app.height*row
            cy = 0.65*app.height - 0.06*app.height*row
            drawCube(app, canvas, cx, cy, row, col)

def drawQbert(app, canvas):
    ## draw just one
    # app.cubeTopDict[(row,col)] = (cx,cy)
    x, y = app.cubeTopMapping[(app.qbert.row,app.qbert.col)]
    rad = app.width//36
    canvas.create_oval(x-rad, y-rad, x+rad, y+rad, fill = 'orange', 
                       width = 0)
    # ## draw test circle at top center of every cube top
    # for row in range(0, 7):
    #     for col in range(0,7-row):
    #         (x,y) = app.cubeTopMapping[(row,col)]
    #         canvas.create_oval(x-rad, y-rad, x+rad, y+rad, fill = 'orange', 
    #                    width = 0)
               
def drawRedEnemy(app, canvas):
    x, y = app.cubeTopMapping[(app.redEnemy.row,app.redEnemy.col)]
    rad = app.width//52
    canvas.create_oval(x-rad, y-rad, x+rad, y+rad, fill = 'red', 
                       width = 0)

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawPyramid(app, canvas)
    drawQbert(app, canvas)
    drawRedEnemy(app, canvas)
    
runApp(width=775, height=775)

