from cmu_112_graphics import *


def appStarted(app):
    app.score = 0
    app.level = 1
    app.round = 1
    app.cubeCenters = []

def keyPressed(app, event):
    pass

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

def drawCube(app, canvas, cx, cy):
## draw a single cube centered at the point (x,y):
## each cube consists of 3 polygons drawn based on 7 total points:
    cubHt = app.height//12
    cubWd = app.width//12
    
    pt1X = cx - cubWd/2
    pt1Y = cy - cubHt/4

    pt2X = cx
    pt2Y = cy - cubHt/2
    
    pt3X = cx + cubWd/2
    pt3Y = pt1Y
    
    pt4X = cx
    pt4Y = cy

    pt5X = pt4X
    pt5Y = pt4Y + cubHt/2

    pt6X = pt1X
    pt6Y = pt1Y + cubHt/2

    pt7X = pt3X
    pt7Y = pt6Y
    
    ## top
    canvas.create_polygon(pt1X, pt1Y, pt2X, pt2Y, pt3X, pt3Y, pt4X, pt4Y,
                          fill = 'RoyalBlue3')
    ## left side
    canvas.create_polygon(pt1X, pt1Y, pt4X, pt4Y, pt5X, pt5Y, pt6X, pt6Y,
                          fill = 'SeaGreen3')
    ## right side
    canvas.create_polygon(pt4X, pt4Y, pt3X, pt3Y, pt7X, pt7Y, pt5X, pt5Y,
                          fill = 'PaleGreen4')

   
def drawCubes(app, canvas):
## draw pyramid of cubes - number of rows and cols never changes, so hard-coded.
## size of cubes is hard-coded, bc screen size cannot change in original game
    dy = app.height//28
    
    
    for row in range(0, 1):
        for col in range(0,1):
            pass
 
def redrawAll(app, canvas):
    drawBackground(app, canvas)
    cx = app.width//2
    cy = app.height//8 + app.height//28 + app.height//12
    drawCube(app, canvas, cx, cy)
    #drawCubes(app, canvas)
    


runApp(width=650, height=650)

