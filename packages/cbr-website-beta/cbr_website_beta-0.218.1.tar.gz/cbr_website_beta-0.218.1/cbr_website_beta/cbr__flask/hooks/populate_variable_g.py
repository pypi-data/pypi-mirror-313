import os
import uuid
from flask                                              import g, request, current_app
from osbot_utils.utils.Misc                             import date_time_now
from cbr_website_beta.cbr__flask.filters.Current_User   import Current_User

log_req_count = 0
log_list_all  = []
app_id        = uuid.uuid4().hex[:6]    # unique id of server or lambda function
app_started   = date_time_now()


#from osbot_utils.helpers.trace.Trace_Call import Trace_Call
#from osbot_utils.helpers.trace.Trace_Call__Config import Trace_Call__Config
# def request_tracer():
#     if hasattr(g, 'request_tracer'):
#         return g.request_tracer
#
#     trace_config                          = Trace_Call__Config()
#     trace_config.title                    = "Traced Request calls"
#     trace_config.trace_ignore_start_with  = ['osbot_utils.utils.Json'] #werkzeug.local','werkzeug.datastructures', 'typing', 'os']
#     trace_config.trace_capture_start_with = ['cbr_website_beta', 'flask']
#     trace_call                            = Trace_Call(config=trace_config)
#
#     #request_tracer.trace_capture_all = True
#     #request_tracer.trace_capture_start_with.append('osbot')
#
#     return trace_call

#@xray_trace("populate_variable_g")


def populate_variable_g():

    app = current_app

    if hasattr(app, 'user_data'):                                       # todo: find a better way to set this value, since this is set via Current_User.client__logged_in
        g.user_data = app.user_data

    if hasattr(g, 'user_data') is False:
        g.user_data = None

    if hasattr(g, 'user_data') is False or not g.user_data :                                # only set g.user_data if it hasn't been set already (for example some tests willl set this value)
        g.user_data     = Current_User().user_data_from_s3()
    if g.user_data:
        #g.user_groups   = g.user_data.data.get('cognito:groups') or ''
        #g.user_name     = g.user_data.data.get('username'      )    or ''
        g.user_name  = g.user_data.user_name
    else:
        g.user_name  = ''
    #g.trace_call = request_tracer()
    g.data_loaded = 'OK'
    g.execution_env = os.environ.get('EXECUTION_ENV', 'LOCAL')

    g.log_list      = []
    g.log_list_all  = log_list_all
    g.log_req_count = 0
    g.app_id        = app_id
    g.app_started   = app_started
    g.host          = request.headers.get('Host'                       ) or ''
    g.latitude      = request.headers.get('Cloudfront-Viewer-Latitude' ) or ''
    g.longitude     = request.headers.get('Cloudfront-Viewer-Longitude') or ''
    g.ip_address    = request.headers.get('X-Forwarded-For'            ) or ''
    g.aws_trace_id  = request.headers.get('X-Amzn-Trace-Id'            ) or ''
