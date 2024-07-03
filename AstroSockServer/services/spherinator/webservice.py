import asyncio
import websockets
import json
import healpy
from .models import Survey


def find_datacube(survey, order, theta, phi):
    n_side = 2**order
    pixel = healpy.ang2pix(n_side, theta, phi, nest=True)
    hierarchy = survey.hierarchy



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
