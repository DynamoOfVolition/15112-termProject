import random

def distance(x0, y0, x1, y1):
        return ((x0-x1)**2 + (y0-y1)**2)**0.5

def createCubeTopDict(width, height):
## returns a mapping from cube row, column to center point at top surface 
## (row, col) --> (cx, cy).  
    cubHt = height//12
    cubeTopDict = dict()
    for row in range(0,7):
        for col in range(0,7-row):
            cx = 0.26*width + 0.08*width*col + 0.04*height*row
            cy = 0.65*height - 0.06*height*row - cubHt/2
            if (row,col) not in cubeTopDict:
                cubeTopDict[(row,col)] = []
            cubeTopDict[(row,col)] = (cx,cy)
    return cubeTopDict 

mapping = {(0, 0): (201.5, 471.75), (0, 1): (263.5, 471.75), 
           (0, 2): (325.5, 471.75), (0, 3): (387.5, 471.75), 
           (0, 4): (449.5, 471.75), (0, 5): (511.5, 471.75), 
           (0, 6): (573.5, 471.75), (1, 0): (232.5, 425.25), 
           (1, 1): (294.5, 425.25), (1, 2): (356.5, 425.25), 
           (1, 3): (418.5, 425.25), (1, 4): (480.5, 425.25), 
           (1, 5): (542.5, 425.25), (2, 0): (263.5, 378.75), 
           (2, 1): (325.5, 378.75), (2, 2): (387.5, 378.75), 
           (2, 3): (449.5, 378.75), (2, 4): (511.5, 378.75), 
           (3, 0): (294.5, 332.25), (3, 1): (356.5, 332.25), 
           (3, 2): (418.5, 332.25), (3, 3): (480.5, 332.25), 
           (4, 0): (325.5, 285.75), (4, 1): (387.5, 285.75), 
           (4, 2): (449.5, 285.75), (5, 0): (356.5, 239.25), 
           (5, 1): (418.5, 239.25), (6, 0): (387.5, 192.75)}

path = [(6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0,0),
        (5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1), 
        (3, 2), (2, 2), (1, 2), 
        (3, 3), (2, 3), (1, 3), (0, 3),
        (2, 4), (1, 4), (0, 4), 
        (1, 5), (0, 5),
        (0,6)]
       
          
           
       
    

print("mapping == ", mapping)
print("path == ", path)
print("========")

def getDirection(rowStart, colStart):
    ## in the case where there are no untouched cubes along any legal direction,
    ## increment row,col along direction with closest untouched cube
    ## return rowStop and colStop along direction of closest untouched cube

        ## loop through all cubes and find untouched cube with lowest distance
        ## increment row,col along that direction

        curDist = 0
        bestDist = 775
        bestRC = ()

        mapping = createCubeTopDict(775, 775)
        (x0,y0) = mapping[(rowStart,colStart)]
        print("your location = ", x0, y0)
        print("your coords = ", rowStart, colStart)
        for row in range(0,7):
            for col in range(0,7-row):
                
                if (row,col) not in path:
                    print("======")
                    (x1,y1) = mapping[(row,col)]
                    curDist = distance(x0, y0, x1, y1)
                    print("open location = ", x1, y1)
                    print("open coords = ", row, col)

                    print("distance to that location = ", curDist)

                    if curDist < bestDist:
                        bestDist = curDist
                        bestRC = (row,col)
        
        ## now determine rowStop and colStop that get approach bestRC
        
        ## if on same row
        if bestRC[0] == rowStart:
            ## if on bottom row, rowStart can only increase
            if rowStart == 0:
                rowStop = rowStart + 1
                ## if to the right
                if bestRC[1] >= colStart:
                    colStop = colStart
                ## if to the left
                else:
                    colStop = colStart - 1
            ## if on middle row, can go down/up 
            else:
                rowIncrement = random.choice([-1,1])
                rowStop = rowStart + rowIncrement
                ## if go down a row
                if rowIncrement == -1:
                    ## if to the right
                    if bestRC[1] > colStart:
                        colStop = colStart +1
                    ## if to the left
                    else:
                        colStop = colStart
                ## if go up a row
                else:
                    ## if to the right
                    if bestRC[1] > colStart:
                        colStop = colStart
                    ## if to the left
                    else:
                        colStop = colStart -1

        ## if above, must increment row by 1
        elif bestRC[0] > rowStart:
            rowStop = rowStart + 1
            ## if to the left
            if bestRC[1] < colStart:
                colStop = colStart - 1
            ## if to the right
            else:
                colStop = colStart

        ## if below, must decrement row by 1
        elif bestRC[0] < rowStart:
            rowStop = rowStart - 1

            ## if to the left
            if bestRC[1] < colStart:
                colStop = colStart - 1
            ## if to the right
            else:
                colStop = colStart

        print("best row, col = ", bestRC)
        print("move to row: ", (rowStop, colStop))

        return (rowStop, colStop)
                    
        # rowStop = bestRC[0]
        # colStop = bestRC[1]
        # return(rowStop, colStop)

print(getDirection(0,5))