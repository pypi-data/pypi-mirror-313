from flask import Blueprint

blueprint = Blueprint(
    'docs_blueprint',
    __name__,
    url_prefix='/web/docs'
)
