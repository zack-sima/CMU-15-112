Project Name:
112 Dynamic Defense

Description:
To run the game, run python[3.x] main.py inside the main folder.
To play the game, place towers on the map by dragging the buttons. Enemies come from entrances as shown by red arrows at the beginning of rounds. The enemies get progressively harder, so find a way to build a maze of towers and stop them!

Modules:
For the base game, no modules required. However, to run multiplayer, you need websockets installed. To install, use pip install websockets.

Shortcuts:
r: skip a round immediately
showmethemoney (type during gameplay): gives 100000 coins
showmethelives (type during gameplay): gives 100000 health

Note: multiplayer is very early, and only runs for two users. The game shouldn't crash if the multiplayer button isn't clicked, but if it is, I can't guarantee anything.

WARNING: for multiplayer to run properly, your python version must be 3.7+. Python 3.6 doesn't contain a method required to run this in its asyncio library.

To run multiplayer, have two players both open the program and click on the multiplayer button. You will see that there's now a "view opponent" button, where if your opponent exists (otherwise it does some weird thing) you can see their base. You will also see that now your buttons on the right are replaced by colored enemies you can send to your opponent for a small cost. Clicking it will cause one to be sent shortly to your opponent, and you should see your sent enemy pop up in your opponent's map (if you spam the buttons they may not send properly).

To host multiplayer, simply make a copy of the websocket_server.py and websocket_player_data.py and run it on a machine that has a public ip. Then, in the clients' websocket_client.py, change the link's ip to whatever ip/DNS your machine is running on. My server has a domain called us.retrocombat.com, and I'm designating the port as 8765 but it can be any port. To run multiplayer in the background I use nohup python[3.9] websocket_server.py &