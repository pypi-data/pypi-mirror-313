from flask import Blueprint

blueprint = Blueprint(
    'root_blueprint',
    __name__,
    url_prefix='/web'
)