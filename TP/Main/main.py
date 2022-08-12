from cmu_112_graphics import *
import random, string, math, time, geometry, ui, enemy, towers, levels, threading

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
    def getTileNeighbors(app, tile, prioritizeVertical):
        neighbors = []
        #look at horizontal first
        if not prioritizeVertical:
            if tile.x > 0:
                neighbors.append(app.tiles[tile.x - 1][tile.y])
            if tile.x < app.tileCols - 1:
                neighbors.append(app.tiles[tile.x + 1][tile.y])
            if tile.y > 0:
                neighbors.append(app.tiles[tile.x][tile.y - 1])
            if tile.y < app.tileRows - 1:
                neighbors.append(app.tiles[tile.x][tile.y + 1])
        else:
            if tile.y > 0:
                neighbors.append(app.tiles[tile.x][tile.y - 1])
            if tile.y < app.tileRows - 1:
                neighbors.append(app.tiles[tile.x][tile.y + 1])
            if tile.x > 0:
                neighbors.append(app.tiles[tile.x - 1][tile.y])
            if tile.x < app.tileCols - 1:
                neighbors.append(app.tiles[tile.x + 1][tile.y])
        return neighbors

    #pathfinds to the tile, avoidoing walls
    #my own floodfill pathfind implementation
    #A* pathfinding reference: https://www.youtube.com/watch?v=-L-WgKMFuhE
    def pathFindToTile(self, target, prioritizeVertical=False):
        #if prioritize vertical, look at vertical neighbors first (for top down search so that paths try to go down first)
        Tile.resetPathfindingPointers(self.app)
        currentTiles = [self]
        while True:
            newTiles = []

            #if this is true after searching, it means pathfinding failed
            noNewTiles = True

            for tile in currentTiles:
                for checkTile in Tile.getTileNeighbors(self.app, tile, prioritizeVertical):
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

    app.multiplayer = False

    app.maps = ["grasslands", "volcano", "tunnels"]
    app.map = app.maps[0] #map should be set outside of game scene

    app.difficulties = ["easy", "normal", "hard", "veteran", "impossible"]
    app.difficulty = 0 #0-3

    app.deltaTime = .02 #actual time between current and next
    app.lastCall = time.time()
    app.timerDelay = 1 #run the game as fast as possible (1ms)

    changeScene(app, app.scene)

def changeScene(app, scene, multiplayer=False):
    app.scene = scene

    #clean up scene objects
    geometry.init(app)
    ui.init(app)

    app.multiplayer = multiplayer

    #load in new scenes
    if scene == "menu":
        app.multiplayer = False
        menuInit(app)
    elif scene == "game":
        gameInit(app)
    else:
        raise Exception(f"scene {scene} not found")

#--------------- Multiplayer ------------------
#callback to multiplayer
def startMultiplayer(app, button):
    #need to define them now
    app.enemies = []
    app.towers = []
    app.otherPlayer = None #use otherPlayer class to display opponent
    app.checkingOpponentMap = False #if true, render opponent map and add buttons for sending enemies
    app.multiplayer = True

    threading.Thread(target=multiplayerThread, args=(app,), daemon=True).start()
    
def multiplayerThread(app):
    import websocket_client
    websocket_client.init(app)

def loadMultiplayer(app):
    #called by websocket_client
    changeScene(app, "game", multiplayer=True)

def switchBetweenOpponent(app, button): #swap between self view and opponent view
    app.checkingOpponentMap = not app.checkingOpponentMap

    if app.checkingOpponentMap:
        app.viewOpponentButton.text = "View Self"
    else:
        app.viewOpponentButton.text = "View Opponent"


#--------------- Multiplayer End -----------------

#callback by menu button to load scene
def goToGame(app, button):
    changeScene(app, "game")

