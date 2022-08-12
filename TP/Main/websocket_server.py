#https://websockets.readthedocs.io/en/stable/
import asyncio
import websockets
import json
import websocket_player_data

async def echo(websocket):
	global players
	assignedPlayerId = -1 #remove this player upon any sort of error (disconnect, etc)
	try:
		async for message in websocket:
			if message == "request_id":
				pid = -1

				index = 0
				for p in players:
					if p.playerId == -1:
						pid = index
						p.playerId = index
						assignedPlayerId = index
						print(f"assigned id: {index}")
						break
					index += 1
				await websocket.send(str(pid))
			else:
				player = websocket_player_data.PlayerData.fromJSON(message)
				players[player.playerId] = player

				otherPlayer = None

				#send info of other player
				if player.playerId == 0:
					otherPlayer = players[1]
				else:
					otherPlayer = players[0]

				if otherPlayer.playerId == -1: #other player not joined yet
					await websocket.send("wait")

				await websocket.send(websocket_player_data.PlayerData.toJSON(otherPlayer))
	except Exception as e:
		if assignedPlayerId != -1:
			#clean player
			print(f"connection dropped: {e}")
		else:
			print(f"connection error: {e}")

	if assignedPlayerId != -1:
		players[assignedPlayerId] = websocket_player_data.PlayerData(-1, None, None)
		print(f"removed player {assignedPlayerId}")

async def main():
	async with websockets.serve(echo, "0.0.0.0", 8765):
		await asyncio.Future()  # run forever

players = []

def init():
	global players
	for i in range(2):
		players.append(websocket_player_data.PlayerData(-1, None, None))

	asyncio.run(main())

if __name__ == "__main__":
	init()