from cbr_website_beta.cbr__flask.Flask_Site import Flask_Site
from cbr_website_beta.cbr__flask.filters.Current_User import client__logged_in
from osbot_playwright.html_parser.Html_Parser import Html_Parser


class Render_Element:
    def __init__(self, path='/', method='GET', data=None, headers=None, element_id=None, tag=None, username=None, user_groups=None, app=None):
        self.method       = method
        self.data         = data
        self.element_id   = element_id
        self.headers      = headers
        self.path         = path
        self.tag          = tag
        self.app          = app or Flask_Site().app()
        if username:
            self.client = client__logged_in(app=self.app, user_name=username, user_groups=user_groups)
        else:
            self.client       = self.app.test_client()
        self.contents     = None
        self.html_parser  = None
        self.raw_element  = None
        self.response     = None


    def __enter__(self):
        self.response    = self.client.open(self.path, method=self.method, data=self.data, headers=self.headers)
        self.html_parser = Html_Parser(self.response.data)
        if self.tag:
            self.raw_element = self.html_parser.soup.find(self.tag)
        else:
            self.raw_element = self.html_parser.soup.find(id=self.element_id)
        if self.raw_element:
            self.contents = Html_Parser(self.raw_element.decode_contents())
        return self, self.contents

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def html(self):
        return self.html_parser.html()

    def title(self):
        return self.html_parser.title()

