from flask import Blueprint

blueprint = Blueprint('spherinator', __name__, template_folder='templates', static_folder='static',
                      static_url_path='spherinator/static')

import services.spherinator.views
