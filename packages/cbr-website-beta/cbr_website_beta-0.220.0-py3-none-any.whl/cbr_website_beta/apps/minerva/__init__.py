from flask import Blueprint

blueprint = Blueprint(
    'minerva_blueprint',
    __name__,
    url_prefix='/web/minerva'
)
