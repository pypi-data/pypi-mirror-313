import cbr_athena
import cbr_static
import cbr_content
import cbr_web_components
import cbr_website_beta
from cbr_shared.cbr_sites.CBR__Shared_Objects               import cbr_shared_objects
from cbr_shared.config.Server_Config__CBR_Website           import server_config__cbr_website
from cbr_shared.utils.Version                               import version__cbr_shared
from osbot_aws.aws.sts.STS                                  import STS
from cbr_shared.aws.s3.S3_DB_Base                           import S3_DB_Base
from osbot_markdown.utils.Version                           import version__osbot_markdown
from osbot_utils.utils.Env                                  import get_env, is_env_var_set, env__old_pwd__remove, env__pwd
from cbr_athena.utils.Version                               import version__cbr_athena
from cbr_static.utils.Version                               import Version          as Version__cbr_static
from osbot_aws.utils.Version                                import Version          as Version__osbot_aws
from osbot_utils.utils.Version                              import Version          as Version__osbot_utils
from osbot_fast_api.utils.Version                           import Version as Version__osbot_fast_api, version__osbot_fast_api
from osbot_aws.AWS_Config                                   import aws_config
from osbot_utils.utils.Http                                 import current_host_online
from osbot_utils.utils.Status                               import status_error

from osbot_utils.base_classes.Type_Safe                     import Type_Safe
from cbr_website_beta.utils.Version                         import version, version__cbr_website, version__cbr_content, version__cbr_web_components
from osbot_utils.decorators.methods.cache_on_self           import cache_on_self


