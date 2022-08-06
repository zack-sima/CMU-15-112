import random, string, math, time

class UIObject:
    def __init__(self, app, x, y):
        self.isActive = True
        self.x = x
        self.y = y

        app.uiObjects.append(self)

    def render(self, app, canvas):
        pass

    def setActive(boolean):
        self.isActive = isActive

class Text(UIObject):
    def __init__(self, app, x, y, text, font="Helvetica 15 bold",
        anchor="center", color="black", alignment="center"):
        super().__init__(app, x, y)
        
        self.font = font
        self.text = text
        self.anchor = anchor
        self.color = color
        self.alignment = alignment

        app.uiObjects.append(self)

    def render(self, app, canvas):
        canvas.create_text(self.x, self.y, text=self.text,
            font=self.font, anchor=self.anchor, fill=self.color, justify=self.alignment)

class Rectangle(UIObject):
    def __init__(self, app, x, y, width, height, color="black", outline=0):
        super().__init__(app, x, y)

        self.width = width
        self.height = height
        self.color = color
        self.outline = outline

    def render(self, app, canvas):
        canvas.create_rectangle(self.x - self.width / 2, self.y - self.height / 2,
            self.x + self.width / 2, self.y + self.height / 2, fill=self.color, width=self.outline)

class Button(UIObject):
    def __init__(self, app, x, y, width, height, color="black", dimColor="", outlineWidth=0, outlineColor="", outlineDimColor="",
        text="", textColor="black", textAlignment="center", textFont="Helvetica 15 bold", clickCallback=None, releaseCallback=None, bid=0):
        super().__init__(app, x, y)

        #note: b-id is for identifying buttons in callback
        self.bid = bid
        self.width = width
        self.height = height
        self.color = color
        self.currentColor = color
        self.textColor = textColor

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
        self.outlineWidth = outlineWidth
        self.outlineColor = outlineColor
        self.outlineDimColor = outlineDimColor
        self.currentOutlineColor = outlineColor

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
            self.currentOutlineColor = self.outlineDimColor

            self.clickedInSelf = True
            if self.clickCallback != None:
                self.clickCallback(app, self)

    def onRelease(self, app, event):
        if self.mouseInSelf(event.x, event.y):
            if self.releaseCallback != None and self.clickedInSelf:
                #callback functions will always have app and button params
                self.releaseCallback(app, self)

        self.currentOutlineColor = self.outlineColor
        self.currentColor = self.color
        self.clickedInSelf = False

    #destroys this object from both memory and render list
    def destroy(self):
        app.uiObjects.remove(self)
        del self

    def render(self, app, canvas):
        canvas.create_rectangle(self.x - self.width / 2, self.y - self.height / 2,
            self.x + self.width / 2, self.y + self.height / 2, fill=self.currentColor, width=self.outlineWidth,
            outline=self.currentOutlineColor)
        canvas.create_text(self.x, self.y, text=self.text, fill=self.textColor, anchor=self.textAlignment, justify="center", font=self.textFont)

def init(app):
    app.uiObjects = []

def renderAll(app, canvas):
    for i in app.uiObjects:
        if i.isActive:
            i.render(app, canvas)

def mouseDown(app, event):
    for i in app.uiObjects:
        if isinstance(i, Button) and i.isActive:
            i.onClick(app, event)
def mouseUp(app, event):
    for i in app.uiObjects:
        if isinstance(i, Button) and i.isActive:
            i.onRelease(app, event)