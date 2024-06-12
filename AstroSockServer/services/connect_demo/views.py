from . import blueprint
from flask import render_template


@blueprint.route('connect_demo/<port>')
def connect_demo(port):
    return render_template('connect_template.html', port=port)
