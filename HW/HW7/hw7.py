#################################################
# hw7: One-Dimensional Connect Four
# name: Zack
# andrew id: ysima
# 
#################################################

import cs112_n22_week3_linter
from cmu_112_graphics import *
import random, string, math, time

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# main app
#################################################

def init(app):
    #element eg: False = green, True = blue
    app.dots = []
    app.selection = -1 #-1 means not selected
    app.outlineWidth = 6
    app.minDots = 6
    app.maxDots = 20
    app.gameOver = False
    app.winStreakIndex = -1 #the first tile where the strikethrough goes
    app.invalidSelection = -1 #when not -1, show corresponding message
    app.invalidSelectionTexts = [
    "Block must contain current player",
    "End cannot be in block"] 
    app.playerDotOffset = 210
    app.titleOffset = 20
    app.descriptionOffset = 55

    random.seed = time.time()
    startOnBlue = random.randint(0, 1)

    app.player = startOnBlue == 1 #True is blue, False is green

    for i in range(app.dotCount):
        if startOnBlue and i % 2 == 0 or\
        not startOnBlue and i % 2 == 1:
            app.dots.append(True)
        else:
            app.dots.append(False)

def appStarted(app):
    app.dotCount = 10

    init(app)

#check if one player has won
def checkForWin(app):
    #check for all possible combinations
    for i in range(len(app.dots) - 3):
        #either all green or all blue
        if app.dots[i] and app.dots[i + 1] and\
        app.dots[i + 2] and app.dots[i + 3] or\
        not app.dots[i] and not app.dots[i + 1] and\
        not app.dots[i + 2] and not app.dots[i + 3]:
            #win game
            app.gameOver = True
            app.winStreakIndex = i
            return

def colorAllSelected(app, s): #helper-fn, debug
    if s < 2 or s > app.dotCount - 3:
        return False

    app.dots[s - 1] = app.dots[s]
    app.dots[s + 1] = app.dots[s]

def checkSelectionValid(app, s): #helper-fn
    if s < 2 or s > app.dotCount - 3:
        return False

    if app.dots[s - 1] != app.player and app.dots[s] != app.player and\
    app.dots[s + 1] != app.player:
        return False

    return True

def distance(x1, y1, x2, y2): #helper-fn
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def getMouseCell(app, x, y):
    cellRadius = app.width / app.dotCount / 2
    dotMargin = cellRadius / 5
    dotRadius = cellRadius - dotMargin
    if y < app.height / 2 - dotRadius or\
    y > app.height / 2 + dotRadius:
        return -1

    #check that cell distance is within radius then return cell
    cell = int(x / (app.width / app.dotCount))
    print(x, y, (cell + 0.5) * cellRadius * 2, app.height / 2)
    if distance(x, y, (cell + 0.5) * cellRadius * 2,
        app.height / 2) < dotRadius:
        return cell
    else:
        return -1

def mousePressed(app, event):
    if app.gameOver:
        return

    mouseIndex = getMouseCell(app, event.x, event.y)

    if mouseIndex > 1 and mouseIndex < app.dotCount - 2:
        if checkSelectionValid(app, mouseIndex):
            app.selection = mouseIndex
            #remove invalid selection texts after sucessful click
            app.invalidSelection = -1
        else:
            #block must contain own color
            app.invalidSelection = 0
    elif mouseIndex != -1 and (app.selection == -1 or\
        mouseIndex != 0 and mouseIndex != app.dotCount - 1):
        #block must not contain endpoints
        app.invalidSelection = 1

    elif app.selection != -1 and\
    (mouseIndex == 0 or mouseIndex == app.dotCount - 1):
        temp = (app.dots[app.selection - 1], app.dots[app.selection],
                app.dots[app.selection + 1])
        #delete current games
        for i in range(3):
                app.dots.pop(app.selection - 1)
        if mouseIndex == 0: #move all to left end
            for i in reversed(temp):
                app.dots.insert(0, i)
        elif mouseIndex == app.dotCount - 1:
            #move all to right end
            for i in temp:
                app.dots.append(i)

        #switch player
        app.player = not app.player
        app.selection = -1
        app.invalidSelection = -1 

        checkForWin(app)

#key events
def keyPressed(app, event):
    #restart
    if event.key == "r":
        init(app)

    #change player
    if event.key == "p":
        app.player = not app.player

    #resize game & reset
    if event.key == "Left" or event.key == "Down":
        if app.dotCount > app.minDots:
            app.dotCount -= 2
            init(app)
    if event.key == "Right" or event.key == "Up":
        if app.dotCount < app.maxDots:
            app.dotCount += 2
            init(app)

    if app.gameOver:
        return

    if event.key == "c" and app.selection != -1:
        colorAllSelected(app, app.selection)

