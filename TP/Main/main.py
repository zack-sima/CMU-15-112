from cmu_112_graphics import *
import random, string, math, time, geometry, ui, enemy, towers, levels

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
        self.tower = None

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
    #A* pathfinding reference: https://www.youtube.com/watch?v=-L-WgKMFuhE
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
    app.scene = "menu" #only load game stuff when this is game scene

    app.deltaTime = .02 #actual time between current and next
    app.lastCall = time.time()
    app.timerDelay = 1 #run the game as fast as possible (1ms)

    changeScene(app, app.scene)

def changeScene(app, scene):
    app.scene = scene

    #clean up scene objects
    geometry.init(app)
    ui.init(app)

    #load in new scenes
    if scene == "menu":
        menuInit(app)
    elif scene == "game":
        gameInit(app)
    else:
        raise Exception(f"scene {scene} not found")

#callback by menu button to load scene
def goToGame(app, button):
    changeScene(app, "game")

def menuInit(app):
    app.background = ui.Rectangle(app, app.width / 2, app.height / 2, app.width, app.height, color="white")
    app.startGameButton = ui.Button(app, app.width / 2, app.height / 2, 350, 70, text="Start Game",
        color="palegreen1", dimColor="green2", outlineWidth=2, textColor="black", 
        textFont="Helvetica 30", releaseCallback=goToGame)

def gameInit(app):
    #initialize levels module
    levels.init(app, level=1)

    #note: last col is nonvisible wall so that the enemy leaves the screen
    app.tileCols, app.tileRows = 16, 15 
    app.rightMargin = 256
    app.money = 500 #starting cash

    app.pathway = [] #temporary enemy pathway
    app.deleteWalls = False #keypress trigger
    app.buyingTower = False
    app.buyinTowerId = 0
    app.currentMouseCoords = (0, 0)
    app.enemies = []
    app.towers = []
    app.selectedTower = None
    app.paused = False
    app.showFPS = False

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

    #tower info background
    ui.Rectangle(app, app.width - app.rightMargin / 2, app.height / 2,
        app.rightMargin, app.height, color="#8a4a22")
    
    #buy tower UI
    app.buyTowerText = ui.Text(app, app.width - app.rightMargin / 2, 100, anchor="n", text="Buy Towers", font="Helvetica 25 bold", color="white")

    app.towerPrices = [[100, 125, 150], [350, 300, 500], [200, 100, 150]]


    app.dartTowerButton = ui.Button(app, app.width - app.rightMargin / 2, 225, 100, 100, color="white", dimColor="lightgreen",
     text=f"Dart\nTower\n\n${app.towerPrices[0][0]}", textFont="Helvetica 18 bold", clickCallback=buyTowerDown, bid=0)

    app.gatlingTowerButton = ui.Button(app, app.width - app.rightMargin / 2, 350, 100, 100, color="white", dimColor="lightgreen",
     text=f"Gatling\nTower\n\n${app.towerPrices[1][0]}", textFont="Helvetica 18 bold", clickCallback=buyTowerDown, bid=1)

    app.freezeTowerButton = ui.Button(app, app.width - app.rightMargin / 2, 475, 100, 100, color="white", dimColor="lightgreen",
     text=f"Freeze\nTower\n\n${app.towerPrices[2][0]}", textFont="Helvetica 18 bold", clickCallback=buyTowerDown, bid=2)

    app.buyTowerUI = [app.buyTowerText, app.dartTowerButton, app.gatlingTowerButton, app.freezeTowerButton]

    #upgrade/sell tower buttons
    app.manageTowerText = ui.Text(app, app.width - app.rightMargin / 2, 100, anchor="n",
        text="[selected tower name]", font="Helvetica 25 bold", color="white")

    app.toggleTargetModeButton = ui.Button(app, app.width - app.rightMargin / 2, 200, 180, 35, color="white", dimColor="lightgreen",
     text="Upgrade\nTower", textFont="Helvetica 18 bold", releaseCallback=toggleSelectedTowerMode, bid=0)

    app.upgradeTowerButton = ui.Button(app, app.width - app.rightMargin / 2, 325, 120, 120, color="white", dimColor="lightgreen",
     text="Target: First", textFont="Helvetica 18 bold", releaseCallback=upgradeSelectedTower, bid=0)

    app.sellTowerButton = ui.Button(app, app.width - app.rightMargin / 2, 500, 120, 120, color="white", dimColor="lightgreen",
     text="Sell\nTower", textFont="Helvetica 18 bold", releaseCallback=sellSelectedTower, bid=0)

    app.manageTowerUI = [app.manageTowerText, app.toggleTargetModeButton, app.upgradeTowerButton, app.sellTowerButton]

    #health and money display
    app.healthText = ui.Rectangle(app, app.width - app.rightMargin - 200, 35, 35, 35, color="yellow", outlineWidth=3, outlineColor="black")

    #pause button
    app.pauseButton = ui.Button(app, app.width - app.rightMargin / 2, 50, 50, 50, color="", dimColor="",
        outlineColor="white", textFont="Helvetica 18 bold", outlineDimColor="lightgreen", outlineWidth=3, text="=",
        textColor="white", textDimColor="lightgreen", releaseCallback=togglePause, bid=0)

    #round level
    app.roundText = ui.Text(app, 15, 15, text=f"Round 1/{len(app.rounds)}",
        font="Helvetica 35 bold", anchor="nw", alignment="left")

