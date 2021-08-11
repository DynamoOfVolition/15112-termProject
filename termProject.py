from cmu_112_graphics import *
import random
import player as pl

def initializeQbert(app):
## make a new qbert, called whenever a round or level is completed
    (x, y) = app.cubeTopMapping[(6,0)]
    app.qbert = pl.Player(6, 0, 6, 0, x, y)

def initializeRedEnemy(app):
## make a new red enemy, initializing starting cube at random
    randRow = random.randint(0,5)
    randCol = random.randint(0,6-randRow)
    (x, y) = app.cubeTopMapping[(randRow,randCol)]
    app.redEnemy = pl.Player(randRow, randCol, randRow, randCol, x, y)
    #app.redEnemy.path.append((randRow, randCol)) # not used yet

def initializeGreenEnemy(app):
    randRow = random.randint(0,5)
    randCol = random.randint(0,6-randRow)
    (x, y) = app.cubeTopMapping[(randRow,randCol)]
    app.greenEnemy = pl.Player(randRow, randCol, randRow, randCol, x, y)

def initializeSnake(app):
    randRow = random.randint(0,5)
    randCol = random.randint(0,6-randRow)
    (x, y) = app.cubeTopMapping[(randRow,randCol)]
    app.snake = pl.Player(randRow, randCol, randRow, randCol, x, y)

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
    initializeSnake(app)

def appStarted(app):
    app.timerDelay = 50

    ## cube 
    ## ... coords of top corner of top cube surface 
    # cx = app.width//2
    # cy = app.height//2 - 3*app.cubHt
    app.defaultTopColor = 'RoyalBlue3'
    app.cubWd = app.width//12
    app.cubHt = app.height//12
    app.cubeTopMapping = createCubeTopDict(app)
    print(app.cubeTopMapping)
    ## top colors
    colorList = ['yellow', 'violet', 'chartreuse2', 'deep pink', 'tomato']
    app.topColor = {}
    for i in range(1,len(colorList)+1):
        app.topColor[i] = colorList[i-1]
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
## increment score by 25 whenever qbert touches a new cube - including
## cubes that were turned off by green enemy
    if (app.qbert.row, app.qbert.col) not in app.qbert.path:
        app.score += 25

def cubicBezier(t, p0, p1, p2):
## Bezier curve function and code adapted from 
## https://towardsdatascience.com/bézier-curve-bfffdadea212

    ## returns a point along a cubic bezier curve 
    px = (1-t)**2*p0[0] + 2*t*(1-t)*p1[0] + t**2*p2[0]
    py = (1-t)**2*p0[1] + 2*t*(1-t)*p1[1] + t**2*p2[1]
    return (px, py)

def manageCollision(app):
## if qbert hops on any enemy, set their alive flag to False, add 10 to score
    if app.qbert.isCollision(app.redEnemy):
        app.redEnemy.alive = False
        app.score += 10
    elif app.qbert.isCollision(app.greenEnemy):
        app.greenEnemy.alive = False
        app.score += 10
    elif app.qbert.isCollision(app.snake):
        app.snake.alive = False
        app.score += 10

def keyPressed(app, event):
## update qberts location, pause/unpause, begin new level, (autoplay tbd))
    # previousRow = app.qbert.rowStart
    # previousCol = app.qbert.colStart
    app.qbert.rowStart = app.qbert.rowStop
    app.qbert.colStart = app.qbert.colStop

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
                app.qbert.moveStart = True
                # app.qbert.row += 1
                # app.qbert.col += 0
                app.qbert.rowStop = app.qbert.rowStart + 1
                app.qbert.colStop = app.qbert.colStart
                #updateScore(app)
                #manageCollision(app)
        elif event.key == 'u': # up-left
            if app.qbert.colStart != 0 and app.qbert.rowStart != 6:
                app.qbert.moveStart = True
            #if app.qbert.col != 0 and app.qbert.row != 6:
                #app.qbert.row += 1
                #app.qbert.col -= 1
                app.qbert.rowStop = app.qbert.rowStart + 1
                app.qbert.colStop = app.qbert.colStart - 1
                #updateScore(app)
                #manageCollision(app)
        elif event.key == 'j': # down-left
            if app.qbert.rowStart > 0:
                app.qbert.moveStart = True
            #if app.qbert.row > 0:
                #app.qbert.row -= 1
                #app.qbert.col += 1
                app.qbert.rowStop = app.qbert.rowStart - 1
                app.qbert.colStop = app.qbert.colStart + 1
                #updateScore(app)
                #manageCollision(app)
        elif event.key == 'h': # down-right
            #if app.qbert.row > 0:
            if app.qbert.rowStart > 0:
                app.qbert.moveStart = True
                #app.qbert.row -= 1
                #app.qbert.col += 0
                app.qbert.rowStop = app.qbert.rowStart - 1
                app.qbert.colStop = app.qbert.colStart 
                #updateScore(app)
                #manageCollision(app)
        ## store cube top that qbert has touched - make sure not to double count
        ## current cube if qbert is trying to make illegal move
        # if ((app.qbert.row, app.qbert.col) != (previousRow, previousCol) and
        #     (app.qbert.row, app.qbert.col) not in app.qbert.path):
        #     app.qbert.path.append((app.qbert.row, app.qbert.col))     
        if ((app.qbert.rowStop, app.qbert.colStop) != 
            (app.qbert.rowStart, app.qbert.colStart) and
            (app.qbert.rowStop, app.qbert.colStop) not in app.qbert.path):
            app.qbert.path.append((app.qbert.rowStop, app.qbert.colStop))     
        #print(app.qbert.path)

    ## if game is over, restart
    elif app.gameOver:
        if event.key == 'Enter':
            restartApp(app)

