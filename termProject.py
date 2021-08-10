from cmu_112_graphics import *
import random
import player as pl

def initializeQbert(app):
## make a new qbert, called whenever a round or level is completed
    app.qbert = pl.Player(6, 0)

def initializeRedEnemy(app):
## make a new red enemy, initializing starting cube at random
    randRow = random.randint(0,5)
    randCol = random.randint(0,6-randRow)
    app.redEnemy = pl.Player(randRow, randCol)
    #app.redEnemy.path.append((randRow, randCol)) # not used yet

def initializeGreenEnemy(app):
    randRow = random.randint(0,5)
    randCol = random.randint(0,6-randRow)
    app.greenEnemy = pl.Player(randRow, randCol)

def restartApp(app):
    ## gameplay
    app.score = 0
    app.level = 1
    app.round = 1
    app.roundWon = False
    app.pauseGame = False
    app.gameOver = False

    ## create qbert and creatures
    initializeQbert(app)
    initializeRedEnemy(app)
    initializeGreenEnemy(app)

def appStarted(app):
    app.timerDelay = 1000

    ## cube 
    ## ... coords of top corner of top cube surface 
    # cx = app.width//2
    # cy = app.height//2 - 3*app.cubHt
    app.defaultTopColor = 'RoyalBlue3'
    app.cubWd = app.width//12
    app.cubHt = app.height//12
    app.cubeTopMapping = createCubeTopDict(app)
    restartApp(app)
    
    
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

def updateScore(app):
    if (app.qbert.row, app.qbert.col) not in app.qbert.path:
        app.score += 25

def manageCollision(app):
## if qbert hops on red enemy, set alive flag to False, returns None
    if app.qbert.isCollision(app.redEnemy):
        app.redEnemy.alive = False
    elif app.qbert.isCollision(app.greenEnemy):
        app.greenEnemy.alive = False

def keyPressed(app, event):
## update qberts location, pause/unpause, begin new level, autoplay (nyi)
    previousRow = app.qbert.row
    previousCol = app.qbert.col

    ## check if game is to be paused or unpaused
    if event.key == 'p':
        app.pauseGame = not app.pauseGame

    ## if game is not paused or over, continue
    if not app.pauseGame and not app.gameOver:
        ## enter used to initialize new round only here
        if event.key == 'Enter':
            app.roundWon = False
        ## check for movement keys
        if event.key == 'i': # up-right
            if not app.qbert.onRightEdge():
                app.qbert.row += 1
                updateScore(app)
                manageCollision(app)
        elif event.key == 'u': # up-left
            if app.qbert.col != 0 and app.qbert.row != 6:
                app.qbert.row += 1
                app.qbert.col -= 1
                updateScore(app)
                manageCollision(app)
        elif event.key == 'j': # down-left
            if app.qbert.row > 0:
                app.qbert.row -= 1
                app.qbert.col += 1
                updateScore(app)
                manageCollision(app)
        elif event.key == 'h': # down-right
            if app.qbert.row > 0:
                app.qbert.row -= 1
                updateScore(app)
                manageCollision(app)
        ## store cube top that qbert has touched - make sure not to double count
        ## current cube if qbert is trying to make illegal move
        if ((app.qbert.row, app.qbert.col) != (previousRow, previousCol) and
            (app.qbert.row, app.qbert.col) not in app.qbert.path):
            app.qbert.path.append((app.qbert.row, app.qbert.col))     
        #print(app.qbert.path)

    ## if game is over, restart
    elif app.gameOver:
        if event.key == 'Enter':
            restartApp(app)

def newRound(app):
    initializeQbert(app)
    initializeRedEnemy(app)
    initializeGreenEnemy(app)
    app.round += 1
            
def timerFired(app):    
    if not app.pauseGame and not app.gameOver:

        ## if score goes negative, game is over
        if app.score < 0:
            app.gameOver = True

        ## if qbert touches all cube tops, round is won
        elif len(app.qbert.path) == 28:
            app.roundWon = True
            newRound(app)

        ## if qbert killed red enemy, make a new one
        elif app.redEnemy.alive == False:
            initializeRedEnemy(app)

        ## if qbert killed green enemy, make a new one
        elif app.greenEnemy.alive == False:
            initializeGreenEnemy(app)

        ## otherwise game continues    
        else:
            ## move red  & green enemies 
            app.redEnemy.randomMove()
            app.greenEnemy.randomMove()

            ## if red enemy goes onto cube qbert is on
            if (app.qbert.isCollision(app.redEnemy) or
                app.qbert.isCollision(app.greenEnemy)):
                app.score -=50

