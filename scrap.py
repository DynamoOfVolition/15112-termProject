
from cmu_112_graphics import *

def appStarted(app):
    colorList = ['yellow', 'violet', 'chartreuse2', 'deep pink', 'tomato']
    app.topColor = {}
    for i in range(1,len(colorList)+1):
        app.topColor[i] = colorList[i-1]
    print(app.topColor)

# def redrawAll(app, canvas):
#     canvas.create_text(app.width//8, app.height//2, 
#                        text = 'Red Enemy Destroyed!', 
#                        fill = 'red2', 
#                        font = 'Helvetica 16 bold',
#                        angle = 45)

runApp(width=775, height=775)
