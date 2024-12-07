import os

from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website
from cbr_website_beta.utils.Version               import version

class Config(object):
    ENV                       = server_config__cbr_website.env()
    #ASSETS_ROOT               = os.getenv('ASSETS_ROOT', server_config__cbr_website.assets_root())
    STATIC_SERVER             = os.getenv('STATIC_SERVER'            , 'https://static.dev.aws.cyber-boardroom.com/'                         )
    CBR__SITE__WEB_COMPONENTS = os.getenv('CBR__SITE__WEB_COMPONENTS', 'https://static.dev.aws.cyber-boardroom.com/cbr-web-components/latest')
    ASSETS_ROOT               = os.getenv('CBR__SITE__STATIC'        , 'https://static.dev.aws.cyber-boardroom.com/cbr-static/latest/assets' )
    GTA_ENABLED               = server_config__cbr_website.gta_enabled()
    VERSION                   = version
    ASSETS_DIST               = server_config__cbr_website.assets_dist()
    CBR_LOGO                  = server_config__cbr_website.cbr_logo()

    
class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY  = server_config__cbr_website.session_cookie_httponly  ()
    REMEMBER_COOKIE_HTTPONLY = server_config__cbr_website.remember_cookie_httponly ()
    REMEMBER_COOKIE_DURATION = server_config__cbr_website.remember_cookie_duration ()
    LOGIN_ENABLED            = server_config__cbr_website.login_enabled            ()

class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
