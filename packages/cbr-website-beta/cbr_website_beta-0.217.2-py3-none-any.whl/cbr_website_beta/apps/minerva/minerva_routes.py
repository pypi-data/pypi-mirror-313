from cbr_website_beta.apps.minerva                           import blueprint
from cbr_website_beta.cbr__flask.decorators.allow_annonymous import allow_anonymous

EXPECTED_ROUTES__MINERVA = [ '/minerva']

@blueprint.route('')
@allow_anonymous
def minerva_root():
    from flask import render_template
    return render_template('minerva/index.html')

