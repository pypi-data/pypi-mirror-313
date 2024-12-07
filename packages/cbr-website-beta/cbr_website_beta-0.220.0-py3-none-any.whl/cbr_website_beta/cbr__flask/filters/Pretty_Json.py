import json


class Pretty_Json:

    filter_name = 'pretty_json'

    def __init__(self, app):
        app.jinja_env.filters[self.filter_name] = self.pretty_json_filter # todo: find a better way to register these filters

    def pretty_json_filter(self,data):
        return json.dumps(data, indent=4)