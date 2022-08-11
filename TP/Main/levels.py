import random
def init(app, level):
	app.currentRound = 0 #one round can have multiple waves, one wave multiple square spawns

	app.currentWave = 0 #wave refers to the wave of square type coming within a round
	app.enemySpawnDelay = 5 #5 seconds to begin game

	app.currentEnemySpawn = 0 #current number of squares spawned

	#enemy properties: health, speed, reward (defined by color)
	app.enemyTypes = {"red": [5, 1, 1], "blue": [10, 1.5, 2], "green": [20, 2, 3],
	"yellow": [35, 3, 4], "pink": [50, 4, 5], "black": [80, 1.5, 7], "white": [120, 1.8, 10],
	"gray": [175, 0.75, 10], "purple": [500, 0.75, 20], "cyan": [150, 3.5, 20], "orange": [1000, 0.7, 50],
	"sienna": [500, 1.5, 50], "lightblue": [3500, 0.5, 100], "lightred": [7000, 0.45, 200], "darkolivegreen": [15000, 0.75, 500]
	}

	for v in app.enemyTypes.values():
		v[0] = int(v[0] * (1 + (app.difficulty - 1) * 0.15)) #15% harder per additional difficulty after normal

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
		#also, some rounds come from https://bloons.fandom.com/wiki/Rounds_(BTD6)?file=RoundSummaryBTD6.png
		
		#round 1
		[["red", 5, 2, 5]],

		#round 2
		[["red", 10, 1, 5]],

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

		#round 10 (boss round)
		[["gray", 3, 2, 5]],

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

		#round 20 (boss round)
		[["purple", 5, 2, 5]],

		#round 21
		[["yellow", 40, 0.42, 1], ["pink", 15, 0.5, 5]],

		#round 22
		[["white", 16, 0.8, 5]],

		#round 23
		[["black", 10, 0.1, 1], ["white", 7, 0.1, 5]],

		#round 24
		[["blue", 50, 0.1, 1], ["gray", 15, 1, 5]],

		#round 25
		[["pink", 25, 0.42, 1], ["purple", 3, 3, 5]],

		#round 26
		[["gray", 5, 1.2, 1], ["pink", 10, 0.5, 1], ["gray", 15, 1.2, 5]],

		#round 27
		[["pink", 35, 0.05, 1], ["blue", 100, 0.08, 1], ["green", 70, 0.1, 1], ["yellow", 50, 0.2, 5]],

		#round 28
		[["purple", 2, 1.5, 1], ["pink", 15, 0.15, 1], ["purple", 3, 1.5, 1], ["yellow", 25, 0.1, 1], ["purple", 5, 2, 5]],

		#round 29
		[["yellow", 50, 0.1, 1], ["pink", 150, 0.2, 5]],

		#round 30 (boss round)
		[["orange", 7, 2, 5]],

		#round 31
		[["black", 20, 0.35, 1], ["white", 20, 0.3, 1], ["gray", 20, 0.25, 5]],

		#round 32
		[["white", 35, 0.35, 1], ["cyan", 5, 0.5, 5]],

		#round 33
		[["yellow", 120, 0.1, 1], ["pink", 120, 0.15, 5]],

		#round 34
		[["pink", 50, 0.12, 1], ["gray", 50, 0.15, 5]],

		#round 35
		[["orange", 3, 1.5, 3], ["purple", 5, 2.5, 3], ["cyan", 10, 0.5, 5]],

		#round 36
		[["white", 50, 0.1, 1], ["pink", 30, 0.15, 1], ["green", 100, 0.05, 5]],

		#round 37
		[["black", 30, 0.1, 1], ["white", 30, 0.15, 1], ["gray", 30, 0.2, 1], ["purple", 10, 1, 5]],

		#round 38
		[["pink", 30, 0.1, 1], ["white", 30, 0.15, 1], ["gray", 30, 0.2, 1], ["purple", 10, 1, 5]],

		#round 39
		[["gray", 100, 0.15, 5]],

		#round 40 (boss round)
		[["sienna", 25, 1, 5]],

		#round 41
		[["cyan", 25, 0.35, 1], ["white", 50, 0.12, 5]],

		#round 41
		[["pink", 100, 0.08, 1], ["orange", 15, 1, 5]],

	]

	#randomize spawns if not explicitly assigned
	for i in app.rounds:
		for j in i:
			if len(j) == 4:
				j.append(random.randint(0, 3))

	#current wave
	app.enemyWave = app.rounds[app.currentRound]