#renderer
def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawTitle(app, canvas)
    drawInstructions(app, canvas)
    drawCurrentPlayerAndMessage(app, canvas)
    drawRules(app, canvas)
    drawPlayerDot(app, canvas)

#title
def drawTitle(app, canvas):
    canvas.create_text(app.width / 2, app.titleOffset, anchor="n",
        text="One-Dimensional Connect Four!", font="Helvetica 30 bold")

#instructions
def drawInstructions(app, canvas):
    messages = ['See rules below.',
                'Click interior piece to select center of 3-piece block.',
                'Click end piece to move that block to that end.',
                'Change board size (and then restart) with arrow keys.',
                'For debugging, press c to set the color of selected block.',
                'For debugging, press p to change the current player.',
                'Press r to restart.',
               ]
    

    offset = 0
    for m in messages:
        canvas.create_text(app.width / 2, app.descriptionOffset + offset,
        text=m, font="Helvetica 16 bold", anchor="n")
        offset += 18

#rules
def drawRules(app, canvas):
    messages = [
  "The Rules of One-Dimensional Connect Four:",
  "Arrange N (10 by default) pieces in a row of alternating colors.",
  "Players take turns to move three pieces at a time, where:",
  "      The pieces must be in the interior (not on either end)",
  "      The pieces must be adjacent (next to each other).",
  "      At least one moved piece must be the player's color.",
  "The three pieces must be moved in the same order to either end of the row.",
  "The gap must be closed by sliding the remaining pieces together.",
  "The first player to get four (or more) adjacent pieces of their color wins!",
               ]
    canvas.create_text(10, app.height - 10,
        text="\n".join(messages), font="Helvetica 16 bold", anchor="sw")

#helper-fn
def getColors(app):
    color = "light green"
    outlineColor = "green"
    if app.player:
        color = "light blue"
        outlineColor = "blue"
    return color, outlineColor

#draws text near player dot
def drawCurrentPlayerAndMessage(app, canvas):
    color, outlineColor = getColors(app)

    textOffset = 30
    canvas.create_text(app.width / 2 - textOffset, app.playerDotOffset,
        text="Current Player:", anchor="e", fill=outlineColor,
        font="Helvetica 18 bold")

    instructionsText = "Select your 3-piece block"
    if app.gameOver:
        instructionsText = "Game Over!!!!!"
    elif app.invalidSelection != -1:
        instructionsText = app.invalidSelectionTexts[app.invalidSelection]
    elif app.selection != -1:
        instructionsText = "Select end to move block"

    canvas.create_text(app.width / 2 + textOffset, app.playerDotOffset,
        text=instructionsText, anchor="w", fill=outlineColor,
        font="Helvetica 18 bold")

#player dot at the top
def drawPlayerDot(app, canvas):
    color, outlineColor = getColors(app)
    dRad = 15 #dot radius
    dOutline = 4 #dot outline

    canvas.create_oval(app.width / 2 - dRad + dOutline,
        app.playerDotOffset - dRad + dOutline,
        app.width / 2 + dRad - dOutline,
        app.playerDotOffset + dRad - dOutline,
        fill=color, width=dOutline, outline=outlineColor)

#board of pieces to be used plus win strikethrough
def drawBoard(app, canvas):
    cellRadius = app.width / app.dotCount / 2
    dotMargin = cellRadius / 5 #leave a bit of whitespace

    for i in range(len(app.dots)):
        color = "light green"
        outlineColor = "green"
        if app.dots[i]:
            color = "light blue"
            outlineColor = "blue"
        x1, x2 = getCellBounds(app, i)

        #selection
        if app.selection != -1 and abs(app.selection - i) <= 1:
            canvas.create_rectangle(x1, app.height / 2 - cellRadius,
                x2, app.height / 2 + cellRadius, fill="orange", width=0)

        #inner circle
        canvas.create_oval(x1 + dotMargin + app.outlineWidth, 
            app.height / 2 - cellRadius + dotMargin + app.outlineWidth,
            x2 - dotMargin - app.outlineWidth,
            app.height / 2 + cellRadius - dotMargin - app.outlineWidth, 
            fill=color, width=app.outlineWidth, outline=outlineColor)

        #win strikethrough
        if app.gameOver:
            x1, x2 = getCellBounds(app, app.winStreakIndex)
            xStart = x1 + (x2 - x1) / 2
            xEnd = x1 + (x2 - x1) * 3.5,
            canvas.create_line(xStart, app.height / 2, 
                xEnd, app.height / 2, width=5)

#helpers
def getCellBounds(app, x):
    return app.width / app.dotCount * x, app.width / app.dotCount * (x + 1)

def main():
    cs112_n22_week3_linter.lint()
    runApp(width=800, height=550)

if __name__ == '__main__':
    main()