def toggleSelectedTowerMode(app, button):
    if app.selectedTower != None:
        app.selectedTower.toggleTargetMode(app)
        updateTowerUI(app)

def togglePause(app, button):
    app.paused = not app.paused
    if app.paused:
        app.pauseButton.text = ">"
    else:
        app.pauseButton.text = "ll"

def buyTowerDown(app, button):
    app.buyingTower = True
    app.buyingTowerId = button.bid

def upgradeSelectedTower(app, button):
    if app.selectedTower != None:
        app.selectedTower.upgrade(app)

def sellSelectedTower(app, button):
    if app.selectedTower != None:
        app.tiles[app.selectedTower.col][app.selectedTower.row].isWall = False
        app.tiles[app.selectedTower.col][app.selectedTower.row].tower = None
        app.selectedTower.destroy(app)
        app.selectedTower = None
        recalculateAllPaths(app)

def calculatePath(app):
    app.pathway = app.entrance.pathFindToTile(app.exit)

def update(app):
    app.roundText.text = f"Round {app.currentRound + 1}/{len(app.rounds)}"
    if app.enemySpawnDelay > 0:
        app.enemySpawnDelay -= app.deltaTime

    if app.enemySpawnDelay <= 0:
        if app.currentWave < len(app.enemyWave):
            if app.currentEnemySpawn < app.enemyWave[app.currentWave][1]:
                enemy.Enemy(app, health=app.enemyTypes[app.enemyWave[app.currentWave][0]][0],
                    speed=app.enemyTypes[app.enemyWave[app.currentWave][0]][1],
                    color=app.enemyWave[app.currentWave][0])
                app.enemySpawnDelay = app.enemyWave[app.currentWave][2]
                app.currentEnemySpawn += 1

                #end of wave
                if app.currentEnemySpawn == app.enemyWave[app.currentWave][1]:
                    app.enemySpawnDelay = app.enemyWave[app.currentWave][3]
                    app.currentWave += 1
                    app.currentEnemySpawn = 0

        elif app.currentWave >= len(app.enemyWave) and app.currentRound < len(app.rounds):
            #new round
            if app.currentRound < len(app.rounds) - 1:
                app.currentRound += 1
                app.currentWave = 0
                app.enemyWave = app.rounds[app.currentRound]

def updateEvenPaused(app):
    for i in app.enemies:
        i.update(app)

    for i in app.towers:
        i.update(app)

def timerFired(app):
    app.deltaTime = time.time() - app.lastCall

    if app.scene == "game":
        if not app.paused:
            update(app)

        updateEvenPaused(app)

    app.lastCall = time.time()

def mouseDragged(app, event):
    if app.scene != "game":
        return
    
    app.currentMouseCoords = (event.x, event.y)

def mousePressed(app, event):
    ui.mouseDown(app, event)

    if app.scene != "game":
        return

    app.currentMouseCoords = (event.x, event.y)
    
    col, row = getTileFromMousePos(app, event.x, event.y)
    if col != -1 and col != app.tileCols - 1:
        #only deselects if a tile is clicked and not last tile (hidden finish tile)
        app.selectedTower = None

    if col != -1 and app.tiles[col][row].tower != None:
        app.selectedTower = app.tiles[col][row].tower
        updateTowerUI(app)

