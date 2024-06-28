from . import blueprint
from flask import render_template, url_for
import os
from services.spherinator.models import Survey


@blueprint.route('spherinator/<port>')
def spherinator(port):
    surveys = Survey.select_all()
    survey_map = {}
    for survey in surveys:
        survey_path = url_for('.static', filename='surveys/'+survey.name)
        survey_map[survey.name] = survey_path
    return render_template('spherinator.html', port=port, survey_map=survey_map, surveys=surveys)
