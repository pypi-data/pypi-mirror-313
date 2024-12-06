from flask import render_template

from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website
from cbr_website_beta._cbr_shared.dynamo_db.DyDB__CBR_Chat_Threads  import DyDB__CBR_Chat_Threads
from cbr_website_beta._cbr_shared.dynamo_db.DyDB__CBR_Logging       import DyDB__CBR_Logging
from cbr_website_beta._cbr_shared.dynamo_db.DyDB__CBR_Requests      import DyDB__CBR_Requests
from cbr_website_beta._cbr_shared.dynamo_db.DyDB__CBR_User_Sessions import DyDB__CBR_User_Sessions
from cbr_website_beta.apps.dev.views.Logs_Views                     import Logs_Views
from osbot_utils.utils.Misc                                         import date_time_now
from osbot_utils.utils.Str                                          import html_escape

CHAT_THREAD__GPT_RESPONSE__MAX_SIZE = 250

class Odin__Panels__Logs:

    def __init__(self):
        self.logs_view = Logs_Views()

    def exposed_methods(self):                                                  # todo: find a better name for this method and move into base class
        return { 'cbr_chat_threads' : self.cbr_chat_threads ,
                 'cbr_logging'      : self.cbr_logging      ,
                 'cbr_requests'     : self.cbr_requests     ,
                 'cbr_user_sessions': self.cbr_user_sessions,
                 'ip_address'       : self.ip_address       }

    # exposed methods
    def cbr_chat_threads (self, index_name=None, index_value=None, env:str="PROD", hours:int=1):
        kwargs        = dict(index_name=index_name, index_value=index_value, env=env, hours=hours)
        render_kwargs = self.cbr_chat_threads__render_kwargs(**kwargs)
        return render_template(**render_kwargs)

    def cbr_logging (self, index_name=None, index_value=None, env:str="PROD", hours:int=1):
        kwargs        = dict(index_name=index_name, index_value=index_value, env=env, hours=hours)
        render_kwargs = self.cbr_logging__render_kwargs(**kwargs)
        return render_template(**render_kwargs)

    def cbr_requests(self, index_name=None, index_value=None, env:str="PROD", hours:int=1):
        kwargs = dict(index_name=index_name, index_value=index_value, env=env, hours=hours)
        return render_template(**self.cbr_requests__render_kwargs(**kwargs))

    def cbr_user_sessions (self, index_name=None, index_value=None, env:str="PROD", hours:int=1):
        kwargs        = dict(index_name=index_name, index_value=index_value, env=env, hours=hours)
        render_kwargs = self.cbr_user_sessions__render_kwargs(**kwargs)
        return render_template(**render_kwargs)

    def ip_address(self, ip_address: str='NA', env:str="PROD", hours:int=1):
        kwargs = dict(ip_address=ip_address, env=env, hours=hours)
        return render_template(**self.ip_address__render_kwargs(**kwargs))

    # internal methods

    def cbr_chat_threads__render_kwargs(self, index_name=None, index_value=None, env=None, hours=5):
        env                   = env or server_config__cbr_website.env()
        dydb_cbr_chat_threads = DyDB__CBR_Chat_Threads(env=env)
        fields                = ['id', 'session_id', 'when', 'user_prompt', 'gpt_response', 'source', 'chat_thread_id', 'date']
        if not index_name:
            index_name = 'date'
            index_value = date_time_now(date_time_format='%Y-%m-%d')

        requests = self.logs_view.api_log_data(dydb=dydb_cbr_chat_threads, index_name=index_name, index_value=index_value,
                                               hours=hours, env=env, fields=fields)

        for request in requests:
            gpt_response = request.get('gpt_response') or ''
            if len(gpt_response) > CHAT_THREAD__GPT_RESPONSE__MAX_SIZE:
                request['gpt_response'] = gpt_response[:CHAT_THREAD__GPT_RESPONSE__MAX_SIZE] + f' ... (size {len(gpt_response)})'

            user_prompt = request.get('user_prompt') or ''
            if len(user_prompt) > CHAT_THREAD__GPT_RESPONSE__MAX_SIZE:
                request['user_prompt'] = user_prompt[:CHAT_THREAD__GPT_RESPONSE__MAX_SIZE] + f' ... (size {len(user_prompt)})'

            request['gpt_response'] = html_escape(request.get('gpt_response') or '')            # todo: find a better way to handle this, since there doesn't seem to be a native jquery.dataTables way to do this
            request['user_prompt' ] = html_escape(request.get('user_prompt' ) or '')

            session_id = request.get('session_id') or ''
            if len(session_id.split('__')) ==2 :
                user_name = session_id.split('__')[0]
                request['session_id'] = user_name
        metadata = dict(fields=fields, hours=hours, env=env)
        render_kwargs = dict(title                 = 'Chat Threads'                     ,
                             requests              = requests                           ,
                             metadata              = metadata                           ,
                             method_name           = 'cbr_chat_threads'                 ,
                             template_name_or_list = "dev/odin/panels/cbr_requests.html")
        return render_kwargs


    def cbr_logging__render_kwargs(self, index_name=None, index_value=None, env=None, hours=5):
        env               = env or server_config__cbr_website.env()
        dydb_cbr_requests = DyDB__CBR_Logging(env=env)
        load_fields       = [ 'id'         ,
                              'source'     , 'when'        , 'message'    , 'level'      ,
                              'topic'      , 'user_id'     , 'extra_data' , 'env'        ]
        view_fields       = [ 'id'         ,
                              'source'     , 'when'        , 'message'    ,
                              'level'      , 'topic'       , 'env'        ]

        if not index_name:
            index_name = 'date'
            index_value = date_time_now(date_time_format='%Y-%m-%d')
        requests = self.logs_view.api_log_data(dydb=dydb_cbr_requests, index_name=index_name, index_value=index_value, hours=hours, env=env,fields=load_fields)

        self.filter_logging_requests(requests=requests)
        metadata = dict(fields=view_fields, hours=hours, env=env)
        render_kwargs = dict(title                 = 'Odin - Logs'  ,
                             requests              = requests       ,
                             metadata              = metadata       ,
                             method_name           = 'cbr_logging'  ,
                             template_name_or_list = "dev/odin/panels/cbr_requests.html")

        return render_kwargs

    def filter_logging_requests(self, requests):
        for request in requests:
            extra_data = request.get('extra_data', {})
            message    = request.get('message'   , '')
            if message == 'prompt_request':
                user_prompt  = extra_data.get('user_prompt' , '')
                histories    = extra_data.get('prompt_data' , {}).get('histories') or []
                gtp_response = extra_data.get('gtp_response', '')
                if len(user_prompt)  > 300:
                    user_prompt = user_prompt[:300] + f'<i> ... (hidden={len(user_prompt)-300})</i>'
                if len(gtp_response) > 500:
                    gtp_response = gtp_response[:500] + f'<i> ... (hidden={len(gtp_response)-500})</i>'
                request['user_prompt' ] =user_prompt
                request['gtp_response'] = gtp_response
                request['history'     ] = len(histories)
            else:
                request['user_prompt' ] = ''
                request['gtp_response'] = ''
                request['history'     ] = 0


    def cbr_requests__render_kwargs(self, index_name=None, index_value=None, env=None, hours=1):
        env               = env or server_config__cbr_website.env()
        dydb_cbr_requests = DyDB__CBR_Requests(env=env)
        fields   = ['id',
                    'source'     , 'when'       , 'user_name'  , 'path'       , 'duration'   ,'city', 'country' ,
                    'ip_address' ,'ip_info'     , 'session_id' , 'level'      ,'referer',
                    'status_code', 'env'        ]
                    # 'date',  'user_role' ,'method'     ,
                    # 'host',
                    #'req_id',
                    #, 'user_status'

        ignore = dict(path='/dev/dev-panel')

        if not index_name:
            index_name = 'date'
            index_value = date_time_now(date_time_format='%Y-%m-%d')
        requests = self.logs_view.api_log_data(dydb=dydb_cbr_requests, index_name=index_name, index_value=index_value, hours=hours, env=env, fields=fields, ignore=ignore)

        metadata = dict(fields=fields, hours=hours, env=env)
        render_kwargs = dict(title                 = 'Web/APIs Requests',
                             requests              = requests           ,
                             metadata              = metadata           ,
                             method_name           = 'cbr_requests'     ,
                             template_name_or_list = "dev/odin/panels/cbr_requests.html" )

        return render_kwargs

    def cbr_user_sessions__render_kwargs(self, index_name=None, index_value=None, env=None, hours=5):
        env                    = env or server_config__cbr_website.env()
        dydb_cbr_user_sessions = DyDB__CBR_User_Sessions(env=env)
        fields                 = ['id', 'user_name', 'display_name', 'session_id', 'source', 'date']
        if not index_name:
            index_name = 'date'
            index_value = date_time_now(date_time_format='%Y-%m-%d')

        requests = self.logs_view.api_log_data(dydb=dydb_cbr_user_sessions, index_name=index_name, index_value=index_value,
                                               hours=hours, env=env, fields=fields)

        metadata = dict(fields=fields, hours=hours, env=env)
        render_kwargs = dict(title                 = 'User Sessions'                    ,
                             requests              = requests                           ,
                             metadata              = metadata                           ,
                             method_name           = 'cbr_user_sessions'                ,
                             template_name_or_list = "dev/odin/panels/cbr_requests.html")
        return render_kwargs

    def ip_address__render_kwargs(self, ip_address, env, hours):
        ip_address_data = self.logs_view.get_ip_address_data(ip_address)
        render_kwargs = dict(env                   = env              ,
                             ip_address            = ip_address       ,
                             ip_address_data       = ip_address_data  ,
                             hours                 = hours            ,
                             template_name_or_list ="dev/odin/panels/ip_address.html")
        return render_kwargs
