import geometry, main

class Tower:
	def __init__(self, app, col, row, detectionRange):
		self.detectionRange = detectionRange
		self.col = col
		self.row = row
		self.x = (col + 0.5) * main.getTileWidth(app)
		self.y = (row + 0.5) * main.getTileHeight(app)
		self.currentTarget = None
		app.towers.append(self)

	def findEnemy(self, app):
		if self.currentTarget == None or self.currentTarget.destroyed or\
		geometry.distance(self.x, self.y, self.currentTarget.x, self.currentTarget.y) > self.detectionRange:
			#find new enemy
			self.currentTarget = None

			for e in app.enemies:
				if geometry.distance(e.x, e.y, self.x, self.y) <= self.detectionRange:
					self.currentTarget = e
					break

	def update(self, app): pass
	def destroy(self, app): pass

class Dart:
	def __init__(self, app, target, sender):
		self.destroyTimer = 10

		self.sender = sender
		self.target = target
		self.destroyed = False

		self.projectile = geometry.Rectangle(app, sender.x, sender.y, 20, 5, color="brown", rotation=sender.turretBase.rotation)
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
				e.loseHealth(app, 1)
				#print("hit enemy")
				self.destroy(app)
				break

		self.projectile.translate(app.deltaTime * 350, 0) #100px/second forward

	def destroy(self, app):
		self.projectile.destroy(app)
		self.sender = None
		self.destroyed = True

class DartTower(Tower):
	def __init__(self, app, col, row):
		super().__init__(app, col, row, 200)

		#stores all projectiles so their update can be called
		self.projectiles = []

		self.shootInterval = 0.15 #const speed

		self.shootDelay = 0 #changing counter

		self.recoil = 0 #recoil moves gun back for animation effect

		width, height = main.getTileWidth(app), main.getTileHeight(app)
		self.turretBase = geometry.Rectangle(app, x=self.x, y=self.y, width=width * 0.7,
			height=height * 0.7, color="orange", layer=4)
		self.turretGun = geometry.Rectangle(app, x=width * 0.33,
			y=0, width=width * 0.75, height=height * 0.1, parent=self.turretBase, color="black", layer=3)

	def update(self, app):
		self.findEnemy(app)

		if self.recoil > 0:
			self.recoil -= app.deltaTime * 5
		if self.recoil < 0:
			self.recoil = 0

		self.turretGun.x = main.getTileWidth(app) * 0.33 - self.recoil * 7

		if self.currentTarget != None:
			self.turretBase.lookAt(self.currentTarget.x, self.currentTarget.y)
		
		if self.shootDelay <= 0:
			if self.currentTarget != None:
				self.shootDelay += self.shootInterval
				
				self.recoil = 1
				self.projectiles.append(Dart(app, self.currentTarget, self))
		else:
			self.shootDelay -= app.deltaTime

		for i in self.projectiles:
			i.update(app)
			
	def destroy(self, app):
		#destroy all projectiles, own building structures, etc
		pass
