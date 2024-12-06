import os

import jwt

from osbot_aws.apis.Cognito_IDP import Cognito_IDP
from osbot_utils.decorators.methods.cache_on_self import cache_on_self


class Cognito_Login:
    def __init__(self):
        self.cognito = Cognito_IDP()

    @cache_on_self
    def client_id(self):
        return os.environ.get("COGNITO_CLIENT_ID")

    def region(self):
        return os.environ.get("AWS_DEFAULT_REGION")

    def project(self):
        return os.environ.get("COGNITO_PROJECT")

    def user_pool_id(self):
        return os.environ.get("COGNITO_USER_POOL_ID")

    def login(self, username, password):
        login_result = {}
        result               = self.cognito.auth_initiate(self.client_id(), username, password)
        if result.get('error'):
            login_result['status'] = 'error'
            login_result['error' ] = str(result.get('error'))
        else:
            auth_result          = result.get('auth_result')
            raw_access_token     = auth_result.get('AccessToken')
            decoded_access_token = jwt.decode(raw_access_token, options={"verify_signature": False})
            login_result['status'      ] = 'ok'
            login_result['access_token'] = decoded_access_token
        return login_result