from cbr_shared.cbr_backend.session.CBR__Session__Load      import cbr_session_load
from jinja2 import pass_context

USER_DATA_WITH_NO_CBR_TOKEN = ''
USER_DATA_WITH_BAD_FIELD    = 'bad_field'
DEFAULT_USER_NAME           = 'default_user_name'
DEFAULT_USER_GROUPS         = ['default_group']
DEFAULT_ADMIN_GROUPS        = ['CBR-Team']

class Current_User:

    filter_name = 'current_user'

    def __init__(self, app=None):
        if app:
            app.jinja_env.filters[self.filter_name] = self.current_user # todo: find a better way to register these filters

    # todo: remove the use of this , since this forces the import of jinja2 (which is quite time consuming on the tests)
    @pass_context                                            # this is needed to allow the filter to access the context
    def current_user(self, context, field):
        try:
            user_data = g_user_data()
            if user_data:
                return user_data.data.get(field, USER_DATA_WITH_BAD_FIELD)
        except Exception as error:
            #todo: add logging
            pass
        return USER_DATA_WITH_NO_CBR_TOKEN


    # def is_logged_in(self):
    #     return g_user_data() is not None

    # this is the key method (since it is the one that returns the user data
    #todo: need to add this to the g object, or there will be tons of calls to the S3
    def user_data_from_s3(self):
        from flask import request
        from cbr_shared.cbr_sites.CBR__Shared__Constants import COOKIE_NAME__CBR__SESSION_ID__ACTIVE

        # if server_config__cbr_website.aws_disabled():             # now there should always be an S3 available (either on the real S3 or via LocalStack)
        #     return None

        session_id  = request.cookies.get(COOKIE_NAME__CBR__SESSION_ID__ACTIVE)
        if session_id:
            db_session = cbr_session_load.session__from_session_id(session_id=session_id)
            if db_session and db_session.exists():
                return db_session.session_config()

            # admin_token   = None
            # impersonating = False
            # if '|' in cbr_token:                                                            # todo: find a better solution to handle the user and admin token
            #     user_and_admin_tokens = cbr_token.split('|')                                #       this was the solution put in place to work around the limitation of not being able to set multiple cookies in TBC Flask serverless environment
            #     if len(user_and_admin_tokens) == 2:
            #         cbr_token   = user_and_admin_tokens[0]
            #         admin_token = user_and_admin_tokens[1]
            #         impersonating = cbr_token != admin_token
            #     else:
            #         return {}       # something went wrong, return empty data
            # if '__' in cbr_token and len(cbr_token) < 100:                                   # todo: handle better the cases when the cookie is not valid
            #     session_id = cbr_token
            #     db_session = S3_DB__Session(session_id)                                          #  load the session data from the S3
            #     if db_session.exists():
            #         user_data = db_session.session_config().get('data')
            #         if admin_token:
            #             user_data['admin_token'  ] = admin_token
            #             user_data['impersonating'] = impersonating
            #         else:
            #             user_data['admin_token'  ] = ''
            #             user_data['impersonating'] = False
            #         return user_data



# HELPER METHODS for testing
# todo: refactor these methods into a separate file and make them instance methods (i.e. not static methods)

def set_g_user_data(user_name=None, user_groups=None, jti='pytest_session'):
    from flask import g, has_request_context
    from cbr_shared.schemas.data_models.Model__Session__Config import Model__Session__Config

    data = {"cognito:groups": user_groups, 'jti': jti, 'username': user_name}

    user_data = Model__Session__Config(user_name=user_name, data=data)

    if has_request_context():
        g.user_data = user_data
    return user_data

def reset_g_user_data():
    from flask import g, has_request_context
    if has_request_context():               # can't access the g variable when request doesn't exist
        g.user_data = None
        return True
    return False

def g_user_data():
    from flask import g, has_request_context
    if has_request_context() and hasattr(g, 'user_data'):
        return g.user_data

def g_user_data_current_username():
    user_data = g_user_data()
    if user_data:
        return user_data.user_name
    return ''

def client__logged_in(app, user_name = None, user_groups=None):  # todo: this will need fixing
    if not user_name:
        user_name = DEFAULT_USER_NAME
    if not user_groups:
        user_groups = DEFAULT_USER_GROUPS
    client      = app.test_client()
    app.secret_key = 'your_secret_key_for_testing'

    user_data = set_g_user_data(user_name, user_groups)
    app.user_data = user_data                              # todo: find a better way to set this value that is currently being used to sync this data with populate_variable_g
    return client