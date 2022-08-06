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

def appStarted(app):
    app.timerDelay = 10
    app.rotation = 0 #degrees

    app.topLeft = (app.width / 2 - 100, app.height / 2 - 100)
    app.topRight = (app.width / 2 + 100, app.height / 2 - 100)
    app.bottomLeft = (app.width / 2 - 100, app.height / 2 + 100)
    app.bottomRight = (app.width / 2 + 100, app.height / 2 + 100)

    app.points = [app.topLeft, app.topRight, app.bottomRight, app.bottomLeft]
    app.center = (app.width / 2, app.height / 2)

def timerFired(app):
    #180˚ per second
    app.rotation += app.timerDelay / 1000 * 180

    #normalize rotation
    if app.rotation < 0:
        app.rotation += 360

    app.rotation = app.rotation % 360

def mouseDragged(app, event):
    pass

def mousePressed(app, event):
    pass

def keyPressed(app, event):
    pass

def redrawAll(app, canvas):
    print("----------new----------")
    rotatedPoints = []
    for p in app.points:
        x = p[0] - app.center[0]
        y = p[1] - app.center[1]
        print("x: " + str(x) + ", y: " + str(y))
        r = (x ** 2 + y ** 2) ** 0.5

        offsetRad = math.pi / 2
        if not almostEqual(y, 0): #atan x/y
            offsetRad = math.atan(x / y)

        #we need to differentiate between different quadrants
        if x < 0 and y < 0 or x > 0 and y < 0:
            offsetRad += math.pi


        newX = app.center[0] + (math.sin(app.rotation * math.pi / 180 + offsetRad) * r)
        newY = app.center[1] + (math.cos(app.rotation * math.pi / 180 + offsetRad) * r)


        rotatedPoints.append((newX, newY))

    polygonPoints = []
    for x, y in rotatedPoints:
        polygonPoints.extend([x, y])

    canvas.create_polygon(polygonPoints, fill="black")

    canvas.create_polygon([0, 0, 0, 100, 100, 100, 100, 0], fill="black")
    print(polygonPoints)
    #print(app.points)

    #print(rotatedPoints)

def main():
    runApp(width=700, height=700)

if __name__ == '__main__':
    main()