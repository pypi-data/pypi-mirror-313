from flask import Blueprint

blueprint = Blueprint(
    'dev_blueprint',
    __name__,
    url_prefix='/web/dev'
)
