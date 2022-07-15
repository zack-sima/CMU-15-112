#################################################
# hw4.py
# name: Zack
# andrew id: ysima
#################################################

import cs112_n22_week2_linter
import math, string

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

def rgbString(red, green, blue):
     return f'#{red:02x}{green:02x}{blue:02x}'

#################################################
# hw4-standard-functions
#################################################

#draws a square-grid pattern
def drawPattern1(canvas, width, height, points):
    hSpace = width / (points - 1)
    vSpace = height / (points - 1)
    #lines going down and right
    for i in range(points - 1):
        canvas.create_line(hSpace * i, 0, width, height - vSpace * i)
    for i in range(1, points - 1):
        canvas.create_line(0, vSpace * i, width - hSpace * i, height)
    #lines going up and right
    for i in range(points - 1):
        canvas.create_line(hSpace * i, height, width, vSpace * i)
    for i in range(1, points - 1):
        canvas.create_line(0, height - vSpace * i, width - hSpace * i, 0)

#makes a "nice" robot with different shapes
def drawNiceRobot(canvas, width, height):
    centerX, centerY = width / 2, height / 2
    canvas.create_line(centerX - width / 3, centerY - height / 10,
        centerX + width / 3, centerY - height / 10)
    canvas.create_rectangle(centerX - width / 10, centerY - height / 3,
        centerX + width / 10, centerY - height / 5, fill="orange")
    canvas.create_oval(centerX - width / 10, centerY - height / 5,
        centerX + width / 10, centerY, fill="green")
    canvas.create_polygon(centerX - width / 10, centerY - height / 10,
        centerX + width / 10, centerY - height / 10,
        centerX, centerY + height / 5, fill="blue")
    canvas.create_rectangle(centerX - width / 13, centerY - height / 3.8,
        centerX - width / 20, centerY - height / 3.6, fill="red")
    canvas.create_rectangle(centerX + width / 20, centerY - height / 3.8,
        centerX + width / 13, centerY - height / 3.6, fill="red")
    canvas.create_rectangle(centerX - width / 10, centerY + height / 10,
        centerX + width / 10, centerY + height / 5, fill="yellow")
    canvas.create_rectangle(centerX - width / 13, centerY + height / 7,
        centerX - width / 20, centerY + height / 2, fill="red")
    canvas.create_rectangle(centerX + width / 20, centerY + height / 7,
        centerX + width / 13, centerY + height / 2, fill="red")
    canvas.create_rectangle(centerX - width / 13, centerY - height / 5,
        centerX + width / 13, centerY - height / 4.5, fill="red")

#draws the flag of Qutar with 8 triangles and two rects
def drawFlagOfQatar(canvas, x0, y0, x1, y1):
    xDif = x1 - x0
    yDif = y1 - y0

    canvas.create_rectangle(x0, y0, x1, y1, fill='#8A1538')
    canvas.create_rectangle(x0, y0, x0 + xDif / 3, y1, fill="white")

    #8 triangles
    for i in range(8):
        canvas.create_polygon(x0 + xDif / 3, y0 + yDif / 8 * i, 
            x0 + xDif / 3, y0 + yDif / 8 * (i + 1), 
            x0 + xDif / 3 + xDif / 10, y0 + yDif / 8 * (i + 0.5), fill="white")

#################################################
# hw4-bonus-functions
# these are optional
#################################################


def drawPattern2(canvas, width, height, points):
    return 42

def drawFancyWheels(canvas, width, height, rows, cols):
    return 42


#################################################
# Test Functions
#################################################

def testDrawPattern1(app, canvas):
    drawPattern1(canvas, app.width, app.height, app.points)
    canvas.create_text(app.width/2, app.height-10, 
          text=('testing drawPattern1' + 
            f'(canvas, {app.width}, {app.height}, {app.points})'))

def testDrawPattern2(app, canvas):
    drawPattern2(canvas, app.width, app.height, app.points)
    canvas.create_text(app.width/2, app.height-10, 
          text=('testing drawPattern2' + 
            f'(canvas, {app.width}, {app.height}, {app.points})'))

def testDrawFlagOfQatar(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='lightYellow')
    drawFlagOfQatar(canvas, 50, 125, 350, 275)
    drawFlagOfQatar(canvas, 425, 100, 575, 200)
    drawFlagOfQatar(canvas, 450, 275, 550, 325)
    canvas.create_text(app.width/2, app.height-20, 
          text="Testing drawFlagOfQatar")
    canvas.create_text(app.width/2, app.height-10, 
          text="This does not need to resize properly!")


def testDrawNiceRobot(app, canvas):
    drawNiceRobot(canvas, app.width, app.height)
    canvas.create_text(app.width/2, app.height-20, 
          text=('Testing drawNiceRobot' +
            f'(canvas, {app.width}, {app.height})'))
    canvas.create_text(app.width/2, app.height-10, 
          text=f'''Comment out these print lines if they mess up your art!''')

def testDrawFancyWheels(app, canvas, rows, cols):
    drawFancyWheels(canvas, app.width, app.height, rows, cols)
    canvas.create_text(app.width/2, app.height-10, 
          text=('testing drawFancyWheels' + 
            f'(canvas, {app.width}, {app.height}, {rows}, {cols})'))


def drawSplashScreen(app, canvas):
    text = f"""
Press the number key for the 
exercise you would like to test!

1. drawPattern1 ({app.points} points)
2. drawNiceRobot
3. drawFlagOfQatar

4. Bonus drawPattern2 ({app.points} points)
5. Bonus drawFancyWheels (1x1)
6. Bonus drawFancyWheels (4x6)


You can press the up or down arrows to change
the number of points for drawPattern1
and drawPattern2 between 3 and 20
"""

    textSize = min(app.width,app.height) // 40
    canvas.create_text(app.width/2, app.height/2, text=text,
                        font=f'Arial {textSize} bold')


def appStarted(app):
    app.lastKeyPressed = None
    app.points = 5
    app.timerDelay = 10**10

def keyPressed(app, event):
    if event.key == "Up":
      app.points = min(20, app.points+1)
      print(f"Increasing points to {app.points}")
      if app.points >= 20: print("Maximum allowed points!")
    elif event.key == "Down":
      app.points = max(3, app.points-1)
      print(f"Decreasing points to {app.points}")
      if app.points <= 3: print("Minimum allowed points!")
    else:
      app.lastKeyPressed = event.key





def redrawAll(app, canvas):
    if app.lastKeyPressed == "1":
      testDrawPattern1(app, canvas)
    elif app.lastKeyPressed == "2":
      testDrawNiceRobot(app, canvas)
    elif app.lastKeyPressed == "3":
      testDrawFlagOfQatar(app, canvas)
    elif app.lastKeyPressed == "4":
      testDrawPattern2(app, canvas)
    elif app.lastKeyPressed == "5":
      testDrawFancyWheels(app, canvas, 1, 1)
    elif app.lastKeyPressed == "6":
      testDrawFancyWheels(app, canvas, 4, 6)
    else:
      drawSplashScreen(app, canvas)

#################################################
# main
#################################################

def main():
    cs112_n22_week2_linter.lint()
    runApp(width=600, height=600)

if __name__ == '__main__':
    main()
