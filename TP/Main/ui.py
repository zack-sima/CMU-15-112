import random, string, math, time

class Button:
    def __init__(self, x, y, width, height, color="black", dimColor="", outline=0,
        text="", textAlignment="center", textFont="Helvetica 15 bold", clickCallback=None, releaseCallback=None, bid=0):

        #note: b-id is for identifying buttons in callback
        self.bid = bid

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.currentColor = color

        if dimColor == "":
            self.dimColor = color
        else:
            self.dimColor = dimColor

        self.clickCallback = clickCallback
        self.releaseCallback = releaseCallback
        self.clickedInSelf = False
        self.text = text
        self.textAlignment = textAlignment
        self.textFont = textFont
        self.outline = outline

    #mouse inside of button coords
    def mouseInSelf(self, x, y):
        if x > self.x - self.width / 2 and x < self.x + self.width / 2 and\
        y > self.y - self.height / 2 and y < self.y + self.height / 2:
            return True
        return False

    #called via mouse functions in main to mouseDown and mouseUp
    def onClick(self, app, event):
        if self.mouseInSelf(event.x, event.y):
            self.currentColor = self.dimColor
            self.clickedInSelf = True
            if self.clickCallback != None:
                self.clickCallback(app, self)

    def onRelease(self, app, event):
        if self.mouseInSelf(event.x, event.y):
            if self.releaseCallback != None and self.clickedInSelf:
                #callback functions will always have app and button params
                self.releaseCallback(app, self)

        self.currentColor = self.color
        self.clickedInSelf = False

    #destroys this object from both memory and render list
    def destroy(self):
        app.uiObjects.remove(self)
        del self

    def render(self, app, canvas):
        canvas.create_rectangle(self.x - self.width / 2, self.y - self.height / 2,
            self.x + self.width / 2, self.y + self.height / 2, fill=self.currentColor)
        canvas.create_text(self.x, self.y, text=self.text, anchor=self.textAlignment, justify="center", font=self.textFont)


def instantiate(app, obj):
    app.uiObjects.append(obj)

def init(app):
    app.uiObjects = []

def renderAll(app, canvas):
    for i in app.uiObjects:
        if i != None:
            i.render(app, canvas)

def mouseDown(app, event):
    for i in app.uiObjects:
        if i != None:
            i.onClick(app, event)
def mouseUp(app, event):
    for i in app.uiObjects:
        if i != None:
            i.onRelease(app, event)