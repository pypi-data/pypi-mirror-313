import os


class Cognito_Test_Users:

    def cognito_client_id(self):
        return os.environ.get("COGNITO_CLIENT_ID")

    def cognito_project(self):
        return os.environ.get("COGNITO_PROJECT")

    def cognito_region(self):
        return os.environ.get("AWS_DEFAULT_REGION")

    def cognito_user_pool_id(self):
        return os.environ.get("COGNITO_USER_POOL_ID")

    def credentials__user_1(self):
        username = os.environ.get("COGNITO_USER_NAME_1")
        password = os.environ.get("COGNITO_USER_PWD_1")
        return username, password
