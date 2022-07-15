#################################################
# hw5.py
#
# Your name:
# Your andrew id:
#################################################

import cs112_n22_week2_linter
from cmu_112_graphics import *
import math

def initializeAppParams(app, rows, columns): #helper-fn
    app.leftMargin = 5
    app.rightMargin = 5
    app.topMargin = 35
    app.bottomMargin = 5
    app.movingRight = True
    app.redDot = False
    app.explosionX, app.explosionY = 0, 0
    app.explosionSize = 0 #0 means no explosion yet

    app.rows = rows
    app.columns = columns
    app.gridWidth = (app.width - app.leftMargin - app.rightMargin) / app.columns
    app.gridHeight = (app.height - app.topMargin - app.bottomMargin) / app.rows

def appStarted(app):
    app.paused = False
    resetGame(app)
    restartGrid(app, rows=10, columns=10)

def resetGame(app):
    app.explosionSize = 0
    app.score = 0
    resetDot(app)
    
def resetDot(app):
    app.dotRow, app.dotColumn = 0, 0

def restartGrid(app, rows, columns): #helper-fn
    initializeAppParams(app, rows=rows, columns=columns)
    resetGame(app)

def getCellBounds(app, row, col):
    return app.leftMargin + col * app.gridWidth,
    app.topMargin + row * app.gridHeight,
    app.leftMargin + (col + 1) * app.gridWidth,
    app.topMargin + (row + 1) * app.gridHeight,

def mousePressed(app, event):
    if app.paused:
        return
    if app.explosionSize == 0:
        app.explosionSize = 10
        app.explosionX = event.x
        app.explosionY = event.y
        explosionIntersectsDot(app)

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


def moveDot(app):
    if app.movingRight:
        if app.dotColumn < app.columns - 1:
            app.dotColumn += 1
        elif app.dotRow < app.rows - 1:
            app.dotRow += 1
            app.movingRight = False
        else:
            app.dotRow = 0
            app.dotColumn = 0
    else:
        if app.dotColumn > 0:
            app.dotColumn -= 1
        elif app.dotRow < app.rows - 1:
            app.dotRow += 1
            app.movingRight = True
        else:
            app.dotRow = 0
            app.dotColumn = 0
            app.movingRight = True

def growExplosion(app):
    if app.explosionSize > 0:
        app.explosionSize += 10
        if app.explosionSize > 50: #stop explosion
            app.explosionSize = 0
            if app.score > 0:
                app.score -= 1
        explosionIntersectsDot(app)

def updateOnce(app): #helper-fn
    moveDot(app)
    growExplosion(app)

def timerFired(app):
    if not app.paused:
        updateOnce(app)

#visual functions

def drawTitleAndScore(app, canvas):
    canvas.create_text(app.width / 2, app.topMargin / 2,
        text="Hw5 game!", anchor="center")

    canvas.create_text(app.width - app.topMargin / 2, app.topMargin / 2,
        text=f"Score: {app.score}", anchor="e")

#draws the grid according to app measurements defined in start
def drawGrid(app, canvas):
    for i in range(app.columns):
        for j in range(app.rows):
            canvas.create_rectangle(app.leftMargin + app.gridWidth * i, 
                app.topMargin + app.gridHeight * j, 
                app.leftMargin + app.gridWidth * (i + 1), 
                app.topMargin + app.gridHeight * (j + 1))

def drawDot(app, canvas):
    canvas.create_oval(app.leftMargin + app.dotColumn * app.gridWidth,
        app.topMargin + app.dotRow * app.gridHeight,
        app.leftMargin + (app.dotColumn + 1) * app.gridWidth,
        app.topMargin + (app.dotRow + 1) * app.gridHeight, fill="blue"\
        if not app.redDot else "red")

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