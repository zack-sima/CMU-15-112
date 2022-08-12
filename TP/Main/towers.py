import geometry, main, math

class Explosion:
	def __init__(self, app, x, y, radius, damage=1, freezeTimer=0, color="black"):
		self.x = x
		self.y = y
		self.destroyed = False
		self.currentRadius = 1
		self.radius = radius
		self.damage = damage
		self.freezeTimer = freezeTimer
		self.circle = geometry.Circle(app, x, y, 1, color="", outlineWidth=3, outlineColor=color, layer=7)

		#check collision
		for e in app.enemies:
			if geometry.distance(self.x, self.y, e.x, e.y) < e.square.width / 2 + self.radius + 10:
				target = e
				target.freezeTimer = max(target.freezeTimer, self.freezeTimer)
				target.loseHealth(app, self.damage)

	def update(self, app):
		if self.destroyed:
			return

		self.currentRadius += app.deltaTime * 7500 / (self.currentRadius + 20)

		self.circle.radius = self.currentRadius

		if self.currentRadius > self.radius:
			self.destroy(app)

	def destroy(self, app):
		self.destroyed = True
		self.circle.destroy(app)

class Dart:
	def __init__(self, app, target, sender, damage=1, freezeTimer=0):
		self.freezeTimer = freezeTimer
		self.destroyTimer = 10

		self.sender = sender
		self.target = target
		self.destroyed = False
		self.damage = damage

		self.projectile = geometry.Rectangle(app, sender.x, sender.y, 20, 5, color=sender.projectileColor, rotation=sender.turretBase.rotation)
		self.projectile.translate(35, 0) #move out of sender turret
	
	def update(self, app):
		if self.destroyed:
			return

		#destroy projectile if too much time has passed
		self.destroyTimer -= app.deltaTime
		if self.destroyTimer <= 0:
			self.destroy(app)
			return

		if self.target != None and not self.target.destroyed:
			#look at target
			self.projectile.lookAt(self.target.x, self.target.y)

		#check collision
		for e in app.enemies:
			if geometry.distance(self.projectile.x, self.projectile.y, e.x, e.y) < e.square.width / 2 + 10:
				target = e
				target.freezeTimer = max(target.freezeTimer, self.freezeTimer)
				target.loseHealth(app, self.damage)
				self.destroy(app)
				break

		self.projectile.translate(app.deltaTime * 350, 0) #100px/second forward

	def destroy(self, app):
		self.projectile.destroy(app)
		self.sender = None
		self.destroyed = True

class ExplosiveDart(Dart):
	def __init__(self, app, target, sender, damage=1, freezeTimer=0, radius=75):
		super().__init__(app, target, sender, damage=damage, freezeTimer=freezeTimer)
		self.radius = radius
		self.explosion = None
		self.exploding = False

	def update(self, app):
		if self.destroyed:
			return

		if self.exploding:
			self.explosion.update(app)
			if self.explosion.destroyed:
				self.destroy(app)
			return

		#destroy projectile if too much time has passed
		self.destroyTimer -= app.deltaTime
		if self.destroyTimer <= 0:
			self.destroy(app)
			return

		if self.target != None and not self.target.destroyed:
			#look at target
			self.projectile.lookAt(self.target.x, self.target.y)

		#check collision
		for e in app.enemies:
			if geometry.distance(self.projectile.x, self.projectile.y, e.x, e.y) < e.square.width / 2 + 10:
				self.projectile.color = ""
				self.explosion = Explosion(app, self.projectile.x, self.projectile.y, self.radius,
					damage=self.damage, freezeTimer=self.freezeTimer, color=self.sender.projectileColor)
				self.exploding = True
				break

		self.projectile.translate(app.deltaTime * 350, 0) #100px/second forward

