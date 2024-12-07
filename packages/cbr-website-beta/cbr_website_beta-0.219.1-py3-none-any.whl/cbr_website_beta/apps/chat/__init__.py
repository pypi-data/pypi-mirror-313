from flask import Blueprint

blueprint = Blueprint(
    'chat_blueprint',
    __name__,
    url_prefix='/web/chat'
)
