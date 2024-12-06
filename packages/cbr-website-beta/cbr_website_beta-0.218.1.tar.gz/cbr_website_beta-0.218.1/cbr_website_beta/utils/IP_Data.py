import os

from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Env import load_dotenv
from osbot_utils.utils.Http import GET_json


ENV_VAR__IP_DATA__API_KEY = 'IP_DATA__API_KEY'
SERVER__IP_DATA_API       = 'https://api.ipdata.co/'

# todo: add support for caching (in dynamodb) the data received from the ipdata.co API since it shouldn't change that often
class IP_Data:

    @cache_on_self
    def api_key(self):
        load_dotenv()
        return os.environ.get(ENV_VAR__IP_DATA__API_KEY, '')

    def request_get(self, ip_address):
        if ip_address:
            try:
                url = f'{SERVER__IP_DATA_API}{ip_address}?api-key={self.api_key()}'
                return GET_json(url)
            except:
                pass                            # todo: add better error detection and logging
        return {}
