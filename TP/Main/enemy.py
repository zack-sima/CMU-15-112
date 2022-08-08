import math, geometry, copy, main, levels

class Enemy:
    def __init__(self, app, health=5, color="red", speed=1):
        #interpolates between current tile and next tile
        self.currentInterpolation = 0
        self.currentPosition = (-1, app.entrance.y) #-1 so it moves into the entrance

        self.speed = speed #game tiles per second moved

        self.path = copy.copy(app.pathway)
        self.path.insert(0, app.entrance)

        self.maxHealth = health
        self.health = health
        self.freezeTimer = 0
        self.color = color

        self.square = geometry.Rectangle(app, -100, 0, main.getTileWidth(app) * 0.8, main.getTileHeight(app) * 0.8, color=color, layer=2)
        self.freezeSquare = geometry.Rectangle(app, 0, 0, main.getTileWidth(app) * 0.5, main.getTileWidth(app) * 0.5, parent=self.square, color="lightblue", layer=2)
        self.freezeSquare.isActive = False #not frozen at the beginning

        self.healthBarRight = geometry.Rectangle(app, x=0, y=self.square.height / 2 + 10, width=self.square.width, height=7, parent=self.square, color="black", layer=5)
        self.healthBarLeft = geometry.Rectangle(app, x=0, y=self.square.height / 2 + 10, width=self.square.width, height=7, parent=self.square, color="#00FF00", layer=5)
        
        self.x = (self.currentPosition[0] + 0.5) * main.getTileWidth(app)
        self.y = (self.currentPosition[1] + 0.5) * main.getTileHeight(app)

        #when this is marked true, all towers referenced to this auto de-refs
        self.destroyed = False

        app.enemies.append(self)

    def loseHealth(self, app, damage):
        self.health -= damage
        if self.health <= 0:
            #give player money
            app.money += app.enemyTypes[self.color][2]
            self.destroy(app)

    def destroy(self, app):
        app.enemies.remove(self)

        self.freezeSquare.destroy(app)
        self.square.destroy(app)
        self.healthBarLeft.destroy(app)
        self.healthBarRight.destroy(app)

        #references to this object by towers may still exist
        self.destroyed = True

    def update(self, app):
        if self.destroyed or app.paused:
            return

        #frozen: third of normal speed
        if self.freezeTimer > 0:
            self.currentInterpolation += app.deltaTime * self.speed * 0.5

            self.freezeTimer -= app.deltaTime
            self.freezeSquare.isActive = True
        else:
            self.currentInterpolation += app.deltaTime * self.speed

            self.freezeSquare.isActive = False

        self.healthBarLeft.width = self.square.width * self.health / self.maxHealth
        self.healthBarRight.width = self.square.width - self.healthBarLeft.width

        self.healthBarLeft.x = (self.health / self.maxHealth - 1) * self.square.width / 2
        self.healthBarRight.x = self.health / self.maxHealth * self.square.width / 2

        

        self.square.x = (self.currentPosition[0] + 0.5) * main.getTileWidth(app)
        self.square.y = (self.currentPosition[1] + 0.5) * main.getTileHeight(app)

        if len(self.path) > 0:
            if self.currentInterpolation < 1:
                self.square.x += ((self.path[0].x + 0.5) * main.getTileWidth(app) - self.square.x) * self.currentInterpolation
                self.square.y += ((self.path[0].y + 0.5) * main.getTileHeight(app) - self.square.y) * self.currentInterpolation
            else:
                self.currentInterpolation = 0
                self.square.x = (self.path[0].x + 0.5) * main.getTileWidth(app)
                self.square.y = (self.path[0].y + 0.5) * main.getTileHeight(app)
                self.currentPosition = (self.path[0].x, self.path[0].y)
                self.path.pop(0)
                if len(self.path) == 0:
                    #player loses health; check player
                    main.playerLoseHealth(app)
                    self.destroy(app)

            #define coordinates so it's easier for towers to track
            self.x = self.square.x
            self.y = self.square.y
        else:
            print("path empty")
            self.destroy(app)

        self.square.updateGlobalPosition()