class Tower:
	def __init__(self, app, col, row, detectionRange, level=1, maxLevel=3):
		self.tid = -1 #tower id used to identify towers, should be set by children
		self.detectionRange = detectionRange
		self.level = level
		self.maxLevel = maxLevel
		self.col = col
		self.row = row
		self.x = (col + 0.5) * main.getTileWidth(app)
		self.y = (row + 0.5) * main.getTileHeight(app)
		self.targetMode = 0 #0 = first, 1 = last, 2 = strong
		self.currentTarget = None
		app.towers.append(self)

	def findEnemy(self, app):
		# if self.currentTarget == None or self.currentTarget.destroyed or\
		# geometry.distance(self.x, self.y, self.currentTarget.x, self.currentTarget.y) > self.detectionRange:
		#find new enemy
		self.currentTarget = None

		if self.targetMode == 0:
			#enemy closest to the end (can't just take first element of list since speeds are different)
			closestPathToEnd = 1000000
			closestInterpolation = 0
			for e in app.enemies:
				if geometry.distance(e.x, e.y, self.x, self.y) <= self.detectionRange and\
				(len(e.path) < closestPathToEnd or len(e.path) == closestPathToEnd and e.currentInterpolation > closestInterpolation):
					closestPathToEnd = len(e.path)
					closestInterpolation = e.currentInterpolation
					self.currentTarget = e
		elif self.targetMode == 1:
			#enemy furthest from the end
			farthestPathToEnd = -1
			farthestInterpolation = 0
			for e in app.enemies:
				if geometry.distance(e.x, e.y, self.x, self.y) <= self.detectionRange and\
				(len(e.path) > farthestPathToEnd or len(e.path) == farthestPathToEnd and e.currentInterpolation < farthestInterpolation):
					farthestPathToEnd = len(e.path)
					farthestInterpolation = e.currentInterpolation
					self.currentTarget = e

		elif self.targetMode == 2:
			largestHealth = 0
			for e in app.enemies:
				if geometry.distance(e.x, e.y, self.x, self.y) <= self.detectionRange and e.health > largestHealth:
					self.currentTarget = e
					largestHealth = e.health

	def toggleTargetMode(self, app):
		self.targetMode += 1
		if self.targetMode == 3:
			self.targetMode = 0

	def update(self, app): pass
	def destroy(self, app): pass
	def upgrade(self, app): pass

	#for multiplayer: render once on call
	def manualRender(self, app, canvas): pass

class DartTower(Tower):
	def __init__(self, app, col, row, projectileColor="brown"):
		super().__init__(app, col, row, 200, level=1, maxLevel=3)

		self.tid = 0

		#stores all projectiles so their update can be called
		self.projectiles = []
		self.projectileColor = projectileColor

		self.name = "Dart Tower"

		self.shootDelay = 0 #changing counter
		self.recoil = 0 #recoil moves gun back for animation effect

		self.destroyed = False

		width, height = main.getTileWidth(app), main.getTileHeight(app)
		self.turretBase = geometry.Rectangle(app, x=self.x, y=self.y, width=width * 0.7,
			height=height * 0.7, color="orange", layer=4)
		self.turretGun = geometry.Rectangle(app, x=width * 0.33,
			y=0, width=width * 0.75, height=height * 0.1, parent=self.turretBase, color="black", layer=3)
		self.upgradeOutline = geometry.Rectangle(app, 0, 0, width * 0.7, height * 0.7, parent=self.turretBase, layer=4,
			color="", outlineWidth=3, outlineColor="")

		self.setLevelProperties(app)

	def manualRender(self, app, canvas):
		#first recalculate positions
		self.turretGun.recalculatePositions()
		self.turretBase.recalculatePositions()
		self.upgradeOutline.recalculatePositions()

		self.turretGun.render(app, canvas)
		self.turretBase.render(app, canvas)
		self.upgradeOutline.render(app, canvas)

	def update(self, app):
		if self.destroyed:
			return

		self.setLevelProperties(app)

		if app.paused:
			return

		#check current enemy/find new enemy
		self.findEnemy(app)

		#gun recoil animation
		if self.recoil > 0:
			self.recoil -= app.deltaTime * 5
		if self.recoil < 0:
			self.recoil = 0
		self.turretGun.x = main.getTileWidth(app) * 0.33 - self.recoil * 7

		#rotate to look at enemy
		if self.currentTarget != None:
			self.turretBase.lookAt(self.currentTarget.x, self.currentTarget.y)
		
		#shoot if delay becomes 0
		if self.shootDelay <= 0:
			if self.currentTarget != None:
				self.shootDelay += self.shootInterval
				
				self.recoil = 1
				self.spawnProjectile(app)
		else:
			self.shootDelay -= app.deltaTime

		#update projectiles
		for i in self.projectiles:
			i.update(app)

	def spawnProjectile(self, app):
		self.projectiles.append(Dart(app, self.currentTarget, self, damage=self.damage))

	def setLevelProperties(self, app):
		#check level properties
		if self.level == 1:
			self.detectionRange = 150
			self.upgradeOutline.outlineColor = ""
			self.shootInterval = 1
			self.damage = 2
		elif self.level == 2:
			self.detectionRange = 175
			self.upgradeOutline.outlineColor = "gray"
			self.shootInterval = 0.7
			self.damage = 3
		elif self.level == 3:
			self.detectionRange = 200
			self.upgradeOutline.outlineColor = "black"
			self.shootInterval = 0.55
			self.damage = 5


	def upgrade(self, app):
		if self.level < self.maxLevel:
			self.level += 1

		main.updateTowerUI(app)
			
	def destroy(self, app):
		#destroy all projectiles, own building structures, etc
		self.destroyed = True
		if self in app.towers:
			app.towers.remove(self)

		for i in self.projectiles:
			i.destroy(app)

		del self.projectiles

		self.upgradeOutline.destroy(app)
		self.turretGun.destroy(app)
		self.turretBase.destroy(app)

		del self.upgradeOutline
		del self.turretGun
		del self.turretBase

