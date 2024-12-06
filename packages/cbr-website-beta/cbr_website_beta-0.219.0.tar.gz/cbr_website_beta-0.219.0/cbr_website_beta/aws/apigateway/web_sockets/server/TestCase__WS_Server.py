import socket
import threading
from unittest       import TestCase
from urllib.parse import urljoin

import requests
from flask          import Flask
from flask_socketio import SocketIO

from cbr_website_beta.aws.apigateway.web_sockets.server.WS__Flask_Server import WS__Flask_Server
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Http import wait_for_port, wait_for_http
from osbot_utils.utils.Objects import obj_info


class TestCase__WS_Server(TestCase):
    ws_flask      : WS__Flask_Server
    app           : Flask
    socketio      : SocketIO
    server_thread : threading.Thread
    port          : int

    @classmethod
    def setUpClass(cls):
        cls.ws_flask      = WS__Flask_Server().setup()
        cls.app           = cls.ws_flask.app()
        cls.socketio      = cls.ws_flask.socketio()
        cls.port          = cls.find_free_port()
        cls.server_thread = threading.Thread(target=cls.socketio.run, args=(cls.app,), kwargs={'port': cls.port})
        cls.server_thread.daemon = True  # This allows the thread to be killed when the main thread exits
        cls.server_thread.start()
        wait_for_port('127.0.0.1',cls.port)

    @classmethod
    def tearDownClass(cls):
        pass
        #cls.socketio.stop()
        #cls.server_thread.join()

    @staticmethod
    def find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]

    def http_get(self, path):
        url = urljoin(self.url(), path)
        return requests.get(url).text

    def url(self):
        return f'http://localhost:{self.port}'