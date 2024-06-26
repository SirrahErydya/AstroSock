import asyncio
import websockets
import json


async def handler(websocket):

    async for message in websocket:
        # Todo: Fill with actual logic
        msg = json.loads(message)
        print(msg)


async def main(port):
    async with websockets.serve(handler, "", port):
        await asyncio.Future()  # run forever


def run(port):
    asyncio.run(main(port))