def newRound(app):
    initializeQbert(app)
    initializeRedEnemy(app)
    initializeGreenEnemy(app)
    initializeSnake(app)
    app.round += 1
            
def timerFired(app):    
    if not app.pauseGame and not app.gameOver:

        ## if score goes negative, game is over (temp stop after level 1 finished)
        if app.score < 0 or app.round > 5:
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

        ## if qbert killed snake, make a new one
        elif app.snake.alive == False:
            initializeSnake(app)

        ## otherwise game continues    
        else:
            if app.qbert.moveStart:
                if app.qbert.drawCount < 11:
                    app.qbert.drawCount += 1
                elif app.qbert.drawCount == 11:
                    app.qbert.moveStart = False
                    app.qbert.drawCount = 1
            #print("move qbert by increment:  ", app.qbert.drawCount)

            ## move red  & green enemies 
            #app.redEnemy.randomMove()
            #app.greenEnemy.randomMove()
            #app.qbert.followMove(app.snake)

            ## if enemy goes onto cube qbert is on deduct points
            # if (app.qbert.isCollision(app.redEnemy) or
            #     app.qbert.isCollision(app.greenEnemy) or
            #     app.qbert.isCollision(app.snake)):
            #     app.score -=50

def difficultyCondition(app):
## return True if a certain difficulty condition is met depending on round num
## these are the squares the green enemy will UNDO
## round 1 condition: any corner
## round 2 condition: bottom row
## round 3 condition: left or right edge
## round 4 condition: left or right edge or bottom row
## round 5 condition: all but top square

## difficulty condition 1: on center block (2,2)
    if app.round == 1:
        return((app.greenEnemy.row,app.greenEnemy.col) == (0,0) or
               (app.greenEnemy.row,app.greenEnemy.col) == (0,6) or
               (app.greenEnemy.row,app.greenEnemy.col) == (6,0))
    elif app.round == 2:
        return(app.greenEnemy.row == 0)
    elif app.round == 3:
        return(app.greenEnemy.onRightEdge() or app.greenEnemy.col==0)
    elif app.round == 4:
        return (app.greenEnemy.onRightEdge() or app.greenEnemy.col==0 or
                app.greenEnemy.row==0)
    elif app.round == 5:
        return ((app.greenEnemy.row, app.greenEnemy.col) != (6,0))

def setTopColor(app, row, col):
## returns the color of the top of the cube located at row, col
    ## if greenEnemy touched one of qberts squares (according to difficulty)
    if ((row, col) in app.qbert.path and 
        #(row, col) == (app.greenEnemy.row, app.greenEnemy.col) and
        (row, col) == (app.greenEnemy.rowStop, app.greenEnemy.colStop) ):
         #and difficultyCondition(app)):
        app.qbert.path.remove((row,col))
        return(app.defaultTopColor)
    ## else if only qbert has touched, change color
    elif (row, col) in app.qbert.path:
        return(app.topColor[app.round])
    ## else hasn't been touched by qbert   
    else:
        return(app.defaultTopColor)
    
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

    topColor = 'RoyalBlue3'
    #topColor = setTopColor(app, row, col)

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
## Bezier curve function and code adapted from 
## https://towardsdatascience.com/bézier-curve-bfffdadea212
    print("===")
    print("drawing Qbert")
    
    ## draw just one
    #x, y = app.cubeTopMapping[(app.qbert.row,app.qbert.col)]

    ## get starting and ending points for the jump
    xStart, yStart = app.cubeTopMapping[(app.qbert.rowStart, app.qbert.colStart)]
    xStop, yStop = app.cubeTopMapping[(app.qbert.rowStop, app.qbert.colStop)]
    #xIntm, yIntm = (xStop+10, 50+app.qbert.rowStart*app.cubHt)
    if yStart < yStop:
        xIntm, yIntm = (xStop, yStart)
    else:
        xIntm, yIntm = (xStart, yStop)

    p0 = (xStart, yStart)
    p1 = (xIntm, yIntm)
    p2 = (xStop, yStop)

    print("start row, col is: ", ((app.qbert.rowStart, app.qbert.colStart)))
    print("start x, y is: ", p0 )
    print("end row, col is: ", ((app.qbert.rowStop, app.qbert.colStop)))
    print("end x, y is: ", p2 )

    #print(p0, p1, p2)

    print(app.qbert.drawCount)
    #print(app.qbert.bezierIncrements)

    rad = app.width//36
    t = app.qbert.bezierIncrements[app.qbert.drawCount]

    if app.qbert.moveStart:
        (x, y) = cubicBezier(t, p0, p1, p2)
        print("(x, y) = ", (x, y))
    else:
        (x, y) = p2
        
    canvas.create_oval(x-rad, y-rad, x+rad, y+rad, fill = 'orange', 
                        width = 0)
    

               
def drawEnemy(app, canvas, enemy):
    if enemy=='red':
        x, y = app.cubeTopMapping[(app.redEnemy.row, app.redEnemy.col)]
        rad = app.width//52
    elif enemy=='green':
        x, y = app.cubeTopMapping[(app.greenEnemy.row, app.greenEnemy.col)]
        rad = app.width//48
    elif enemy=='purple':
        rad = app.width//40
        x, y = app.cubeTopMapping[(app.snake.row, app.snake.col)]
    
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

    # if app.redEnemy.alive:
    #     drawEnemy(app, canvas, 'red')

    # if app.greenEnemy.alive:
    #     drawEnemy(app, canvas, 'green')
    
    # if app.snake.alive:
    #     drawEnemy(app, canvas, 'purple')

    if app.roundWon:
        drawRoundWon(app, canvas)
    elif app.gameOver:
        drawGameOver(app, canvas)
    elif not app.redEnemy.alive: 
        drawKillMessage(app, canvas)

runApp(width=775, height=775)

