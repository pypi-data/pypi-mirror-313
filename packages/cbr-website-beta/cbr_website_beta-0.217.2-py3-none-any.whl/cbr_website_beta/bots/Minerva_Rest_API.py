from urllib.parse import urljoin

import requests


class Minerva_Rest_API:

    def __init__(self):
        self.url = "https://minerva-dev.cyber-boardroom.com/"

    # utils
    def requests_get(self, path):
        url = urljoin(self.url, path)
        return requests.get(url).json()

    def version(self):
        return self.requests_get('/version')

    # methods
    def root(self):
        return self.requests_get('/')

    def aws_cost_explorer(self, days=7):
        return self.requests_get(f'/aws_cost_explorer?days={days}')