def difficultyCondition(app):
## return True if a certain difficulty condition is met depending on round num
## difficulty condition 4: on left or right edge
## difficulty condition 3: on bottom row
## difficulty condition 2: on any corner
## difficulty condition 1: on center block (2,2)
    if app.round == 1:
        return((app.greenEnemy.row,app.greenEnemy.col) == (2,2))
    elif app.round == 2:
        return((app.greenEnemy.row,app.greenEnemy.col) == (0,0) or
               (app.greenEnemy.row,app.greenEnemy.col) == (0,6) or
               (app.greenEnemy.row,app.greenEnemy.col) == (6,0))
    elif app.round == 3:
        return(app.greenEnemy.row == 0)
    elif app.round == 4:
        return(app.greenEnemy.onRightEdge() or app.greenEnemy.col==0)

def setTopColor(app, row, col):
## returns the color of the top of the cube located at row, col
## colors depends on round and level
## get rid of if/else by using list and indexing..
    if app.level == 1:
        if app.round == 1:
            ## if greenEnemy on square qbert touched according to difficulty 1
            if ((row, col) in app.qbert.path and 
                (row, col) == (app.greenEnemy.row, app.greenEnemy.col) and
                difficultyCondition(app)):
                app.qbert.path.remove((row,col))
                return(app.defaultTopColor)
            ## else if only qbert has touched, make yello
            elif (row, col) in app.qbert.path:
            #if (row, col) in app.qbert.path:
                return('yellow')
            else:
                return(app.defaultTopColor)
        elif app.round == 2:
            if (row, col) in app.qbert.path:
                return('violet')
            else:
                return(app.defaultTopColor)
        elif app.round == 3:
            if (row, col) in app.qbert.path:
                return('chartreuse2')
            else:
                return(app.defaultTopColor)
    
    print("app.qbert.path AFTER ===== ", app.qbert.path)


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
    canvas.create_text(app.width - app.width//8, app.height//8 + dy, 
                       text = f'Round: {app.round}',
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
                          fill = 'DarkSeaGreen4') # DarkOliveGreen4 ?
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
               
def drawEnemy(app, canvas, enemy):
    if enemy=='red':
        x, y = app.cubeTopMapping[(app.redEnemy.row,app.redEnemy.col)]
        rad = app.width//52
    elif enemy=='green':
        x, y = app.cubeTopMapping[(app.greenEnemy.row,app.greenEnemy.col)]
        rad = app.width//48
    
    canvas.create_oval(x-rad, y-rad, x+rad, y+rad, fill = enemy, width = 0)

def drawRoundWon(app, canvas):
    canvas.create_text(app.width//2, app.height//8,
                       text = f'You won Round {app.round-1}!!!',
                       fill = 'white',
                       font = 'Helvetica 24 bold')
    canvas.create_text(app.width//2, app.height//8 + app.height//28,
                       text = f'Press Enter to continue...',
                       fill = 'white',
                       font = 'Helvetica 24 bold')

def drawGameOver(app, canvas):
    canvas.create_text(app.width//2, app.height//8,
                       text = 'Game Over!!!!',
                       fill = 'chartreuse',
                       font = 'Helvetica 28 bold')
    canvas.create_text(app.width//2, app.height//8 + app.height//20,
                       text = f'Press Enter to restart...',
                       fill = 'hot pink',
                       font = 'Helvetica 24 bold italic')

def drawKillMessage(app, canvas):
    canvas.create_text(app.width//8, app.height//2, 
                       text = 'Red Enemy Destroyed!', 
                       fill = 'red2', 
                       font = 'Helvetica 16 bold')
                       #angle = 45)

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawPyramid(app, canvas)
    drawQbert(app, canvas)

    if app.redEnemy.alive:
        drawEnemy(app, canvas, 'red')

    if app.greenEnemy.alive:
        drawEnemy(app, canvas, 'green')

    if app.roundWon:
        drawRoundWon(app, canvas)
    elif app.gameOver:
        drawGameOver(app, canvas)
    elif not app.redEnemy.alive: 
        drawKillMessage(app, canvas)
runApp(width=775, height=775)

