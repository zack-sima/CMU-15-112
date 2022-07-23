#################################################
# hw5.py
#
# Your name:
# Your andrew id:
#################################################

import cs112_n22_week2_linter
from cmu_112_graphics import *
import math

#initializes necessary parameters for the app
def initializeAppParams(app, rows, columns): #helper-fn
    app.leftMargin = 5
    app.rightMargin = 5
    app.topMargin = 35
    app.bottomMargin = 5
    app.movingRight = True
    app.redDot = False
    app.explosionX, app.explosionY = 0, 0
    app.explosionSize = 0 #0 means no explosion yet
    app.pinkCoords = "" #note: use (x, y) to store coords
    app.rows = rows
    app.columns = columns
    app.gridWidth = (app.width - app.leftMargin - app.rightMargin) / app.columns
    app.gridHeight = (app.height - app.topMargin - app.bottomMargin) / app.rows

#app start
def appStarted(app):
    app.paused = False
    resetGame(app)
    restartGrid(app, rows=10, columns=10)

#resets game but doesn't remake the grid
def resetGame(app):
    app.redDot = False
    app.pinkCoords = ""
    app.explosionSize = 0
    app.score = 0
    resetDot(app)
    
#resets location of dot
def resetDot(app):
    app.movingRight = True
    app.dotRow, app.dotColumn = 0, 0

#recreates the grid based on new parameters
def restartGrid(app, rows, columns): #helper-fn
    initializeAppParams(app, rows=rows, columns=columns)
    resetGame(app)

#gets cell column, row (x, y) from mouse coordinates
def getCellFromMouseCoords(app, x, y):
    x -= app.leftMargin
    y -= app.topMargin
    if x < 0 or y < 0:
        return -1, -1
    x = int(x / app.gridWidth)
    y = int(y / app.gridHeight)
    return x, y

#internal event function
def mousePressed(app, event):
    #note: currently set to not be affected by pause to
    #debug better

    #cell mouse click lands inside
    cx, cy = getCellFromMouseCoords(app, event.x, event.y)

    if cx != -1 and cy != -1 and app.explosionSize == 0 and \
        f"({cx}, {cy})" not in app.pinkCoords:

        x, y = getCellFromMouseCoords(app, event.x, event.y)
        app.pinkCoords += f", ({x}, {y})"
        app.explosionSize = 10
        app.explosionX = event.x
        app.explosionY = event.y
        explosionIntersectsDot(app)

#internal event function
def keyPressed(app, event):
    if event.key == "p":
        app.paused = not app.paused
    elif event.key == "s":
        updateOnce(app)
    elif event.key == "r":
        resetGame(app)
    elif event.key.isdigit():
        n = int(event.key)
        if n < 4:
            restartGrid(app, n + 10, n + 10)

#checks whether the explosion intersects with dot
def explosionIntersectsDot(app): 
    #note: gridWidth / 2 assumed to be circle radius
    #since the game's dimensions are set
    dotX = app.leftMargin + (app.dotColumn + 0.5) * app.gridWidth
    dotY = app.topMargin + (app.dotRow + 0.5) * app.gridHeight
    if math.sqrt((dotX - app.explosionX) ** 2 + (dotY - app.explosionY) ** 2) \
        < app.explosionSize + app.gridWidth / 2:
        if not app.redDot:
            app.score += app.explosionSize // 10
            app.redDot = True
        else:
            app.score += 10
            app.redDot = False
        app.explosionSize = 0
        resetDot(app)

#moves the dot by one
def moveDot(app):
    if app.movingRight:
        if app.dotColumn < app.columns - 1:
            app.dotColumn += 1
        elif app.dotRow < app.rows - 1:
            app.dotRow += 1
            app.movingRight = False
        else:
            resetDot(app)
    else:
        if app.dotColumn > 0:
            app.dotColumn -= 1
        elif app.dotRow < app.rows - 1:
            app.dotRow += 1
            app.movingRight = True
        else:
            resetDot(app)

#grows the explosion by 10/removes it when r>50
def growExplosion(app):
    if app.explosionSize <= 0:
        return

    app.explosionSize += 10
    explosionIntersectsDot(app)
    if app.explosionSize > 50: #stop explosion
        app.explosionSize = 0
        if app.score > 0:
            app.score -= 1
        
#does one step
def updateOnce(app): #helper-fn
    moveDot(app)
    growExplosion(app)

#internal timer function
def timerFired(app):
    if not app.paused:
        updateOnce(app)

#visual functions
#################
def drawTitleAndScore(app, canvas):
    canvas.create_text(app.width / 2, app.topMargin / 2,
        text="Hw5 Game!", anchor="center")

    canvas.create_text(app.width - app.topMargin / 2, app.topMargin / 2,
        text=f"Score: {app.score}", anchor="e")

#draws the grid according to app measurements defined in start
def drawGrid(app, canvas):
    for i in range(app.columns):
        for j in range(app.rows):
            canvas.create_rectangle(app.leftMargin + app.gridWidth * i, 
                app.topMargin + app.gridHeight * j, 
                app.leftMargin + app.gridWidth * (i + 1), 
                app.topMargin + app.gridHeight * (j + 1),
                fill="white" if f"({i}, {j})" not in app.pinkCoords else "pink")

#draws the dot
def drawDot(app, canvas):
    canvas.create_oval(app.leftMargin + app.dotColumn * app.gridWidth,
        app.topMargin + app.dotRow * app.gridHeight,
        app.leftMargin + (app.dotColumn + 1) * app.gridWidth,
        app.topMargin + (app.dotRow + 1) * app.gridHeight, fill="blue"\
        if not app.redDot else "red")

#draws the explosion
def drawExplosion(app, canvas):
    if app.explosionSize > 0:
        canvas.create_oval(app.explosionX - app.explosionSize,
            app.explosionY - app.explosionSize,
            app.explosionX + app.explosionSize,
            app.explosionY + app.explosionSize, fill="orange")
################

def redrawAll(app, canvas):
    drawTitleAndScore(app, canvas)
    drawGrid(app, canvas)
    drawDot(app, canvas)
    drawExplosion(app, canvas)

def main():
    cs112_n22_week2_linter.lint()
    runApp(width=510, height=540)

if __name__ == '__main__':
    main()