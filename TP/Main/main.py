from cmu_112_graphics import *
import random, string, math, time, geometry, ui, enemy, towers

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

            if noNewTiles:
                return []

            #replaces current tiles so next iteration can search
            currentTiles = newTiles

def appStarted(app):
    app.deltaTime = .02 #actual time between current and next
    app.lastCall = time.time()
    app.timerDelay = 1

    app.tileCols, app.tileRows = 15 + 1, 15 #note: last col is wall
    app.rightMargin = 256

    geometry.init(app)
    ui.init(app)
    init(app)
    initRes(app)

def buyTowerDown(app, button):
    app.buyingTower = True
    app.buyingTowerId = button.bid

#initialize resources
def initRes(app):
    app.image1 = app.loadImage("circle.png")

def init(app):
    app.pathway = [] #temporary enemy pathway
    app.deleteWalls = False #keypress trigger
    app.buyingTower = False
    app.buyinTowerId = 0
    app.currentMouseCoords = (0, 0)
    # app.enemySpawnDelay = 3

    app.enemies = []
    app.towers = []

    app.tiles = []
    for i in range(app.tileCols):
        app.tiles.append([])
        for j in range(app.tileRows):
            #new tile
            t = Tile(app, i, j)
            app.tiles[i].append(t)
            if i == app.tileCols - 1:
                t.isWall = True #last col is not seen but all walls


    app.entrance = app.tiles[0][app.tileRows // 2]
    app.exit = app.tiles[app.tileCols - 1][app.tileRows // 2]

    calculatePath(app)

    #------------- add game UI --------------

    #buy towers background
    ui.Rectangle(app, app.width - app.rightMargin / 2, app.height / 2,
        app.rightMargin, app.height, color="#8a4a22")
    ui.Text(app, app.width - app.rightMargin / 2, 25, anchor="n", text="Buy Towers", font="Helvetica 25 bold", color="white")

    #buy tower buttons
    ui.Button(app, app.width - app.rightMargin / 2, 150, 100, 100, color="white", dimColor="lightgreen",
     text="Dart\nTower", textFont="Helvetica 15 bold", clickCallback=buyTowerDown, bid=0)

    #health, speed
    app.enemyTypes = {"red": (5, 1), "blue": (10, 1.5), "green": (15, 2),
    "yellow": (20, 2.5), "black": (30, 1.5), "white": (35, 1.8)}

    #color, number, interval, pause after
    app.enemyWaves = [("red", 10, 1, 5), ("blue", 10, 1.5, 5), ("red", 20, 0.8, 5), ("green", 7, 2, 10),
    ("yellow", 3, 3, 5), ("black", 100, 5, 10)]

    app.currentWave = 0
    app.enemySpawnDelay = 3
    app.currentEnemySpawn = 0 #current number of squares spawned

def calculatePath(app):
    app.pathway = app.entrance.pathFindToTile(app.exit)

def timerFired(app):
    app.deltaTime = time.time() - app.lastCall

    if app.enemySpawnDelay > 0:
        app.enemySpawnDelay -= app.deltaTime
    if app.enemySpawnDelay <= 0 and app.currentWave < len(app.enemyWaves):
        if app.currentEnemySpawn < app.enemyWaves[app.currentWave][1]:
            enemy.Enemy(app, health=app.enemyTypes[app.enemyWaves[app.currentWave][0]][0],
                speed=app.enemyTypes[app.enemyWaves[app.currentWave][0]][1],
                color=app.enemyWaves[app.currentWave][0])
            app.enemySpawnDelay = app.enemyWaves[app.currentWave][2]
            app.currentEnemySpawn += 1
        else:
            app.enemySpawnDelay = app.enemyWaves[app.currentWave][3]
            app.currentWave += 1
            app.currentEnemySpawn = 0

    # app.enemySpawnDelay -= app.deltaTime
    # if app.enemySpawnDelay < 0:
    #     app.enemySpawnDelay = 1
    #     enemy.Enemy(app)

    for i in app.enemies:
        i.update(app)

    for i in app.towers:
        i.update(app)

    app.lastCall = time.time()

def mouseEvent(app, event): #helper called by both drag and press
    col, row = getTileFromMousePos(app, event.x, event.y)
    if col != -1 and (col, row) != app.entrance.coordinates and\
    (col, row) != app.exit.coordinates:
        if (not app.tiles[col][row].isWall and not app.deleteWalls) or\
        (app.tiles[col][row].isWall and app.deleteWalls):
            app.tiles[col][row].toggleWall()
            calculatePath(app)

def mouseDragged(app, event):
    app.currentMouseCoords = (event.x, event.y)

def mousePressed(app, event):
    app.currentMouseCoords = (event.x, event.y)

    ui.mouseDown(app, event)

def tryPlaceTower(app, x, y, tower):
    if canPlaceTower(app, x, y):
        col, row = getTileFromMousePos(app, x, y)
        app.tiles[col][row].isWall = True

        towers.DartTower(app, col, row)

        #make all enemies recalculate path
        for i in app.enemies:
            i.path = [i.path[0]]
            i.path.extend(i.path[0].pathFindToTile(app.exit))

        calculatePath(app)

def canPlaceTower(app, x, y):
    col, row = getTileFromMousePos(app, x, y)
    if col != -1 and not app.tiles[col][row].isWall:
        allCoords = {(app.entrance.x, app.entrance.y)}
        for i in app.enemies:
            if i.currentPosition[0] == col and i.currentPosition[1] == row or\
            i.path[0].x == col and i.path[0].y == row:
                return False
            if i.currentPosition[0] != -1 and i.path[0] != app.exit:
                #all all possible tiles to set and check all of them
                allCoords.add((i.currentPosition[0], i.currentPosition[1]))
                allCoords.add((i.path[0].x, i.path[0].y))

        #assume this is a wall and see if pathfinding is successful
        app.tiles[col][row].isWall = True

        for i in allCoords:
            #if any tile cannot pathfind, don't allow placement
            if app.tiles[i[0]][i[1]].pathFindToTile(app.exit) == []:
                app.tiles[col][row].isWall = False
                return False

        app.tiles[col][row].isWall = False
        return True
    return False

def mouseReleased(app, event):
    ui.mouseUp(app, event)

    #check tower purchase
    if app.buyingTower:
        tryPlaceTower(app, event.x, event.y, app.buyingTowerId)
        app.buyingTower = False

def keyPressed(app, event):
    if event.key == "x":
        app.deleteWalls = not app.deleteWalls

    if event.key == "r":
        appStarted(app)

#both use height for square grid
def getTileWidth(app):
    return (app.width - app.rightMargin) / (app.tileCols - 1)

def getTileHeight(app):
    return app.height / app.tileRows

def getTileFromMousePos(app, x, y):
    col = int(x / getTileWidth(app))
    row = int(y / getTileHeight(app))

    if col >= app.tileCols or row >= app.tileRows:
        return -1, -1

    return col, row

def redrawAll(app, canvas):
    #background
    canvas.create_rectangle(0, 0, app.width, app.height, fill="black", width=0)
    

    tileWidth, tileHeight = getTileWidth(app), getTileHeight(app)
    tileMargin = 0 #space between tiles

    for col in app.tiles:
        for tile in col:
            x1 = tileWidth * tile.x + tileMargin
            x2 = tileWidth * (tile.x + 1) - tileMargin
            y1 = tileHeight * tile.y + tileMargin
            y2 = tileHeight * (tile.y + 1) - tileMargin

            color = "lightgreen"
            if tile.isWall:
                color = "white"

            # elif tile in app.pathway or tile == app.entrance:
            #     color = "blue"
            
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)
            #canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

    #geometry
    geometry.renderAll(app, canvas)

    #ui: always on top of game elements
    ui.renderAll(app, canvas)

    circleSize = 500
    scale = circleSize / app.image1.size[0]
    scaledCircle = app.scaleImage(app.image1, scale)

    # canvas.create_image(app.width / 2, app.height / 2, image=ImageTk.PhotoImage(scaledCircle))

    #building hover
    if app.buyingTower:
        color = "red"
        if canPlaceTower(app, app.currentMouseCoords[0], app.currentMouseCoords[1]):
            color = "green"
        canvas.create_rectangle(
            app.currentMouseCoords[0] - getTileWidth(app) / 2,
            app.currentMouseCoords[1] - getTileHeight(app) / 2,
            app.currentMouseCoords[0] + getTileWidth(app) / 2,
            app.currentMouseCoords[1] + getTileHeight(app) / 2, 
            fill=color, width=0)

    #fps display
    canvas.create_text(10, 10, anchor="nw", text=f"{int(1 / app.deltaTime)} fps", 
        font="Helvetica 25", fill="black")

def main():
    runApp(width=1024, height=768)

if __name__ == '__main__':
    main()