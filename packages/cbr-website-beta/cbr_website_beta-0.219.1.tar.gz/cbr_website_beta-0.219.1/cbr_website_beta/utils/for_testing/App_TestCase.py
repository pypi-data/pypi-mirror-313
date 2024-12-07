from flask import Flask
from flask.testing import FlaskClient
from flask_testing import TestCase

from cbr_website_beta.cbr__flask.Flask_Site                  import Flask_Site
from cbr_website_beta.utils.app_client.API_Request      import API_Request
from cbr_website_beta.utils.app_client.Render_Element   import Render_Element
from osbot_playwright.html_parser.Html_Parser           import Html_Parser
from osbot_utils.utils.Json                             import json_dumps


class App_TestCase(TestCase):

    app   : Flask
    client: FlaskClient

    def api_request(self, path='/',  username=None, user_groups=None):
        kwargs = { 'path'       : path          ,
                   'username'   : username      ,
                   'user_groups': user_groups   ,
                   'app'        : self.app      }
        return API_Request(**kwargs)

    def render_element(self, path='/', method='GET', data=None, headers=None, element_id=None, tag=None, username=None, user_groups=None):
        kwargs = { 'path'       : path          ,
                   'method'     : method        ,
                   'data'       : data          ,
                   'element_id' : element_id    ,
                   'headers'    : headers       ,
                   'tag'        : tag           ,
                   'username'   : username      ,
                   'user_groups': user_groups   ,
                   'app'        : self.app      }
        return Render_Element(**kwargs)

    def render_element_post_json(self, path='/', data=None, headers=None, element_id=None, tag=None, username=None, user_groups=None):
        if headers is None:
            headers = {}
        headers['Content-Type'] = 'application/json'
        if type(data) is not str:
            data = json_dumps(data)

        kwargs = { 'path'       : path          ,
                   'method'     : 'POST'        ,
                   'data'       : data          ,
                   'element_id' : element_id    ,
                   'headers'    : headers       ,
                   'tag'        : tag           ,
                   'username'   : username      ,
                   'user_groups': user_groups   ,
                   'app'        : self.app      }
        return Render_Element(**kwargs)


    def create_app(self):
        #self.app = app                         # todo fix the tests that break when we only use this one version of app (prob is with the cases where we need to have a logged in user in testclient )
        self.app = Flask_Site().app()           # called 20 times and takes about 20ms (which adds)
        return self.app

    def setUp(self) -> None:
        self.client = self.app.test_client()

    def get(self, path, status_code=200):
        response    = self.client.get(path)
        html_parser = Html_Parser(response.data)
        assert response.status_code == status_code
        return html_parser

    def get_raw(self, path):
        return self.client.get(path)

    def template(self, index=0):
        if len(self.templates) > index:
            template, context = self.templates[index]
            return template

    def template_context(self, index=0):
        if len(self.templates) > index:
            template, context = self.templates[index]
            return context
        return {}