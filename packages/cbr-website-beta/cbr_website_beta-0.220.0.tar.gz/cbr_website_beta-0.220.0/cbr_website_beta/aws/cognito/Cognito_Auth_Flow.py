ERROR_MESSAGE__COGNITO_AUTH                  = 'could not authenticate user, please contact the Support team'
ERROR_MESSAGE__COGNITO_AUTH__NO_USER_CREATED = 'cloud not create user, please contact the Support team'

class Cognito_Auth_Flow:

    def convert_auth_code_to_auth_data(self, sign_in_code, redirect_uri):
        import requests

        project     = 'the-cbr-beta.auth'
        region      = "eu-west-2"
        client_id   = "5ij6l5kdho4umoks5rjfh9cbid"
        grant_type  = "authorization_code"

        token_url = f"https://{project}.{region}.amazoncognito.com/oauth2/token"

        payload = {
            "grant_type"  : grant_type,
            "client_id"   : client_id            ,
            "code"        : sign_in_code,
            "redirect_uri": redirect_uri
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(token_url, data=payload, headers=headers)
        return response.json()

    def create_cbr_token_cookie_from_cognito_code(self, sign_in_code):
        from cbr_website_beta.cbr__flask.utils.current_server   import current_server
        from osbot_aws.AWS_Config                               import aws_config
        from osbot_utils.utils.Status                           import status_ok, status_error

        try:
            aws_config.set_aws_session_region_name('eu-west-2')     # todo: remove this from here
            redirect_uri   = f"{current_server()}web/sign-in"
            cognito_tokens = self.convert_auth_code_to_auth_data(sign_in_code, redirect_uri)
            access_token   = cognito_tokens.get('access_token')
            user_info      = self.parse_jwt_token(access_token)
            db_user        = self.create_user    (user_info)                                 # create user if needed
            if not db_user:                                                                  # check that user was created ok
                return status_error(message = ERROR_MESSAGE__COGNITO_AUTH__NO_USER_CREATED)
            db_session     = self.create_session(user_info)                                  # creat new session for user
            session_id     = db_session.session_id
            data = {'cookie_value': session_id, 'user_info': user_info}
            return status_ok(data=data)
        except Exception as error:
            return status_error(message = ERROR_MESSAGE__COGNITO_AUTH ,
                                error   = f'{error}'                  )

    def create_user(self, user_info):
        from cbr_shared.cbr_sites.CBR__Shared_Objects           import cbr_shared_objects
        from cbr_shared.schemas.data_models.Model__User__Config import Model__User__Config

        db_users  = cbr_shared_objects.db_users()
        user_name = user_info.get('username')
        user_id   = user_info.get('sub')
        db_user   =  db_users.db_user(user_id)
        if db_user.exists():
            return db_user

        user_config = Model__User__Config(user_id=user_id, user_name=user_name)     # if user doesn't exist, using the user_name from cognito as a first value for user_nmae
        db_user.create(user_config=user_config)                                     # create user
        if db_user.exists():                                                        # double check that user was created ok
            return db_user


    def create_session(self, user_info):
        from cbr_shared.cbr_sites.CBR__Shared_Objects import cbr_shared_objects

        db_sessions = cbr_shared_objects.db_sessions()
        user_name   = user_info.get('username')
        user_jti    = user_info.get('jti')              # Cognito's JWT Token Identifier (changes on every login)
        user_id     = user_info.get('sub')              # Cognito's User Identifier      (never changes)
        session_id  = user_jti                          # we can use the jti as the session_id
        db_session  = db_sessions.db_session(session_id)
        db_session.create(user_id, user_name, user_info)
        return db_session

    def create_session_in_athena(self, user_info, cognito_tokens):
        from cbr_website_beta.bots.Athena_Rest_API             import Athena_Rest_API
        from cbr_website_beta.bots.schemas.Create_User_Session import Create_User_Session

        user_name       = user_info.get('username')
        session_id      = user_info.get('jti')
        source          = 'CognitoAuth'
        athena_rest_api = Athena_Rest_API()
        kwargs = dict(user_name     = user_name ,
                      session_id    = session_id,
                      source        = source    ,
                      cognito_tokens = cognito_tokens)
        create_user_session = Create_User_Session(**kwargs)
        response            = athena_rest_api.user__create_session(create_user_session)
        if 'session_id' in response:
            session_id           = response.get('session_id')
            return session_id
        raise Exception(f'no session_id in response: {response}')



    def parse_jwt_token(self, access_token):
        import jwt
        decoded_access_token = jwt.decode(access_token, algorithms=["RS256"], options={"verify_signature": False})
        return decoded_access_token
