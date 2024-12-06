import sys

import cbr_website_beta

from osbot_utils.utils.Files import path_combine, file_contents
from osbot_utils.utils.Json import json_file_load, json_file_create


class Site_Utils:

    def path_code_root(self):
        return cbr_website_beta.__path__[0]

    def path_source_code_root(self):
        return path_combine(self.path_code_root(), '..')

    @staticmethod
    def running_in_pytest():
        return 'pytest' in sys.modules
