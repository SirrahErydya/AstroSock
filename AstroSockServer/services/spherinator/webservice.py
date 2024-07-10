import asyncio
import websockets
import json
import healpy
from .models import Survey, SpherinatorCell
from utils import PUBLISHER

SUBSCRIBERS = set()

def pick_cell(survey, order, theta, phi):
    hierarchy = survey["hierarchy"]
    n_order = order + hierarchy
    n_side = 2**n_order
    pixel = healpy.ang2pix(n_side, theta, phi, nest=True)
    cell = SpherinatorCell.select_by_healpix(n_order, pixel)
    if not cell:
        return {}
    cube_paths = {}
    data_aspects = cell.survey.data_aspects
    for dim in data_aspects.keys():
        for aspect in data_aspects[dim]:
            path = cell.survey.survey_url() + '/data_cube/' + dim + '/' + aspect + '/' + cell.dp_id
            cube_paths[aspect] = path
    cell_info = {
        'cell': cell.to_json(),
        'data_aspects': data_aspects,
        'cube_paths': cube_paths
    }
    return cell_info


async def subscribe(websocket):
    print("Subscribing...")
    SUBSCRIBERS.add(websocket)

async def handler(websocket):
    async for message in websocket:
        msg = json.loads(message)
        if msg['type'] == "subscribe":
            await subscribe(websocket)

        if msg['type'] == 'pick_spherinator_cell':
            broadcast_message = {
                'type': 'datacube_broadcast',
                'cell_info': pick_cell(msg['survey'], msg['order'], msg['theta'], msg['phi'])
            }
            #print(broadcast_message)
            for sub in SUBSCRIBERS:
                await sub.send(json.dumps(broadcast_message))



async def main(port):
    async with websockets.serve(handler, "", port):
        await asyncio.Future()  # run forever


def run(port):
    asyncio.run(main(port))
