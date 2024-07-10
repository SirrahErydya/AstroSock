import asyncio
import websockets
import json

SUBSCRIBERS = set()


async def subscribe(websocket):
    print("Subscribing...")
    SUBSCRIBERS.add(websocket)


async def handler(websocket):
    async for message in websocket:
        msg = json.loads(message)
        if msg['type'] == "subscribe":
            await subscribe(websocket)

        if msg['type'] == 'publish':
            #print(broadcast_message)
            for sub in SUBSCRIBERS:
                await sub.send(json.dumps(msg["publish_msg"]))


async def main(port):
    async with websockets.serve(handler, "", port):
        await asyncio.Future()  # run forever
