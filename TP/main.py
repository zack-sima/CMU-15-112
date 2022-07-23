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

class Tile:
    def __init__(self, app, x, y):
        self.app = app
        self.x = x
        self.y = y
        self.coordinates = (x, y)
        self.isWall = False

        #pathfinding: points to tile that goes here
        #note: since there isn't terrain, all costs are equal
        #   so there's no need to specify current cost
        self.pointToTile = None

    def __repr__(self):
        return f"Tile at ({self.x}, {self.y})"

    def toggleWall(self):
        self.isWall = not self.isWall

    # ------ pathfinding helpers ------
    @staticmethod
    def resetPathfindingPointers(app):
        for col in app.tiles:
            for tile in col:
                tile.pointToTile = None

    @staticmethod
    def getTileNeighbors(app, tile):
        neighbors = []
        if tile.x > 0:
            neighbors.append(app.tiles[tile.x - 1][tile.y])
        if tile.x < app.tileCols - 1:
            neighbors.append(app.tiles[tile.x + 1][tile.y])
        if tile.y > 0:
            neighbors.append(app.tiles[tile.x][tile.y - 1])
        if tile.y < app.tileRows - 1:
            neighbors.append(app.tiles[tile.x][tile.y + 1])
        return neighbors

    #pathfinds to the tile, avoidoing walls
    #my own floodfill pathfind implementation
    def pathFindToTile(self, target):
        Tile.resetPathfindingPointers(self.app)
        currentTiles = [self]
        while True:
            newTiles = []

            #if this is true after searching, it means pathfinding failed
            noNewTiles = True

            for tile in currentTiles:
                for checkTile in Tile.getTileNeighbors(self.app, tile):
                    if checkTile == target:
                        #target found, recursively add pointers to path and return
                        print("found target!")

                        target.pointToTile = tile
                        path = []
                        pointer = target

                        while pointer != self:
                            path.append(pointer)
                            pointer = pointer.pointToTile

                            if pointer == None: #should never happen
                                print("pathfinding broken")
                                break

                        path.reverse() #reversed list goes from start to finish

                        #print(path)
                        return path
                    if not checkTile.isWall and checkTile.pointToTile == None\
                    and checkTile != self:
                        #hasn't been assigned to a tile yet
                        checkTile.pointToTile = tile
                        newTiles.append(checkTile)
                        noNewTiles = []

            #print(newTiles)

            if noNewTiles:
                print("pathfinding failed")
                return []

            #replaces current tiles so next iteration can search
            currentTiles = newTiles

def appStarted(app):
    app.tileCols, app.tileRows = 10, 10

    init(app)

def init(app):
    app.pathway = [] #temporary enemy pathway

    app.deleteWalls = False #keypress trigger

    app.tiles = []
    for i in range(app.tileCols):
        app.tiles.append([])
        for j in range(app.tileRows):
            #new tile
            t = Tile(app, i, j)
            app.tiles[i].append(t)

    app.entrance = app.tiles[0][app.tileRows // 2]
    app.exit = app.tiles[app.tileCols - 1][app.tileRows // 2]
    calculatePath(app)

def calculatePath(app):
    app.pathway = app.entrance.pathFindToTile(app.exit)

def timerFired(app):
    pass

def mouseEvent(app, event): #helper called by both drag and press
    col, row = getTileFromMousePos(app, event.x, event.y)
    if col != -1 and (col, row) != app.entrance.coordinates and\
    (col, row) != app.exit.coordinates:
        if (not app.tiles[col][row].isWall and not app.deleteWalls) or\
        (app.tiles[col][row].isWall and app.deleteWalls):
            app.tiles[col][row].toggleWall()
            calculatePath(app)

def mouseDragged(app, event):
    mouseEvent(app, event)

def mousePressed(app, event):
    mouseEvent(app, event)


def keyPressed(app, event):
    if event.key == "x":
        app.deleteWalls = not app.deleteWalls

    if event.key == "Left" and app.tileCols > 5:
        app.tileCols -= 1
        app.tileRows -= 1
        init(app)
    if event.key == "Right" and app.tileCols < 100:
        app.tileCols += 1
        app.tileRows += 1
        init(app)

#both use height for square grid
def getTileWidth(app):
    return app.width / app.tileCols

def getTileHeight(app):
    return app.height / app.tileRows

def getTileFromMousePos(app, x, y):
    col = min(int(x / getTileWidth(app)), app.tileCols - 1)
    row = min(int(y / getTileHeight(app)), app.tileRows - 1)
    return col, row

def redrawAll(app, canvas):
    #background
    canvas.create_rectangle(0, 0, app.width, app.height, fill="black", width=0)

    tileWidth, tileHeight = getTileWidth(app), getTileHeight(app)
    tileMargin = app.width / 300 #space between tiles

    for col in app.tiles:
        for tile in col:
            x1 = tileWidth * tile.x + tileMargin
            x2 = tileWidth * (tile.x + 1) - tileMargin
            y1 = tileHeight * tile.y + tileMargin
            y2 = tileHeight * (tile.y + 1) - tileMargin

            color = "gray"
            if tile == app.entrance:
                color = "green"
            elif tile == app.exit:
                color = "red"
            elif tile.isWall:
                color = "white"
            elif tile in app.pathway:
                color = "blue"
            

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

def main():
    runApp(width=700, height=700)

if __name__ == '__main__':
    main()