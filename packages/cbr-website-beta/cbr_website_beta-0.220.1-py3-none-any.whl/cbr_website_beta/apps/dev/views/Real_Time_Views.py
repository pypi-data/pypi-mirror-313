from flask import render_template

from cbr_website_beta.aws.apigateway.web_sockets.WS__Users import WS__Users


class Real_Time_Views:

    def __init__(self):
        self.ws_users = WS__Users()

