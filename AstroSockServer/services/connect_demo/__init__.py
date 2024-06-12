from flask import Blueprint

blueprint = Blueprint('connect_demo', __name__, template_folder='templates', static_folder='static')

import services.connect_demo.views
