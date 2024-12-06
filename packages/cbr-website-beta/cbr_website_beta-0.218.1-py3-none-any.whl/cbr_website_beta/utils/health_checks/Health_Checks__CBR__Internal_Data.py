from cbr_shared.config.Server_Config__CBR_Website   import server_config__cbr_website
from osbot_utils.utils.Misc                         import list_set

RESULT_OK__aws_disabled               = 'aws access is disabled'
RESULT_OK__cbr_config_data            = 'CBR__Config had the expected data'
RESULT_OK__cbr_check_session_creation = 'Temp CBR session created and deleted'

EXCEPTION__cbr_config_data            = 'CBR__Config did NOT had the expected data'

class Health_Checks__CBR__Internal_Data:

    @staticmethod
    def cbr_config_data():
        if list_set(server_config__cbr_website.cbr_config().json()) == [ 'cbr_dev', 'cbr_website']:
            return RESULT_OK__cbr_config_data
        raise Exception(EXCEPTION__cbr_config_data)

    @staticmethod
    def cbr_check_session_creation():
        if server_config__cbr_website.aws_disabled():
            return RESULT_OK__aws_disabled
        from cbr_website_beta.aws.cognito.Cognito_Auth_Flow import Cognito_Auth_Flow
        cognito_auth_flow = Cognito_Auth_Flow()
        user_info = { 'auth_time'     : 1707694293                                                   ,
                      'client_id'     : '11112223333444555'                                          ,
                      'cognito:groups': ['AAAAAA_Group']                                             ,
                      'event_id'      : 'fbe19987-aaaa-aaaa-aaaa-73d0eff0985e'                       ,
                      'exp'           : 1707780693                                                   ,
                      'iat'           : 1707694293                                                   ,
                      'iss'           : 'https://cognito-idp.eu-west-2.amazonaws.com/eu-west-2_BBBBB',
                      'jti'           : '2fca243c-cccc-bbbb-aaaa-996f35942d59'                       ,
                      'origin_jti'    : '7fe352e1-aaaa-bbbb-cccc-2718eae9ebc5'                       ,
                      'scope'         : 'phone openid email'                                         ,
                      'sub'           : '48fe1709-aaaa-aaaa-aaaa-6526f1537537'                       ,
                      'token_use'     : 'access'                                                     ,
                      'username'      : 'an_temp_user_xyz'                                           ,
                      'version'       : 2                                                            }
        metadata  = {'source': 'pytest'}
        db_session = cognito_auth_flow.create_session(user_info, metadata)
        assert db_session.exists() is True
        assert db_session.delete() is True
        return RESULT_OK__cbr_check_session_creation