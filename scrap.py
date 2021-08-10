
from cmu_112_graphics import *


def redrawAll(app, canvas):
    canvas.create_text(app.width//8, app.height//2, 
                       text = 'Red Enemy Destroyed!', 
                       fill = 'red2', 
                       font = 'Helvetica 16 bold',
                       angle = 45)

runApp(width=775, height=775)