def menuInit(app):
    app.background = ui.Rectangle(app, app.width / 2, app.height / 2, app.width, app.height, color="white")
    app.startGameButton = ui.Button(app, app.width / 2, app.height / 2 - 85, 350, 70, text="Start Game",
        color="palegreen1", dimColor="green2", outlineWidth=2, textColor="black", 
        textFont="Helvetica 30", releaseCallback=goToGame)
    app.chooseMapButton = ui.Button(app, app.width / 2, app.height / 2, 350, 70, text=f"Map: {app.map}",
        color="palegreen1", dimColor="green2", outlineWidth=2, textColor="black", 
        textFont="Helvetica 30", releaseCallback=toggleMap)
    app.chooseDifficultyButton = ui.Button(app, app.width / 2, app.height / 2 + 85, 350, 70, text=f"Difficulty: {app.difficulties[app.difficulty]}",
        color="palegreen1", dimColor="green2", outlineWidth=2, textColor="black", 
        textFont="Helvetica 30", releaseCallback=toggleDifficulty)

    app.multiplayerButton = ui.Button(app, app.width / 2, app.height / 2 + 200, 350, 70, text="Multiplayer\n[Experimental]",
        color="palegreen1", dimColor="green2", outlineWidth=2, textColor="black", 
        textFont="Helvetica 25", releaseCallback=startMultiplayer)

def toggleMap(app, button):
    if app.maps.index(app.map) == len(app.maps) - 1:
        app.map = app.maps[0]
    else:
        app.map = app.maps[app.maps.index(app.map) + 1]
    app.chooseMapButton.text = f"Map: {app.map}"

def toggleDifficulty(app, button):
    if app.difficulty == len(app.difficulties) - 1:
        app.difficulty = 0
    else:
        app.difficulty += 1
    app.chooseDifficultyButton.text = f"Difficulty: {app.difficulties[app.difficulty]}"

def playerLoseHealth(app):
    app.health -= 1

    #check lose condition
    if app.health <= 0:
        app.health = 0

        if app.gameOver:
            return

        app.gameOver = True

        #game over ui
        ui.Rectangle(app, app.width / 2, app.height / 2, 370, 250, color="gray")
        ui.Text(app, app.width / 2, app.height / 2 - 50, "Game Over", color="white", font="Helvetica 50 bold")
        ui.Button(app, app.width / 2, app.height / 2 + 50, 300, 51, text="Return to Menu", releaseCallback=returnToMenu,
            color="white", textColor="black", dimColor="lightgreen", textFont="Helvetica 30")

#game over button callback
def returnToMenu(app, button):
    if app.scene != "menu":
        changeScene(app, "menu")

