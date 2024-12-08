import json

from osbot_utils.utils.Misc import str_to_base64, base64_to_str


class Misc_Filters:

    def __init__(self, app):
        app.jinja_env.filters['to_base64'  ] = self.filter__str_to_base64
        app.jinja_env.filters['from_base64'] = self.filter__base64_to_str

    def filter__str_to_base64(self, target):
        return str_to_base64(target)

    def filter__base64_to_str(self, target):
        return base64_to_str(target)
