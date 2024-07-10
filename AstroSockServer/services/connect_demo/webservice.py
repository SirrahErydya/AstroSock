import asyncio
from services.connect_demo.connect4 import PLAYER1, PLAYER2, Connect4
import websockets
import itertools
import json


async def handler(websocket):
    # Initialize a Connect Four game.
    game = Connect4()

    # Players take alternate turns, using the same browser.
    turns = itertools.cycle([PLAYER1, PLAYER2])
    player = next(turns)



    async for message in websocket:
        # Parse a "play" event from the UI.
        event = json.loads(message)
        print(message)
        if event['type'] == 'datacube_broadcast':
            print("Connect demo received the datacube broadcast!")

        elif event["type"] == "play":
            column = event["column"]

            try:
                # Play the move.
                row = game.play(player, column)
            except RuntimeError as exc:

                # Send an "error" event if the move was illegal.
                event = {
                    "type": "error",
                    "message": str(exc),

                }
                await websocket.send(json.dumps(event))
                continue

            # Send a "play" event to update the UI.
            event = {
                "service": 'connect_demo',
                "type": "play",
                "player": player,
                "column": column,
                "row": row,
            }
            await websocket.send(json.dumps(event))

            # If move is winning, send a "win" event.
            if game.winner is not None:
                event = {
                    "type": "win",
                    "player": game.winner,
                }
                await websocket.send(json.dumps(event))

            # Alternate turns.
            player = next(turns)


async def main(port):
    async with websockets.serve(handler, "", port):
        await asyncio.Future()  # run forever


def run(port):
    asyncio.run(main(port))


if __name__ == "__main__":
    asyncio.run(main(8001))