def updateTowerUI(app):
    if app.selectedTower != None:
        app.manageTowerText.text = app.selectedTower.name + "\n(level " + str(app.selectedTower.level) + ")"
        if app.selectedTower.level == app.selectedTower.maxLevel:
            app.upgradeTowerButton.text = "Max Level"
        else:
            app.upgradeTowerButton.text = "Upgrade\nTower"

        if app.selectedTower.targetMode == 0:
            app.toggleTargetModeButton.text = "Target: first"
        elif app.selectedTower.targetMode == 1:
            app.toggleTargetModeButton.text = "Target: last"
        elif app.selectedTower.targetMode == 2:
            app.toggleTargetModeButton.text = "Target: strong"

def mouseReleased(app, event):
    ui.mouseUp(app, event)

    if app.scene != "game":
        return

    #check tower purchase
    if app.buyingTower:
        tryPlaceTower(app, event.x, event.y, app.buyingTowerId)
        app.buyingTower = False

def keyPressed(app, event):
    if app.scene != "game":
        return

    if event.key == "f":
        app.showFPS = not app.showFPS



def tryPlaceTower(app, x, y, tower):
    if canPlaceTower(app, x, y):
        col, row = getTileFromMousePos(app, x, y)
        app.tiles[col][row].isWall = True

        t = None
        if tower == 0:
            t = towers.DartTower(app, col, row)
        elif tower == 1:
            t = towers.GatlingTower(app, col, row)
        elif tower == 2:
            t = towers.FreezeTower(app, col, row)
        else:
            print("error: no tower with button id; defaulting to dart tower")
            t = towers.DartTower(app, col, row)
        
        app.tiles[col][row].tower = t

        recalculateAllPaths(app)

def recalculateAllPaths(app):
    #make all enemies recalculate path
    for i in app.enemies:
        i.path = [i.path[0]]
        i.path.extend(i.path[0].pathFindToTile(app.exit))

    calculatePath(app)

def canPlaceTower(app, x, y):
    col, row = getTileFromMousePos(app, x, y)

    #can't build on entrance, edge scenario
    if app.tiles[col][row] == app.entrance:
        return False

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


#both use height for square grid
def getTileWidth(app):
    #return (app.width - app.rightMargin) / (app.tileCols - 1)
    return (1024 - app.rightMargin) / (app.tileCols - 1)

def getTileHeight(app):
    # return app.height / app.tileRows
    return 768 / app.tileRows


def getTileFromMousePos(app, x, y):
    col = int(x / getTileWidth(app))
    row = int(y / getTileHeight(app))

    if col >= app.tileCols or row >= app.tileRows:
        return -1, -1

    return col, row

def redrawGame(app, canvas):
    #background
    canvas.create_rectangle(0, 0, app.width, app.height, fill="black", width=0)

    tileWidth, tileHeight = getTileWidth(app), getTileHeight(app)
    tileMargin = 0 #space between tiles

    if app.buyingTower:
        tileMargin = 1 #show grid

    for col in app.tiles:
        for tile in col:
            x1 = tileWidth * tile.x + tileMargin
            x2 = tileWidth * (tile.x + 1) - tileMargin
            y1 = tileHeight * tile.y + tileMargin
            y2 = tileHeight * (tile.y + 1) - tileMargin

            color = "palegreen"
            if tile.isWall:
                color = "white"

            # elif tile in app.pathway or tile == app.entrance:
            #     color = "blue"
            
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)
            #canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

    #geometry
    geometry.renderAll(app, canvas)

    #selected tower range display and display different UI
    if app.selectedTower != None:
        for i in app.manageTowerUI:
            i.isActive = True
        for i in app.buyTowerUI:
            i.isActive = False

        canvas.create_oval(app.selectedTower.x - app.selectedTower.detectionRange,
            app.selectedTower.y - app.selectedTower.detectionRange,
            app.selectedTower.x + app.selectedTower.detectionRange,
            app.selectedTower.y + app.selectedTower.detectionRange, fill="", width=2, outline="black")
    else:
        for i in app.manageTowerUI:
            i.isActive = False
        for i in app.buyTowerUI:
            i.isActive = True

    #ui: always on top of game elements
    ui.renderAll(app, canvas)

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
    if app.showFPS:
        canvas.create_text(10, 10, anchor="nw", text=f"{int(1 / app.deltaTime)} fps", 
            font="Helvetica 25", fill="black")

def redrawMenu(app, canvas):
    geometry.renderAll(app, canvas)
    ui.renderAll(app, canvas)

def redrawAll(app, canvas):
    if app.scene == "menu":
        redrawMenu(app, canvas)
    elif app.scene == "game":
        redrawGame(app, canvas)

def main():
    runApp(width=1024, height=768)

if __name__ == '__main__':
    main()