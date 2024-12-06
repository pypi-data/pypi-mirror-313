import requests
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_aws.apis.shell.Shell_Client  import Shell_Client
from osbot_utils.utils.Dev              import pprint

CBR__LAMBDA_SHELL__DEFAULT_SERVER = 'https://dev.cyber-boardroom.com'
CBR__LAMBDA_SHELL__PATH           = '{server}/web/dev/lambda-shell'

class CBR__Remote_Shell(Shell_Client, Type_Safe):

    def __init__(self, target_server=None):
        self.target_server = target_server or CBR__LAMBDA_SHELL__DEFAULT_SERVER

    def _invoke(self, method_name, method_kwargs=None, return_logs=False):
        auth_key = self._lambda_auth_key()
        url      = CBR__LAMBDA_SHELL__PATH.format(server=self.target_server)
        payload  = {'lambda_shell': {'method_name'  : method_name    ,
                                     'method_kwargs': method_kwargs  ,
                                     'auth_key'     : auth_key       }}
        response = requests.post(url, json=payload)
        if response.headers.get('Content-Type') == 'application/json':
            return response.json()
        return response.text.strip()

    def exec_print(self, executable, *params):
        result = self.exec(executable, params)
        pprint(result)
        return result

    def function(self, function):
        return self.python_exec_function(function)

    def function__print(self,function):
        result = self.function(function)
        pprint(result)
        return result

    # helper excution methods

    def env_vars(self):
        def return_dict_environ():
            from os import environ
            return dict(environ)
        return self.function(return_dict_environ)