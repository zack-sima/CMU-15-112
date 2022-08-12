#https://websockets.readthedocs.io/en/stable/
import asyncio
import websockets
import json
import time
import main
import websocket_player_data

async def mainFunc(app):
	link = "ws://us.retrocombat.com:8765"
	#link = "ws://localhost:8765"
	
	async with websockets.connect(link) as websocket:
		while True:
			if app.playerId == -1:
				await websocket.send("request_id")
			else:
				player = websocket_player_data.PlayerData(app.playerId, app.towers, app.enemies)
				print(f"sent: {websocket_player_data.PlayerData.toJSON(player)}")
				await websocket.send(websocket_player_data.PlayerData.toJSON(player))

			msg = str(await websocket.recv()).replace("\n", "") 
			print(f"received: { msg }")

			if msg.isdigit() and app.playerId == -1: #receiving player id
				print("assigning player id, loading game")
				app.playerId = int(msg)
				main.loadMultiplayer(app)
			else:
				#check if game is starting
				if msg != "wait":
					#parse data (other player)
					try:
						app.otherPlayer = websocket_player_data.PlayerData.fromJSON(msg)
						#update
					except:
						print("could not decipher json msg")
				else:
					app.otherPlayer = None


			time.sleep(0.1)
	# except Exception as e:
	# 	print("websockets failed: " + str(e))

def init(app):
	app.playerId = -1
	asyncio.run(mainFunc(app))