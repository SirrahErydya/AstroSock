from . import blueprint
from flask import render_template, url_for, session
import os
from services.spherinator.models import Survey


@blueprint.route('spherinator/<port>')
def spherinator(port):
    surveys = Survey.select_all()
    return render_template('spherinator.html', port=port, surveys=surveys, services=session['services'])

@blueprint.route('spherinator/<port>/<survey_id>')
def survey(port, survey_id):
    survey_obj = Survey.select_by_id(survey_id)
    return render_template('survey.html', port=port, survey=survey_obj)
