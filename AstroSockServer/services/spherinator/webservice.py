import asyncio
import websockets
import json
import healpy
from .models import Survey, SpherinatorCell
from flask import session


def pick_cell(survey, order, theta, phi):
    hierarchy = survey.hierarchy
    n_side = 2**(order+hierarchy)
    pixel = healpy.ang2pix(n_side, theta, phi, nest=True)
    cell = SpherinatorCell.select_by_healpix(order, pixel)
    cube_paths = {}
    data_aspects = cell.survey.data_aspects()
    for dim in data_aspects.keys():
        for aspect in data_aspects[dim]:
            path = cell.survey.survey_url() + '/data_cube/' + dim + '/' + aspect + '/' + cell.dp_id
            cube_paths['aspect'] = path
    cell_info = {
        'cell': cell.to_json(),
        'data_aspects': data_aspects,
        'cube_paths': cube_paths
    }
    return cell_info


async def handler(websocket):
    session['sockets']['spherinator'] = websocket

    async for message in websocket:
        # Todo: Fill with actual logic
        msg = json.loads(message)
        if msg['type'] == "datacube_broadcast":
            print("Spherinator got the datacube broadcast!")
        if msg['type'] == 'pick_spherinator_cell':
            broadcast_message = {
                'type': 'datacube_broadcast',
                'cell_info': pick_cell(msg['survey'], msg['order'], msg['theta'], msg['phi'])
            }
            websockets.broadcast(session['sockets'].values(), broadcast_message)



async def main(port):
    async with websockets.serve(handler, "", port):
        await asyncio.Future()  # run forever


def run(port):
    asyncio.run(main(port))
