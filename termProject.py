from cmu_112_graphics import *

class Player(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col

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
    ## score 
    app.score = 0
    app.level = 1
    app.round = 1
    ## cube 
    app.topColor = 'RoyalBlue3'
    app.cubWd = app.width//12
    app.cubHt = app.height//12
    app.cubeTopMapping = createCubeTopDict(app)
    ## ... coords of top corner of top cube surface
    # cx = app.width//2
    # cy = app.height//2 - 3*app.cubHt
    ## qbert parameters
    app.qbert = Player(6, 0)
    app.qbertPath = []

def onRightEdge(app):
    onRightEdge = ((app.qbert.row == 6 and app.qbert.col == 0) or
                     (app.qbert.row == 5 and app.qbert.col == 1) or
            (app.qbert.row == 4 and app.qbert.col == 2) or
            (app.qbert.row == 3 and app.qbert.col == 3) or
            (app.qbert.row == 2 and app.qbert.col == 4) or
            (app.qbert.row == 1 and app.qbert.col == 5) or
            (app.qbert.row == 0 and app.qbert.col == 6))
    print("OnRightEdge = ", onRightEdge)
    return onRightEdge

def keyPressed(app, event):
## recall app.cubeTopDict[(row,col)] = (cx,cy)
## update app.qbert.cx and app.qbert.cy
    #if event.key == 'Up' and event.key == 'Right':
    if event.key == 'i':
        if not onRightEdge(app):
            app.qbert.row += 1
    #elif event.key == 'Up' and event.key == 'Left':
    elif event.key == 'u':
        if app.qbert.col != 0:
            app.qbert.row += 1
            app.qbert.col -= 1
    #elif event.key == 'Down' and event.key == 'Right':
    elif event.key == 'j':
        if app.qbert.row > 0:
            app.qbert.row -= 1
            app.qbert.col += 1
    #elif event.key == 'Down' and event.key == 'Left':
    elif event.key == 'h':
        if app.qbert.row > 0:
            app.qbert.row -= 1

def mousePressed(app, event):
    pass

def timerFired(app):
    pass

def getCell(app, x, y):
    pass

def getCellBounds(app, row, col):
    pass

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
    ## top
    canvas.create_polygon(pt1X, pt1Y, pt2X, pt2Y, pt3X, pt3Y, pt4X, pt4Y,
                          fill = app.topColor)
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
## scales with window size
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
               
def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawPyramid(app, canvas)
    drawQbert(app, canvas)
    
runApp(width=775, height=775)

