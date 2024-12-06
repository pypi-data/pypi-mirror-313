from cbr_website_beta.cbr__flask.Flask_Site import Flask_Site
from cbr_website_beta.cbr__flask.filters.Current_User import client__logged_in

class API_Request:
    def __init__(self, path='/', username=None, user_groups=None, app=None):
        self.path         = path
        self.app          = app or Flask_Site().app()
        if username:
            self.client = client__logged_in(app=self.app, user_name=username, user_groups=user_groups)
        else:
            self.client   = self.app.test_client()
        self.response     = None


    def __enter__(self):
        self.response    = self.client.get(self.path)
        return self, self.response.json

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass