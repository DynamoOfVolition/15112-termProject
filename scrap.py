# SideScroller1:

from cmu_112_graphics import *
import random

def appStarted(app):
    app.scrollX = 0
    app.dots = [(random.randrange(app.width),
                  random.randrange(60, app.height)) for _ in range(50)]

def keyPressed(app, event):
    if (event.key == "Left"):    app.scrollX -= 5
    elif (event.key == "Right"): app.scrollX += 5

def redrawAll(app, canvas):
    # draw the player fixed to the center of the scrolled canvas
    cx, cy, r = app.width/2, app.height/2, 10
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='cyan')

    # draw the dots, shifted by the scrollX offset
    for (cx, cy) in app.dots:
        cx -= app.scrollX  # <-- This is where we scroll each dot!!!
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='lightGreen')

    # draw the x and y axes
    x = app.width/2 - app.scrollX # <-- This is where we scroll the axis!
    y = app.height/2
    canvas.create_line(x, 0, x, app.height)
    canvas.create_line(0, y, app.width, y)

    # draw the instructions and the current scrollX
    x = app.width/2
    canvas.create_text(x, 20, text='Use arrows to move left or right')
    canvas.create_text(x, 40, text=f'app.scrollX = {app.scrollX}')

runApp(width=300, height=300)