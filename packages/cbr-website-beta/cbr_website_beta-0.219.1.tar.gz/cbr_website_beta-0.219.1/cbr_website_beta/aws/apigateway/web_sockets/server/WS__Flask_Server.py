import logging

import flask
from flask import Flask, render_template
from flask_socketio import emit, send, SocketIO

from cbr_website_beta.utils.Site_Utils import Site_Utils
from cbr_website_beta.utils.Version import Version
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.testing.Logging import Logging
from osbot_utils.utils.Misc import list_set

WS_FLASK__ROUTES__FLASK    = ['/'                       ,
                              '/static/<path:filename>' ,
                              '/test-ws'                ,
                              '/version'                ]
WS_FLASK__ROUTES__SOCKETIO = ['connect', 'disconnect', 'json', 'message']
WS_FLASK__ROUTES__ALL      = WS_FLASK__ROUTES__FLASK + WS_FLASK__ROUTES__SOCKETIO

active_sids = []
class WS__Flask_Server(Kwargs_To_Self):

    def __init__(self):
        super().__init__()
        self.logging      = Logging()
        self.log_handler = self.logging.log_to_sys_stdout()
        #self.logging.enable_pycharm_logging()

    @cache_on_self
    def app(self):
        self.logging.info('in WS__Flask_Server app()')
        app = Flask(__name__)
        app.logger.setLevel(logging.DEBUG)
        #app.logger.addHandler(self.log_handler)
        app.config['SECRET_KEY'] = 'secret!'
        return app

    @cache_on_self
    def socketio(self):
        return SocketIO(self.app())

    def setup(self):
        self.setup_routes()
        return self

    def setup_routes(self):
        app      = self.app()
        socketio = self.socketio()

        @app.route('/')
        def page__root():
            return render_template('index.html')

        @app.route('/test-ws')
        def page__test_ws():
            return render_template('test-ws.html')

        @app.route('/version')
        def version():
            return Version().value()

        @socketio.on('connect')
        def handle_connect():
            active_sids.append(flask.request.sid)
            connect_message = f'sid:{flask.request.sid}'
            emit('after connect', {'data': connect_message})

        @socketio.on('disconnect')
        def handle_disconnect():
            active_sids.remove(flask.request.sid)
            print('Client disconnected')

        @socketio.on('message')
        def handle_message(message):
            print('Received message:', message)
            send(f'Response back to the message: {message}')
            #self.sent_manually('manual message')

        @app.route('/send_manually/<to>/<message>')
        def send_manually(to:str, message:str):
            self.sent_manually(message, to=to)
            return f"send message to: {to}"

        @app.route('/send_all/<message>')
        def send_all(message: str):
            for active_sid in active_sids:
                self.sent_manually(message, to=active_sid)
            return f"send message to: {active_sids}"

        @app.route('/active_sids')
        def send_active_sids():
            return f"{active_sids}"

        @socketio.on('json')
        def handle_json(json):
            reply = dict(source='handle_json',json=json)
            print('Received json:', json)
            send(reply, json=True)

    def routes(self):
        return self.routes__flask() + self.routes__socketio()

    def routes__flask(self):
        return [rule.rule for rule in self.app().url_map.iter_rules()]

    def routes__socketio(self):
        root_handler = self.socketio().server.handlers.get('/')
        return list_set(root_handler)

    def sent_manually(self, message, **kwargs):
        json = kwargs.get('json', False)
        # if 'namespace' in kwargs:
        #     namespace = kwargs['namespace']
        # else:
        #     namespace = flask.request.namespace
        namespace = None
        callback = kwargs.get('callback')
        broadcast = kwargs.get('broadcast')
        to = kwargs.pop('to', None) or kwargs.pop('room', None)
        if to is None and not broadcast:
            to = flask.request.sid
        include_self = kwargs.get('include_self', True)
        skip_sid = kwargs.get('skip_sid')
        ignore_queue = kwargs.get('ignore_queue', False)

        socketio = flask.current_app.extensions['socketio']
        response = socketio.send(message, json=json, namespace=namespace, to=to,
                             include_self=include_self, skip_sid=skip_sid,
                             callback=callback, ignore_queue=ignore_queue)
        print(response)
        print('---- message send ---')


if __name__ == '__main__':
    ws_flask = WS__Flask_Server().setup()
    app      = ws_flask.app()
    socketio = ws_flask.socketio()
    socketio.run(app, debug=True, port=5222)