class CBR__Site_Info(Type_Safe):

    def data(self):
        try:
            return dict(aws         = self.aws        (),
                        dbs         = self.dbs        (),
                        dates       = self.dates      (),
                        env_vars    = self.env_vars   (),
                        http_events = self.http_events(),
                        paths       = self.paths      (),
                        urls        = self.urls       (),
                        versions    = self.versions   (),
                        server      = self.server     ())
        except Exception as error:
            return status_error(message="error in CBR__Site_Info.data", error=f'{error}')

    def aws(self):
        aws_configured = aws_config.aws_configured() and server_config__cbr_website.aws_enabled()
        if aws_configured:
            caller_identity = STS().caller_identity()
        else:
            caller_identity = 'NA'
        return dict(aws_configured        = aws_configured              ,
                    caller_identity       = caller_identity             ,
                    region                = aws_config.region_name()    ,
                    s3_bucket__s3_db_base = S3_DB_Base().s3_bucket()    ,
                    s3_db_server_requests = self.s3_db_server_requests())

    def dbs(self):
        db_cbr              = cbr_shared_objects.s3_db_cbr            ()
        db_chat_threads     = cbr_shared_objects.s3_db_chat_threads   ()
        db_server_requests  = cbr_shared_objects.s3_db_server_requests()
        db_servers          = cbr_shared_objects.s3_db_servers        ()
        db_sessions         = cbr_shared_objects.db_sessions          ()
        db_users            = cbr_shared_objects.db_users             ()
        return dict(db_cbr             = dict(bucket = db_cbr            .s3_bucket(), local_stack=db_cbr            .using_local_stack(), online=db_cbr            .bucket_exists()),
                    db_chat_threads    = dict(bucket = db_chat_threads   .s3_bucket(), local_stack=db_chat_threads   .using_local_stack(), online=db_chat_threads   .bucket_exists()),
                    db_server_requests = dict(bucket = db_server_requests.s3_bucket(), local_stack=db_server_requests.using_local_stack(), online=db_server_requests.bucket_exists()),
                    db_servers         = dict(bucket = db_servers        .s3_bucket(), local_stack=db_servers        .using_local_stack(), online=db_servers        .bucket_exists()),
                    db_sessions        = dict(bucket = db_sessions       .s3_bucket(), local_stack=db_sessions       .using_local_stack(), online=db_sessions       .bucket_exists()),
                    db_users           = dict(bucket = db_users          .s3_bucket(), local_stack=db_users          .using_local_stack(), online=db_users          .bucket_exists()))


    def dates(self):
        return dict(cbr_site_published_at = get_env('CBR__SITE__PUBLISHED_AT', ''))

    def env_vars(self):
        return dict(status = self.env_vars__status(),
                    values = self.env_vars__values())

    def env_vars__status(self):
        var_names = ['OPEN_AI__API_KEY', 'IP_DATA__API_KEY', 'OPEN_ROUTER_API_KEY',
                     'GROQ_API_KEY', 'COGNITO_USER_POOL_ID', 'TOGETHER_AI_API_KEY',
                     'MISTRAL_API_KEY', 'SAMBANOVA_API_KEY']
        status = {}
        for var_name in var_names:
            status[var_name] = is_env_var_set(var_name)
        return status

    def env_vars__values(self):
        var_names = ['CBR__CONFIG_FILE', 'EXECUTION_ENV', 'PORT', 'S3_DEV__VERSION' , 'AWS_LWA_INVOKE_MODE']
        values = {}
        for var_name in var_names:
            values[var_name] = get_env(var_name)
        return values

    def http_events(self):
        from cbr_website_beta.cbr__fastapi.CBR__Fast_API import cbr_fast_api        # handle circular import
        http_events = cbr_fast_api.http_events

        return dict(fast_api_name       = http_events.fast_api_name       ,
                    max_requests_logged = http_events.max_requests_logged ,
                    trace_calls         = http_events.trace_calls         ,
                    requests_data       = len(http_events.requests_data  ),
                    requests_order      = len(http_events.requests_order ))

    def paths(self):
        return dict(cbr_athena         = env__old_pwd__remove(cbr_athena        .path),
                    cbr_content        = env__old_pwd__remove(cbr_content       .path),
                    cbr_static         = env__old_pwd__remove(cbr_static        .path),
                    cbr_web_components = env__old_pwd__remove(cbr_web_components.path),
                    cbr_website_beta   = env__old_pwd__remove(cbr_website_beta  .path),
                    pwd                = env__pwd()                                   )


    def server(self):
        return dict(aws_configured = aws_config.aws_configured() ,
                    server_online  = current_host_online())

    def s3_db_server_requests(self):
        return cbr_shared_objects.s3_db_server_requests().json()

    def target_athena_url(self):        # todo: refactor out once new setup is stable
        return server_config__cbr_website.athena_path()

    def url_athena__internal(self):                                         # todo: refactor this calculation to a better class
        port        = self.cbr_host__port()
        athena_path = server_config__cbr_website.athena_path()
        if athena_path.startswith('http'):
            return athena_path
        if port:
            return f'http://localhost:{port}{athena_path}'

    def urls(self):
        return dict(url_athena           = self.target_athena_url    (),
                    url_athena__internal = self.url_athena__internal (),
                    url_assets_dist      = server_config__cbr_website.assets_dist(),
                    url_assets_root      = server_config__cbr_website.assets_root())

    @cache_on_self
    def version(self):
        return version

    def versions(self):
        cbr   = dict(cbr_athena         = version__cbr_athena              ,
                     cbr_content        = version__cbr_content             ,
                     cbr_shared         = version__cbr_shared              ,
                     cbr_web_components = version__cbr_web_components      ,
                     cbr_website        = version__cbr_website             ,
                     cbr_static         = Version__cbr_static    ().value() )       # todo create: version__cbr_static
        osbot = dict(osbot_aws          = Version__osbot_aws     ().value() ,       # todo create: version__osbot_aws
                     osbot_fast_api     = version__osbot_fast_api           ,
                     osbot_markdown     = version__osbot_markdown           ,
                     osbot_utils        = Version__osbot_utils   ().value() )       # todo create: version__osbot_utils

        return dict(cbr      = cbr   ,
                    osbot    = osbot )


    # individual values
    def cbr_host__port(self):
        return get_env('PORT')
