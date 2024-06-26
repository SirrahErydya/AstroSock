from . import blueprint
from flask import render_template, url_for


@blueprint.route('spherinator/<port>')
def spherinator(port):
    surveys_folder = url_for('.static', filename='surveys')
    return render_template('spherinator.html', port=port)