class GatlingTower(DartTower):
	def __init__(self, app, col, row):
		super().__init__(app, col, row, projectileColor="green")

		self.tid = 1

		self.name = "Gatling Tower"

		self.turretBase.color = "lightgreen"

		self.setLevelProperties(app)

	def setLevelProperties(self, app):
		#check level properties
		if self.level == 1:
			self.detectionRange = 200
			self.upgradeOutline.outlineColor = ""
			self.shootInterval = 0.15
			self.damage = 1
		elif self.level == 2:
			self.detectionRange = 225
			self.upgradeOutline.outlineColor = "gray"
			self.shootInterval = 0.12
			self.damage = 2
		elif self.level == 3:
			self.detectionRange = 250
			self.upgradeOutline.outlineColor = "black"
			self.shootInterval = 0.08
			self.damage = 3

class FreezeTower(DartTower):
	def __init__(self, app, col, row):
		super().__init__(app, col, row, projectileColor="blue")

		self.tid = 2

		self.name = "Freeze Tower"

		self.turretBase.color = "lightblue"

		self.setLevelProperties(app)

	def setLevelProperties(self, app):
		#check level properties
		if self.level == 1:
			self.radius = 50
			self.detectionRange = 150
			self.upgradeOutline.outlineColor = ""
			self.shootInterval = 1.5
			self.freezeTimer = 1
			self.damage = 0
		elif self.level == 2:
			self.radius = 65
			self.detectionRange = 165
			self.upgradeOutline.outlineColor = "gray"
			self.shootInterval = 1
			self.freezeTimer = 1.5
			self.damage = 0
		elif self.level == 3:
			self.radius = 75
			self.detectionRange = 180
			self.upgradeOutline.outlineColor = "black"
			self.shootInterval = 0.75
			self.freezeTimer = 2
			self.damage = 0

	def spawnProjectile(self, app):
		self.projectiles.append(ExplosiveDart(app, self.currentTarget, self,
			damage=self.damage, freezeTimer=self.freezeTimer, radius=self.radius))

class CannonTower(DartTower):
	def __init__(self, app, col, row, projectileColor="red"):
		super().__init__(app, col, row, projectileColor=projectileColor)
		self.tid = 3

		self.name = "Cannon Tower"

		self.turretBase.color = "red"

		self.setLevelProperties(app)

	def setLevelProperties(self, app):
		#check level properties
		if self.level == 1:
			self.radius = 55
			self.detectionRange = 225
			self.upgradeOutline.outlineColor = ""
			self.shootInterval = 1.5
			self.damage = 2
		elif self.level == 2:
			self.radius = 70
			self.detectionRange = 250
			self.upgradeOutline.outlineColor = "gray"
			self.shootInterval = 1.2
			self.damage = 3
		elif self.level == 3:
			self.radius = 85
			self.detectionRange = 275
			self.upgradeOutline.outlineColor = "black"
			self.shootInterval = 1
			self.damage = 5

	def spawnProjectile(self, app):
		self.projectiles.append(ExplosiveDart(app, self.currentTarget, self, damage=self.damage, radius=self.radius))
