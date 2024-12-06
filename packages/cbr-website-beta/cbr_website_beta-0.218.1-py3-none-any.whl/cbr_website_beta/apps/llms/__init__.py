from flask import Blueprint

blueprint = Blueprint(
    'llms_blueprint',
    __name__,
    url_prefix='/web/llms'
)
