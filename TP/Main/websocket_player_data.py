from types import SimpleNamespace
import json

class PlayerData:
	def __init__(self, playerId, towers, enemies, opponentSpawnColor):
		self.playerId = playerId
		#instead of classes, have a list of elements:
		#[x, y, rotation, tower type, tower level]
		self.towers = []
		if towers != None:
			for t in towers:
				self.towers.append([t.col, t.row, t.turretBase.rotation, t.level, t.turretBase.color]) #just have coordinates for now

		self.enemies = []
		if enemies != None:
			for e in enemies:
				self.enemies.append([e.x, e.y, e.color, e.health])

		self.opponentSpawnColor = opponentSpawnColor

	@staticmethod
	def toJSON(obj):
		#from https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
		return str(json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=0, separators=(',',':'))).replace("\n", "")

	@staticmethod
	def fromJSON(jsonStr):
		#from https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
		player = json.loads(jsonStr, object_hook=lambda d: SimpleNamespace(**d))
		return player