from flask import Blueprint

EXPECTED_ROUTES__ROOT = ['/athena',
                         '/home',
                         '/home.html',
                         '/version',
                         '/chat-with-llms',
                         '/chat/single',
                         '/chat/history',
                         '/chat/view/<chat_id>']

blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix='/web'
)
