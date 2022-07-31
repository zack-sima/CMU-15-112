#################################################
# hw9.py: Tetris!
#
# Your name: Zack
# Your andrew id: ysima
#
# Your partner's name: Harshal
# Your partner's andrew id: hdalvaig
#################################################

import cs112_n22_week4_linter
import math, copy, random

from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

def playTetris():
    runApp(width=350, height=500)

#helper unused function
def changeDimensions(app, w, h):
    app.rows += w
    app.cols += h
    init(app)

def init(app):
    app.score = 0
    app.gameOver = False
    app.board = []

    for i in range(app.rows):
        app.board.append([])
        for j in range(app.cols):
            app.board[i].append("blue") #blue = empty cell

    initPieces(app)
    newFallingPiece(app)

def initPieces(app):
    # Seven "standard" pieces (tetrominoes)
    iPiece = [
        [  True,  True,  True,  True ]
    ]
    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    app.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    app.tetrisPieceColors = ["red", "yellow", "magenta",
    "pink", "cyan", "green", "orange"]


def newFallingPiece(app):
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = copy.deepcopy(app.tetrisPieces[randomIndex])
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    app.fallingPieceLocation = [0,
        app.cols // 2 - len(app.fallingPiece[0]) // 2] #row, col

#draw falling piece
def drawFallingPiece(app, canvas):
    for i in range(len(app.fallingPiece)):
        for j in range(len(app.fallingPiece[0])):
            if app.fallingPiece[i][j]:
                drawCell(app, canvas, app.fallingPieceLocation[0] + i, 
                    app.fallingPieceLocation[1] + j, app.fallingPieceColor)

#draws cell
def drawCell(app, canvas, row, col, color):
    cellWidth = (app.width - app.margin * 2) / app.cols
    cellHeight = (app.height - app.margin * 2) / app.rows
    x1 = app.margin + cellWidth * col
    y1 = app.margin + cellHeight * row
    canvas.create_rectangle(x1, y1, x1 + cellWidth, y1 + cellHeight,
        fill=color, width=5)

#initialization
def appStarted(app):
    app.timerDelay = 350
    app.rows = 15
    app.cols = 10
    app.margin = 35

    init(app)
    initPieces(app)

#board draw
def drawBoard(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="orange", width=0)
    for i in range(app.rows):
        for j in range(app.cols):
            drawCell(app, canvas, i, j, app.board[i][j])
def drawScore(app, canvas):
    canvas.create_text(app.width / 2, app.margin / 2,
        text=f"Score: {app.score}", fill="blue",
        anchor="center", font="Ariel 25 bold")
def drawGameOver(app, canvas):
    if app.gameOver:
        canvas.create_rectangle(app.margin, 50 + app.margin,
            app.width - app.margin, 150 + app.margin, fill="black")
        canvas.create_text(app.width / 2, app.margin + 100,
            text="Game Over!", fill="white",
            anchor="center", font="Ariel 30 bold")

#redraws all
def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawFallingPiece(app, canvas)
    drawScore(app, canvas)
    drawGameOver(app, canvas)

def doStep(app):
    #simulate downwards
    if checkPieceLegal(app, app.fallingPiece,
        [app.fallingPieceLocation[0] + 1, app.fallingPieceLocation[1]]):
        app.fallingPieceLocation[0] += 1
        return True
    else:
        for i in range(len(app.fallingPiece)):
            for j in range(len(app.fallingPiece[0])):
                if not app.fallingPiece[i][j]:
                    continue
                app.board[app.fallingPieceLocation[0] + i]\
                [app.fallingPieceLocation[1] + j] = app.fallingPieceColor
        checkFullRows(app)
        newFallingPiece(app)
        if not checkPieceLegal(app, app.fallingPiece,
        [app.fallingPieceLocation[0], app.fallingPieceLocation[1]]):
            app.gameOver = True

        return False

def timerFired(app):
    if app.gameOver:
        return

    doStep(app)
    

def checkFullRows(app):
    for row in range(app.rows):
        while "blue" not in app.board[row]:
            app.score += 1
            app.board.pop(row)
            app.board.insert(0, ["blue" for i in range(app.cols)])

#checks if block is occupied or out of range
def canMoveblock(app, row, col):
    #print(row, col)
    if row < 0 or row >= app.rows or col < 0 or col >= app.cols:
        #print("bounded")
        return False

    return app.board[row][col] == "blue"

def checkPieceLegal(app, piece, tempLocation):
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] and not canMoveblock(app,
                tempLocation[0] + i,
                tempLocation[1] + j):

                return False
    return True

def rotatePiece(app):
    piece = app.fallingPiece
    newPiece = []
    for i in range(len(piece[0])):
        newPiece.append([])
        for j in range(len(piece)):
            newPiece[i].append(False)

    #invert rows/cols
    for i in range(len(newPiece)):
        for j in range(len(newPiece[0])):
            #if the rotation is illegal exit now
            rev = list(reversed(piece[j]))
            newPiece[i][j] = rev[i]

    tempLocation = copy.copy(app.fallingPieceLocation)
    tempLocation[1] += len(piece[0]) // 2 - len(newPiece[0]) // 2
    tempLocation[0] += len(piece) // 2 - len(newPiece) // 2

    if checkPieceLegal(app, newPiece, tempLocation):
        app.fallingPiece = newPiece
        app.fallingPieceLocation = tempLocation

def keyPressed(app, event):
    if event.key == "r":
        appStarted(app)
        return

    if app.gameOver:
        return

    if event.key == "Space":
        while doStep(app):
            pass

    moveX, moveY = 0, 0

    if event.key == "Up":
        rotatePiece(app)
    if event.key == "Down":
        moveY = 1
    if event.key == "Left":
        moveX = -1
    if event.key == "Right":
        moveX = 1

    canMove = True
    for i in range(len(app.fallingPiece)):
        for j in range(len(app.fallingPiece[0])):
            #check if the cell is blocked
            if app.fallingPiece[i][j] and not\
            canMoveblock(app, app.fallingPieceLocation[0] + i + moveY,
                app.fallingPieceLocation[1] + j + moveX):
                canMove = False
    if canMove:
        app.fallingPieceLocation = [app.fallingPieceLocation[0] + moveY,
            app.fallingPieceLocation[1] + moveX]


#################################################
# main
#################################################

def main():
    cs112_n22_week4_linter.lint()
    playTetris()

if __name__ == '__main__':
    main()
