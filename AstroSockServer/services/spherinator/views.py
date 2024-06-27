from . import blueprint
from flask import render_template, url_for
import os
from services.spherinator.models import Survey


@blueprint.route('spherinator/<port>')
def spherinator(port):
    surveys_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'surveys')
    surveys = Survey.select_all()
    survey_paths = [ os.path.join(surveys_folder, survey.name) for survey in surveys]
    return render_template('spherinator.html', port=port, survey_paths=survey_paths, surveys=surveys)
