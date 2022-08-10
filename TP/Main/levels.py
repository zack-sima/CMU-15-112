import random
def init(app, level):
	app.currentRound = 0 #one round can have multiple waves, one wave multiple square spawns
	app.currentWave = 0 #wave refers to the wave of square type coming within a round
	app.enemySpawnDelay = 5 #5 seconds to begin game

	app.currentEnemySpawn = 0 #current number of squares spawned

	#enemy properties: health, speed, reward (defined by color)
	app.enemyTypes = {"red": (5, 1, 1), "blue": (10, 1.5, 2), "green": (20, 2, 3),
	"yellow": (35, 3, 4), "pink": (50, 4, 5), "black": (80, 1.5, 7), "white": (120, 1.8, 10),
	"gray": (200, 0.5, 10), "purple": (500, 0.75, 20), "cyan": (150, 3.5, 20), "orange": (1000, 0.7, 50),
	}

	if level == 1:
		initLevel1(app)
	else:
		raise Exception("error: no levels to initialize")

#level 1 setup
def initLevel1(app):
	#rounds: list of waves; 
	#wave: (color, number spawned, interval between spawn, pause after spawning, spawn path)
	#note if spawn path missing it is assumed to be 0 or randomized if map allows
	app.rounds = [
		#round 1
		[["red", 5, 2, 5]],

		#round 2
		[["red", 10, 1, 1]],

		#round 3
		[["blue", 5, 2, 5]],

		#round 4
		[["red", 10, 0.7, 1], ["blue", 3, 1, 5]],

		#round 5
		[["red", 25, 0.35, 5]],

		#round 6
		[["green", 5, 2, 1], ["blue", 10, 1, 5]],

		#round 7
		[["blue", 15, 0.7, 1], ["green", 5, 1, 1], ["red", 30, 0.3, 5]],

		#round 8
		[["green", 15, 0.8, 1], ["blue", 25, 0.5, 5]],

		#round 9
		[["red", 50, 0.15, 5]],

		#round 10 (boss round]
		[["gray", 3, 1, 10]],

		#round 11
		[["blue", 20, 0.35, 2], ["green", 20, 0.7, 2], ["yellow", 5, 1.5, 5]],

		#round 12
		[["red", 30, 0.2, 1], ["blue", 30, 0.25, 1], ["green", 30, 0.5, 5]],

		#round 13
		[["yellow", 5, 0.5, 1], ["blue", 50, 0.15, 5]],

		#round 14
		[["green", 50, 0.3, 5]],

		#round 15
		[["black", 5, 1, 5]],

		#round 16
		[["yellow", 20, 0.5, 1], ["blue", 100, 0.12, 5]],

		#round 17
		[["green", 30, 0.2, 1], ["pink", 5, 0.3, 5]],

		#round 18
		[["red", 30, 0.1, 0.1], ["yellow", 5, 0.2, 0.2], ["red", 30, 0.1, 0.1], ["green", 15, 0.15, 0.2], ["pink", 3, 0.5, 5]],

		#round 19
		[["blue", 150, 0.07, 5]],

		#round 20 (boss round]
		[["purple", 5, 2, 5]],
	]
	#randomize spawns if not explicitly assigned
	for i in app.rounds:
		for j in i:
			if len(j) == 4:
				j.append(random.randint(0, 1))

	#current wave
	app.enemyWave = app.rounds[app.currentRound]
