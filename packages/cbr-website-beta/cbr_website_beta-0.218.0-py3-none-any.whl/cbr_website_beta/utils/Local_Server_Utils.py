from os import environ

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import datetime_now


class Local_Server_Utils():


    def send_startup_ws_message(self):
        in_local_server = environ.get('LOCAL_SERVER')
        if in_local_server == 'True':
            from cbr_website_beta.aws.apigateway.web_sockets.WS__Users import WS__Users
            ws_users = WS__Users()
            print('>>>>> starting local flask server <<<<<<<')
            topic = 'system'
            data  = f'local flask server starting: {datetime_now()}'
            ws_users.send_to_active_connections(topic, data)
