import random, string, math, time

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

        if math.isclose(dx, 0): #atan(dy/0) = 90
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

    def destroy(self, app):
        app.renderedObjects[self.layer].remove(self)
        del self

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
            if not math.isclose(y, 0): #atan x/y
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
    
def init(app):
    app.renderedObjects = {} #key is layer, value is list

def renderAll(app, canvas):
    #check all layers
    layers = sorted(list(app.renderedObjects.keys()))
    for i in layers:
        while None in app.renderedObjects[i]:
            #remove none objects (should've been removed if destroy was called properly)
            app.renderedObjects[i].remove(None)

        for j in app.renderedObjects[i]:
            j.render(app, canvas)