def gameInit(app):
    #initialize levels module
    levels.init(app, level=1)

    #note: last col is nonvisible wall so that the enemy leaves the screen
    app.tileCols, app.tileRows = 16, 16 
    app.rightMargin = 256

    app.money = 750 #starting cash
    app.health = 50 #starting health
    if app.difficulty == 1:
        app.money = 500
        app.health = 30
    elif app.difficulty == 2:
        app.money = 450
        app.health = 15
    elif app.difficulty == 3:
        app.money = 400
        app.health = 5
    elif app.difficulty == 4:
        app.money = 350
        app.health = 1

    app.cheatString = "" #cheat string for free money and health

    app.pathways = [[], []] #enemy paths
    app.deleteWalls = False #keypress trigger
    app.buyingTower = False
    app.buyinTowerId = 0
    app.currentMouseCoords = (0, 0)
    app.enemies = []
    app.towers = []
    app.selectedTower = None
    app.paused = False
    app.showFPS = False
    app.gameOver = False
    app.optionsOn = False

    app.tiles = []
    for i in range(app.tileCols):
        app.tiles.append([])
        for j in range(app.tileRows):
            #new tile
            t = Tile(app, i, j)
            app.tiles[i].append(t)

            if i == app.tileCols - 1 or j == app.tileRows - 1:
                t.isWall = True #last col/row is not seen but all walls

    if app.map == "grasslands":
        #only 1 entrance
        app.entrances = [app.tiles[0][app.tileRows // 2 - 1]]
        app.exits = [app.tiles[app.tileCols - 1][app.tileRows // 2 - 1]]
    elif app.map == "volcano":
        app.entrances = [app.tiles[0][app.tileRows // 2 - 1], app.tiles[app.tileCols // 2 - 1][0]]
        app.exits = [app.tiles[app.tileCols - 1][app.tileRows // 2 - 1], app.tiles[app.tileCols // 2 - 1][app.tileRows - 1]]

        #add lava tiles
        lavaTiles = [
        #corners
        (0, 14), (0, 13), (0, 12), (0, 11), (0, 10),
        (1, 14), (1, 13), (1, 12), #(1, 11),
        (2, 14), (2, 13), #(2, 12),
        (3, 14), #(3, 13),
        (4, 14),

        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
        (1, 0), (1, 1), (1, 2), #(1, 3),
        (2, 0), (2, 1), #(2, 2),
        (3, 0), #(3, 1),
        (4, 0),

        (14, 0), (14, 1), (14, 2), (14, 3), (14, 4),
        (13, 0), (13, 1), (13, 2), #(13, 3),
        (12, 0), (12, 1), #(12, 2),
        (11, 0), #(11, 1),
        (10, 0),

        (14, 14), (14, 13), (14, 12), (14, 11), (14, 10),
        (13, 14), (13, 13), (13, 12), #(13, 11),
        (12, 14), (12, 13), #(12, 12),
        (11, 14), #(11, 13),
        (10, 14),

        #extras
        (6, 7), (7, 6), (7, 8), (8, 7)
        ]
        for t in lavaTiles:
            app.tiles[t[0]][t[1]].isWall = True
    elif app.map == "tunnels":
        app.entrances = [app.tiles[0][4], app.tiles[0][10], app.tiles[4][0], app.tiles[10][0]]
        app.exits = [app.tiles[app.tileCols - 1][4], app.tiles[app.tileCols - 1][10],  app.tiles[4][app.tileRows - 1], app.tiles[10][app.tileRows - 1]]

        #add lava tiles
        tunnelTiles = [
        #corners
        (0, 14), (0, 13), (0, 12), #(0, 11), (0, 10),
        (1, 14), (1, 13), #(1, 12), #(1, 11),
        (2, 14), #(2, 13), #(2, 12),
        #(3, 14), #(3, 13),
        #(4, 14),

        (0, 0), (0, 1), (0, 2), #(0, 3), (0, 4),
        (1, 0), (1, 1), #(1, 2), #(1, 3),
        (2, 0), #(2, 1), #(2, 2),
        #(3, 0), #(3, 1),
        #(4, 0),

        (14, 0), (14, 1), (14, 2), #(14, 3), (14, 4),
        (13, 0), (13, 1), #(13, 2), #(13, 3),
        (12, 0), #(12, 1), #(12, 2),
        #(11, 0), #(11, 1),
        #(10, 0),

        (14, 14), (14, 13), (14, 12), #(14, 11), (14, 10),
        (13, 14), (13, 13), #(13, 12), #(13, 11),
        (12, 14), #(12, 13), #(12, 12),
        #(11, 14), #(11, 13),
        #(10, 14),

        #extras
        (4, 6), (4, 7), (4, 8),
        (6, 4), (7, 4), (8, 4),
        (10, 6), (10, 7), (10, 8),
        (6, 10), (7, 10), (8, 10),
        ]
        for t in tunnelTiles:
            app.tiles[t[0]][t[1]].isWall = True



    calculatePath(app)

    #------------- add game UI --------------

    #tower info background
    ui.Rectangle(app, app.width - app.rightMargin / 2, app.height / 2,
        app.rightMargin, app.height, color="#8a4a22")
    
    #------- Multiplayer -------
    if app.multiplayer:
        app.viewOpponentButton = ui.Button(app, (app.width - app.rightMargin) / 2, 100, 200, 35, color="gray75", dimColor="lightgreen",
         text=f"View Opponent", textFont="Helvetica 20", releaseCallback=switchBetweenOpponent, bid=0)
    #--end--

    #buy tower UI
    app.buyTowerText = ui.Text(app, app.width - app.rightMargin / 2, 100, anchor="n", text="Buy Towers", font="Helvetica 25 bold", color="white")

    app.towerPrices = [[75, 100, 150], [300, 400, 500], [200, 200, 250], [350, 450, 600]]


    app.dartTowerButton = ui.Button(app, app.width - app.rightMargin / 2, 225, 100, 100, color="white", dimColor="lightgreen",
     text=f"Dart\nTower\n\n${app.towerPrices[0][0]}", textFont="Helvetica 18 bold", clickCallback=buyTowerDown, bid=0)

    app.gatlingTowerButton = ui.Button(app, app.width - app.rightMargin / 2, 350, 100, 100, color="white", dimColor="lightgreen",
     text=f"Gatling\nTower\n\n${app.towerPrices[1][0]}", textFont="Helvetica 18 bold", clickCallback=buyTowerDown, bid=1)

    app.freezeTowerButton = ui.Button(app, app.width - app.rightMargin / 2, 475, 100, 100, color="white", dimColor="lightgreen",
     text=f"Freeze\nTower\n\n${app.towerPrices[2][0]}", textFont="Helvetica 18 bold", clickCallback=buyTowerDown, bid=2)

    app.cannonTowerButton = ui.Button(app, app.width - app.rightMargin / 2, 600, 100, 100, color="white", dimColor="lightgreen",
     text=f"Cannon\nTower\n\n${app.towerPrices[3][0]}", textFont="Helvetica 18 bold", clickCallback=buyTowerDown, bid=3)

    app.buyTowerUI = [app.buyTowerText, app.dartTowerButton, app.gatlingTowerButton, app.freezeTowerButton, app.cannonTowerButton]

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

    #entrance/exits
    for e in app.entrances:
        xOffset = 0
        yOffset = 0
        if e.x == 0:
            xOffset = -getTileWidth(app) * 0.7
        elif e.y == 0:
            yOffset = -getTileHeight(app) * 0.7
        geometry.Rectangle(app, (e.x + 0.5) * getTileWidth(app) + xOffset,
            (e.y + 0.5) * getTileHeight(app) + yOffset, getTileWidth(app), getTileHeight(app), color="black", layer=10)
    for e in app.exits:
        xOffset = 0
        yOffset = 0
        if e.x == app.tileCols - 1:
            xOffset = -getTileWidth(app) * 0.3
        elif e.y == app.tileRows - 1:
            yOffset = -getTileHeight(app) * 0.3
        geometry.Rectangle(app, (e.x + 0.5) * getTileWidth(app) + xOffset,
            (e.y + 0.5) * getTileHeight(app) + yOffset, getTileWidth(app), getTileHeight(app), color="black", layer=10)

    #make arrows
    app.pathArrows = []

    index = 0
    for entrance in app.entrances:
        if entrance.x == 0: #arrow righwards
            p1 = (0, (app.entrances[index].y + 0.5) * getTileHeight(app))
            pathArrow = geometry.Polygon(app, 
                p1[0], p1[1] - 10,
                p1[0], p1[1] + 10,
                p1[0] + 70, p1[1] + 10,
                p1[0] + 70, p1[1] + 20,
                p1[0] + 100, p1[1], 
                p1[0] + 70, p1[1] - 20,
                p1[0] + 70, p1[1] - 10,
                color="red", layer=7)
            pathArrow.isActive = False
            app.pathArrows.append(pathArrow)
        elif entrance.y == 0:
            p2 = ((app.entrances[index].x + 0.5) * getTileWidth(app), 0)
            pathArrow = geometry.Polygon(app, 
                p2[0] - 10, p2[1],
                p2[0] + 10, p2[1],
                p2[0] + 10, p2[1] + 70,
                p2[0] + 20, p2[1] + 70,
                p2[0], p2[1] + 100, 
                p2[0] - 20, p2[1] + 70,
                p2[0] - 10, p2[1] + 70,
                color="red", layer=7)
            pathArrow.isActive = False
            app.pathArrows.append(pathArrow)
        index += 1

    #health and money display
    app.moneyIcon = ui.Rectangle(app, app.width - app.rightMargin - 250, 35, 35, 35, color="yellow", outlineWidth=3, outlineColor="black")
    app.healthIcon = ui.Rectangle(app, app.width - app.rightMargin - 100, 35, 35, 35, color="red", outlineWidth=3, outlineColor="black")
    app.moneyText = ui.Text(app, app.width - app.rightMargin - 215, 35, str(app.money), anchor="w", alignment="left", font="Helvetica 27")
    app.healthText = ui.Text(app, app.width - app.rightMargin - 65, 35, str(app.health), anchor="w", alignment="left", font="Helvetica 27")

    #pause & options button
    app.pauseButton = ui.Button(app, app.width - app.rightMargin / 2 - 35, 50, 50, 50, color="", dimColor="",
        outlineColor="white", textFont="Helvetica 18 bold", outlineDimColor="lightgreen", outlineWidth=3, text="=",
        textColor="white", textDimColor="lightgreen", releaseCallback=togglePause, bid=0)
    app.optionsButton = ui.Button(app, app.width - app.rightMargin / 2 + 35, 50, 50, 50, color="", dimColor="",
        outlineColor="white", textFont="Helvetica 18 bold", outlineDimColor="lightgreen", outlineWidth=3, text="#",
        textColor="white", textDimColor="lightgreen", releaseCallback=toggleOptions, bid=0)

    #round level
    app.roundText = ui.Text(app, 15, 15, text=f"Round 1/{len(app.rounds)}",
        font="Helvetica 35 bold", anchor="nw", alignment="left")

    #options UI
    u1 = ui.Rectangle(app, app.width / 2, app.height / 2, 370, 300, color="gray")
    u2 = ui.Text(app, app.width / 2, app.height / 2 - 75, "Options", color="white", font="Helvetica 50 bold")
    u3 = ui.Button(app, app.width / 2, app.height / 2 + 20, 300, 51, text="Continue Game", releaseCallback=toggleOptions,
        color="white", textColor="black", dimColor="lightgreen", textFont="Helvetica 30")
    u4 = ui.Button(app, app.width / 2, app.height / 2 + 90, 300, 51, text="Return to Menu", releaseCallback=returnToMenu,
        color="white", textColor="black", dimColor="lightgreen", textFont="Helvetica 30")
    app.optionsUI = [u1, u2, u3, u4]

    #disables the rects
    toggleOptions(app)
    toggleOptions(app)

def toggleOptions(app, button=None):
    app.optionsOn = not app.optionsOn

    if app.optionsOn:
        for i in app.optionsUI:
            i.isActive = True
    else:
        for i in app.optionsUI:
            i.isActive = False

def toggleSelectedTowerMode(app, button):
    if app.selectedTower != None:
        app.selectedTower.toggleTargetMode(app)
        updateTowerUI(app)

def togglePause(app, button):
    if app.gameOver:
        return
    app.paused = not app.paused
    if app.paused:
        app.pauseButton.text = ">"
    else:
        app.pauseButton.text = "ll"

def buyTowerDown(app, button):
    if app.money >= app.towerPrices[button.bid][0]:
        app.buyingTower = True
        app.buyingTowerId = button.bid

def upgradeSelectedTower(app, button):
    if app.selectedTower != None and app.selectedTower.level < app.selectedTower.maxLevel:
        if app.money >= app.towerPrices[app.selectedTower.tid][app.selectedTower.level]:
            app.money -= app.towerPrices[app.selectedTower.tid][app.selectedTower.level]
            app.selectedTower.upgrade(app)

def sellSelectedTower(app, button):
    #only refunds 70%
    if app.selectedTower != None:
        app.money += int(checkTowerPrice(app, app.selectedTower.tid, app.selectedTower.level) * 0.7)
        app.tiles[app.selectedTower.col][app.selectedTower.row].isWall = False
        app.tiles[app.selectedTower.col][app.selectedTower.row].tower = None
        app.selectedTower.destroy(app)
        app.selectedTower = None
        recalculateAllPaths(app)

def checkTowerPrice(app, towerId, level):
    return sum(app.towerPrices[towerId][:level])

def calculatePath(app):
    app.pathways = []
    for i in range(len(app.entrances)):
        app.pathways.append(app.entrances[i].pathFindToTile(app.exits[i], prioritizeVertical=isVerticalPath(app, i)))

def update(app):
    #disable wave arrows
    for arrow in app.pathArrows:
        arrow.isActive = False

    if app.enemySpawnDelay > 0 and app.currentRound < len(app.rounds):
        app.enemySpawnDelay -= app.deltaTime

        enemiesAlive = False
        if app.currentWave >= len(app.enemyWave): #make sure to only decrease timer if all troops are killed
            for e in app.enemies:
                if not e.destroyed:
                    enemiesAlive = True
                    break
            if enemiesAlive:
                app.enemySpawnDelay += app.deltaTime #add timer back if an enemy is still alive

        if not enemiesAlive and (app.currentEnemySpawn == 0 and app.currentWave == 0 or\
        app.currentWave >= len(app.enemyWave) and app.enemySpawnDelay < 3):
            #enable wave arrows; check if next round has any from said path
            hasPaths = [False] * len(app.entrances)

            for spawn in app.rounds[app.currentRound + 1 if app.currentWave > 0 else 0]:
                if len(spawn) < 5 or spawn[4] == 0 or spawn[4] >= len(app.entrances): #path 0
                    hasPaths[0] = True
                elif len(spawn) >= 5 and spawn[4] > 0: #path 1
                    hasPaths[spawn[4]] = True

            for i in range(len(app.pathArrows)):
                if hasPaths[i] and len(app.entrances) > i:
                    app.pathArrows[i].isActive = True


    if app.enemySpawnDelay <= 0:
        if app.currentWave < len(app.enemyWave):
            if app.currentEnemySpawn < app.enemyWave[app.currentWave][1]:
                path = 0

                #note: defaults back to 0 if path is not in current map
                if len(app.enemyWave[app.currentWave]) == 5 and len(app.entrances) > app.enemyWave[app.currentWave][4]:
                    path = app.enemyWave[app.currentWave][4]

                enemy.Enemy(app, health=app.enemyTypes[app.enemyWave[app.currentWave][0]][0],
                    speed=app.enemyTypes[app.enemyWave[app.currentWave][0]][1],
                    color=app.enemyWave[app.currentWave][0], pathNum=path)
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

                #more money
                app.money += 100 + app.currentRound * 10

                app.currentWave = 0
                app.enemyWave = app.rounds[app.currentRound]


    if app.currentRound == len(app.rounds) - 1 and app.currentWave >= len(app.enemyWave): #last round
        #check that no enemies are alive
        enemiesAlive = False
        for e in app.enemies:
            if not e.destroyed:
                enemiesAlive = True
                break

        if not app.gameOver and not enemiesAlive:
            #win game
            app.gameOver = True

            #win game ui
            ui.Rectangle(app, app.width / 2, app.height / 2, 370, 250, color="gray")
            ui.Text(app, app.width / 2, app.height / 2 - 50, "You Win!", color="white", font="Helvetica 50 bold")
            ui.Button(app, app.width / 2, app.height / 2 + 50, 300, 51, text="Return to Menu", releaseCallback=returnToMenu,
                color="white", textColor="black", dimColor="lightgreen", textFont="Helvetica 30")

def updateEvenPaused(app):
    #ui displays
    app.roundText.text = f"Round {app.currentRound + 1}/{len(app.rounds)}"
    app.healthText.text = str(app.health)
    app.moneyText.text = str(app.money)

    for i in app.enemies:
        i.update(app)

    for i in app.towers:
        i.update(app)

def timerFired(app):
    app.deltaTime = time.time() - app.lastCall

    if app.scene == "game":
        if not app.paused and not app.gameOver:
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
    
    #if multiplayer checking opponent don't click anything
    if app.multiplayer and app.checkingOpponentMap: return 

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
            app.upgradeTowerButton.text = f"Upgrade\nTower\n\n${app.towerPrices[app.selectedTower.tid][app.selectedTower.level]}"

        app.sellTowerButton.text = f"Sell\nTower\n\n+${int(checkTowerPrice(app, app.selectedTower.tid, app.selectedTower.level) * 0.7)}"

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

    if event.key == "r":
        app.currentRound += 1
        app.enemyWave = app.rounds[app.currentRound]
        app.currentWave = 0

    if event.key == "f":
        app.showFPS = not app.showFPS

    app.cheatString += event.key

    moneyCode = "showmethemoney"
    livesCode = "showmethelives"

    while app.cheatString != "" and app.cheatString not in moneyCode and app.cheatString not in livesCode:
        app.cheatString = app.cheatString[1:]
    
    if app.cheatString == moneyCode:
        app.cheatString = ""
        app.money += 100000
    elif app.cheatString == livesCode:
        app.cheatString = ""
        app.health += 100000

def tryPlaceTower(app, x, y, tower):
    if canPlaceTower(app, x, y):
        col, row = getTileFromMousePos(app, x, y)
        app.tiles[col][row].isWall = True

        app.money -= app.towerPrices[tower][0]

        t = None
        if tower == 0:
            t = towers.DartTower(app, col, row)
        elif tower == 1:
            t = towers.GatlingTower(app, col, row)
        elif tower == 2:
            t = towers.FreezeTower(app, col, row)
        elif tower == 3:
            t = towers.CannonTower(app, col, row)
        else:
            print("error: no tower with button id; defaulting to dart tower")
            t = towers.DartTower(app, col, row)
        
        app.tiles[col][row].tower = t

        recalculateAllPaths(app)

def isVerticalPath(app, pathNum):
    if app.map == "grasslands":
        return False
    if app.map == "volcano":
        if pathNum == 0:
            return False
        if pathNum == 1:
            return True
    if app.map == "tunnels":
        if pathNum == 0:
            return False
        if pathNum == 1:
            return False
        if pathNum == 2:
            return True
        if pathNum == 3:
            return True

def recalculateAllPaths(app):
    #make all enemies recalculate path
    for e in app.enemies:
        e.path = [e.path[0]]

        e.path.extend(e.path[0].pathFindToTile(app.exits[e.pathNum],
            prioritizeVertical=isVerticalPath(app, e.pathNum)))

    calculatePath(app)

def canPlaceTower(app, x, y):
    col, row = getTileFromMousePos(app, x, y)

    #can't build on entrance, edge scenario
    if app.tiles[col][row] in app.entrances:
        return False

    if col != -1 and not app.tiles[col][row].isWall:
        allCoords = set()
        for entrance in app.entrances:
            allCoords.add((entrance.x, entrance.y))

        for i in app.enemies:
            if i.currentPosition[0] == col and i.currentPosition[1] == row or\
            i.path[0].x == col and i.path[0].y == row:
                # print("on top of an enemy")
                return False
            if i.currentPosition[0] != -1 and i.currentPosition[1] != -1 and i.path[0] != app.exits[i.pathNum]:
                #all all possible tiles to set and check all of them
                allCoords.add((i.currentPosition[0], i.currentPosition[1]))
                allCoords.add((i.path[0].x, i.path[0].y))

        #assume this is a wall and see if pathfinding is successful
        app.tiles[col][row].isWall = True

        for i in allCoords:
            #if any tile cannot pathfind, don't allow placement
            for e in app.exits:
                if app.tiles[i[0]][i[1]].pathFindToTile(e) == []:
                    # print(f"tile: {i[0]}, {i[1]}")
                    # print("no path")
                    app.tiles[col][row].isWall = False
                    return False
                # else:
                    # print("path succeeded")

        app.tiles[col][row].isWall = False
        return True

    # print("illegal tile")
    return False


def getTileWidth(app):
    #return (app.width - app.rightMargin) / (app.tileCols - 1)
    return (1024 - app.rightMargin) / (app.tileCols - 1)

def getTileHeight(app):
    # return app.height / (app.tileRows - 1)
    return 768 / (app.tileRows - 1)

def getTileFromMousePos(app, x, y):
    col = int(x / getTileWidth(app))
    row = int(y / getTileHeight(app))

    if col >= app.tileCols or row >= app.tileRows:
        return -1, -1

    return col, row

#-------- Multiplayer ---------
def redrawOpponentGame(app, canvas, otherPlayer):
    if otherPlayer != None and otherPlayer.towers != None:
        tileWidth, tileHeight = getTileWidth(app), getTileHeight(app)
        tileMargin = 0 #space between tiles

        towerCoords = set()
        for t in otherPlayer.towers:
            towerCoords.add((t[0], t[1]))

        for col in app.tiles:
            for tile in col:
                x1 = tileWidth * tile.x + tileMargin
                x2 = tileWidth * (tile.x + 1) - tileMargin
                y1 = tileHeight * tile.y + tileMargin
                y2 = tileHeight * (tile.y + 1) - tileMargin

                color = "palegreen"
                if app.map == "volcano":
                    color = "gray38"
                elif app.map == "tunnels":
                    color = "gray30"

                if tile.isWall and tile.tower == None or (tile.x, tile.y) in towerCoords:
                    color = "white"
                    if app.map == "volcano" and tile.tower == None:
                        color = "orangered"
                    elif app.map == "tunnels" and tile.tower == None:
                        color = "gray25"
                
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)
        for t in otherPlayer.towers:
            #render t
            tempTower = towers.DartTower(app, t[0], t[1])
            tempTower.turretBase.rotation = t[2]
            tempTower.manualRender(app, canvas)
            tempTower.destroy(app)

        #render enemies
        for e in otherPlayer.enemies:
            tempEnemy = enemy.Enemy(app, color=e[2], health=app.enemyTypes[e[2]][0])
            tempEnemy.x = e[0]
            tempEnemy.y = e[1]
            tempEnemy.health = e[3]
            tempEnemy.manualRender(app, canvas)
            tempEnemy.destroy(app)


    ui.renderAll(app, canvas)


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
            if app.map == "volcano":
                color = "gray38"
            elif app.map == "tunnels":
                color = "gray30"

            if tile.isWall:
                color = "white"
                if app.map == "volcano" and tile.tower == None:
                    color = "orangered"
                elif app.map == "tunnels" and tile.tower == None:
                    color = "gray25"
            
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

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
        if app.multiplayer and app.checkingOpponentMap:
            redrawOpponentGame(app, canvas, app.otherPlayer)
        else:
            redrawGame(app, canvas)

def main():
    runApp(width=1024, height=768)

if __name__ == '__main__':
    main()