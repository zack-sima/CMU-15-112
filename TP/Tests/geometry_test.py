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

class Rectangle:
    #center: (x, y); if parent exists, all x and y are local
    #the higher the layer, the later it is rendered (thus on top)
    #   when adding this object to the list of rendered objects,
    #   add it to the right layer order (do a binary search of list)
    def __init__(self, x, y, width, height,
        rotation=0, layer=0, parent=None, color="black", name="rectangle"):

        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.parent = parent
        self.rotation = rotation
        self.spawnTime = time.time()

        if parent != None:
            self.globalRotation = parent.globalRotation + rotation
            self.globalX = parent.globalX + x
            self.globalY = parent.globalY + y
        else:
            self.globalRotation = rotation
            self.globalX = x
            self.globalY = y
        self.layer = layer
        self.color = color

    def translate(self, x, y, local=True):
        if not local:
            #just add straight to the local position without considering rotation
            self.x += x
            self.y += y
        else:
            self.x += x * math.cos(-self.globalRotation * math.pi / 180) + \
            y * math.cos((-self.globalRotation + 90) * math.pi / 180)

            self.y += x * math.sin(-self.globalRotation * math.pi / 180) + \
            y * math.sin((-self.globalRotation + 90) * math.pi / 180)
            self.updateGlobalPosition()

    #makes the right side of the rectangle look towards given coords
    def lookAt(self, x, y):
        dx = x - self.globalX
        dy = y - self.globalY

        if almostEqual(dx, 0): #atan(dy/0) = 90
            if dy < 0:
                self.rotation = 90
            else:
                self.rotation = -90

            return

        self.rotation = math.atan(dy / dx) * -180 / math.pi

        if dx < 0:
            self.rotation += 180

        self.updateGlobalRotation()

    def updateGlobalPosition(self):
        #if object has parents, x and y need to be rotated according to parent
        if self.parent != None:
            dx, dy = self.x, self.y
            dr = (dx ** 2 + dy ** 2) ** 0.5

            self.globalX = self.parent.globalX + dr * math.cos(-self.parent.globalRotation * math.pi / 180)
            self.globalY = self.parent.globalY + dr * math.sin(-self.parent.globalRotation * math.pi / 180)
        else:
            self.globalX = self.x
            self.globalY = self.y


    def updateGlobalRotation(self):
        if self.parent != None:
            self.globalRotation = self.parent.globalRotation + self.rotation
        else:
            self.globalRotation = self.rotation

    def rotate(self, degree):
        self.rotation += degree

        #normalize rotation
        while self.rotation < 0:
            self.rotation += 360

        self.rotation = self.rotation % 360
        self.updateGlobalRotation()

    def render(self, app, canvas):
        self.updateGlobalRotation()
        self.updateGlobalPosition()

        topLeft = (self.globalX - self.width / 2, self.globalY - self.height / 2)
        topRight = (self.globalX + self.width / 2, self.globalY - self.height / 2)
        bottomLeft = (self.globalX - self.width / 2, self.globalY + self.height / 2)
        bottomRight = (self.globalX + self.width / 2, self.globalY + self.height / 2)
        points = [topLeft, topRight, bottomRight, bottomLeft]

        rotatedPoints = []
        for p in points:
            x = p[0] - self.globalX
            y = p[1] - self.globalY

            #pythagorean theorem
            r = (x ** 2 + y ** 2) ** 0.5

            #the offset of the point compared to center
            offsetRad = math.pi / 2
            if not almostEqual(y, 0): #atan x/y
                offsetRad = math.atan(x / y)

            #differentiate between different quadrants for atan
            if y < 0:
                offsetRad += math.pi

            newX = self.globalX + (math.sin(self.globalRotation * math.pi / 180 + offsetRad) * r)
            newY = self.globalY + (math.cos(self.globalRotation * math.pi / 180 + offsetRad) * r)

            rotatedPoints.extend([newX, newY])

        canvas.create_polygon(rotatedPoints, fill=self.color)


def instantiate(app, obj):
    if app.renderedObjects.get(obj.layer) == None:
        app.renderedObjects[obj.layer] = []

    app.renderedObjects[obj.layer].append(obj)

def appStarted(app):
    app.timerDelay = 20

    app.bulletDelay = 0

    app.renderedObjects = {} #key is layer, value is list

    app.wDown, app.sDown, app.aDown, app.dDown = False, False, False, False

    app.turret = Rectangle(x=app.width / 2, y=app.height / 2,
        width=100, height=80, color="orange", layer=2)
    app.turretHead = Rectangle(x=app.turret.width / 2 + 20, y=0,
        width=50, height=30, color="black", parent=app.turret, layer=1)
    # app.turretMuzzle = Rectangle(x=app.turretHead.width / 2 + 7, y=0,
    #     width=12, height=30, color="yellow", parent=app.turretHead)

    app.enemy = Rectangle(x=app.width, y=app.height / 2,
        width=50, height=50, color="red", layer=0)

    app.bullets = []

    instantiate(app, app.turret)
    instantiate(app, app.turretHead)
    instantiate(app, app.enemy)

    # instantiate(app, app.turretMuzzle)

def timerFired(app):
    app.turret.lookAt(app.enemy.x, app.enemy.y)
    app.bulletDelay -= app.timerDelay / 1000
    if app.bulletDelay < 0:
        app.bulletDelay = 0.07
        bullet = Rectangle(x=app.turretHead.globalX, y=app.turretHead.globalY,
            rotation=app.turret.rotation, width=30, height=10, color="brown", layer=0)
        bullet.translate(30, 0)

        app.bullets.append(bullet)
        instantiate(app, bullet)

    i = 0
    while i < len(app.bullets):
        app.bullets[i].translate(app.timerDelay / 1000 * 550, 0)
        if time.time() - app.bullets[i].spawnTime > 2:
            deletedBullet = app.bullets[i]
            app.bullets.remove(deletedBullet)
            app.renderedObjects[deletedBullet.layer].remove(deletedBullet)

            del deletedBullet
        i += 1


    if app.wDown:
        app.enemy.translate(app.timerDelay / 1000 * 25, 0)
    if app.sDown:
        app.enemy.translate(app.timerDelay / 1000 * -25, 0)
    if app.aDown:
        app.enemy.translate(0, app.timerDelay / 1000 * -25)
    if app.dDown:
        app.enemy.translate(0, app.timerDelay / 1000 * 25)

def mousePressed(app, event):
    app.enemy.x, app.enemy.y = event.x, event.y
    #app.turret.lookAt(event.x, event.y)

def mouseDragged(app, event):
    app.enemy.x, app.enemy.y = event.x, event.y
    #app.turret.lookAt(event.x, event.y)

def keyPressed(app, event):
    if event.key == "w":
        print("pressed")
        app.wDown = True
    if event.key == "s":
        app.sDown = True
    if event.key == "a":
        app.aDown = True
    if event.key == "d":
        app.dDown = True

#NOTE: not working properly
def keyReleased(app, event):
    if event.key == "w":
        print("released")
        app.wDown = False
    if event.key == "s":
        app.sDown = False
    if event.key == "a":
        app.aDown = False
    if event.key == "d":
        app.dDown = False

def redrawAll(app, canvas):
    #check all layers
    layers = sorted(list(app.renderedObjects.keys()))
    for i in layers:
        while None in app.renderedObjects[i]:
            #remove none objects
            app.renderedObjects[i].remove(None)

        for j in app.renderedObjects[i]:
            j.render(app, canvas)

def main():
    runApp(width=700, height=700)

if __name__ == '__main__':
    main()