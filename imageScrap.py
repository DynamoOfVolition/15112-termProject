from cmu_112_graphics import *

def appStarted(app):
    app.image1 = app.loadImage('qbert_down_left.png')
    app.image2 = app.scaleImage(app.image1, 2/3)

def redrawAll(app, canvas):
    canvas.create_image(200, 300, image=ImageTk.PhotoImage(app.image1))
    canvas.create_image(500, 300, image=ImageTk.PhotoImage(app.image2))

runApp(width=700, height=600)