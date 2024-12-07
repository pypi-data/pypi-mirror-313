#LOG_STATIC_FILES = True
def env_vars_to_log():
    from os import environ

    env_vars = {'lambda': {"memory_size"        : environ.get('AWS_LAMBDA_FUNCTION_MEMORY_SIZE' ,''),
                           "function_name"      : environ.get('AWS_LAMBDA_FUNCTION_NAME'        ,''),
                           "function_version"   : environ.get('AWS_LAMBDA_FUNCTION_VERSION'     ,''),
                           "aws_region"         : environ.get('AWS_REGION'                      ,''),
                           "execution_env"      : environ.get('EXECUTION_ENV'                   ,''),
                           "amzn_trace_id"      : environ.get('_X_AMZN_TRACE_ID'                ,''),
                           "runtime"            : environ.get('AWS_EXECUTION_ENV'               ,'')}}
    return env_vars

#@xray_trace("register_logging")
def register_logging(app):
    import sys

    if 'pytest' in sys.modules:             # disable for unit tests
       return

    #dydb_cbr_requests = DyDB__CBR_Requests()

    #todo: move this logic to the post_request so that we can capture the elapsed time
    # @xray_trace("before_request - pre_request_logging")

    @app.after_request
    def post_request_logging(response):
        from flask import request, g
        from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website

        if server_config__cbr_website.req_traces_enabled():
            if hasattr(request, 'trace_call'):
                request.trace_call.stop()                               # stop tracing session
                g.request_data.add_traces(request.trace_call)           # capture the traces in the FastAPI request_data object

                # if response.headers.get('Content-Type') != 'application/json':
                #     with Stdout() as stdout:
                #         request.trace_call.print()
                #     trace_data = ansi_to_text(stdout.value())
                #     extra_content = f'<div style="margin-left:300px"><pre>{trace_data}</pre> </div>'
                #     response = make_response(response.get_data() + extra_content.encode('utf-8'), response.status_code, dict(response.headers))
        return response


    @app.before_request
    #@cbr_trace_calls(include=['*'])
    def pre_request_logging():
        from flask                                                      import request, g
        from cbr_shared.config.Server_Config__CBR_Website               import server_config__cbr_website
        from cbr_website_beta                                           import global_vars
        from cbr_website_beta._cbr_shared.dynamo_db.DyDB__CBR_Requests  import dydb_cbr_requests
        from osbot_utils.helpers.trace.Trace_Call                       import Trace_Call
        from osbot_utils.helpers.trace.Trace_Call__Config               import Trace_Call__Config
        from osbot_utils.utils.Dev                                      import pprint

        # capture the fastapi request object
        g.request_id = request.headers.get('Fast-Api-Request-Id')
        g.request_data = global_vars.fast_api_http_events.requests_data.get(g.request_id)

        if server_config__cbr_website.req_traces_enabled():
            # todo: re-enabled back this trace functionality
            #print(f"\n\n******* starting trace for : {request.path} ******")
            trace_call_config                           = Trace_Call__Config()
            trace_call_config.trace_capture_start_with  = ["cbr", "osbot"]
            trace_call_config.show_method_class         = True
            #trace_call_config.show_parent_info = True
            trace_call_config.duration(padding=110, bigger_than=0.001)
            trace_call = Trace_Call(config=trace_call_config)
            trace_call.start()

            request.trace_call = trace_call



        if dydb_cbr_requests.disabled is True:
            return

        if server_config__cbr_website.s3_log_requests() is False:
            return

        try:
            cbr_request = create_logging__cbr_request()

            document    = cbr_request.json()
            document    = dydb_cbr_requests.add_document(document)
            document_id = document.get('document').get('id')
            print(f'>>>> added request as {document_id} to {dydb_cbr_requests.table_name}')
        except Exception as e:
            pprint(e)               # todo add custom error handler which will send the errors to DyDB


        # cbr_request.status_code= ???   #todo add this to the response section

        #todo: remove the legacy code below
        # timestamp    = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')  # ISO 8601 format
        # request_data = {"env"            : g.execution_env                      ,
        #                 "user_name"      : g.user_name                          ,
        #                 "user_groups"    : g.user_groups                        ,
        #                 #"remote_addr"   : request.remote_addr                  ,
        #                 "ip_address"     : g.ip_address                         ,
        #                 #"timestamp"     : datetime.utcnow().strftime("%d/%b/%Y %H:%M:%S"),
        #                 #"time"           : datetime.utcnow().strftime("%H:%M:%S"),
        #                 #"method"        : request.method                        ,
        #                 "path"           : request.path                          ,
        #                 "latitude"       : g.latitude                            ,
        #                 "longitude"      : g.longitude                           ,
        #                 #"scheme"        : request.scheme.upper()                ,
        #                 #"protocol"      : request.environ.get("SERVER_PROTOCOL").split("/")[-1],
        #                 }


        # todo: figure out why this takes so long to run in AWS (between 20ms to 70ms)


        #with Duration(f'cloud_watch_logs.send_log'):
        #cloud_watch_logs.send_log(log_msg)
        #with Duration(f'DyDB__Timeseries.add_document'):
        #dydb_timeseries  .add_document(log_msg, partition=g.execution_env)
        #dydb_web_requests.add_document(log_msg, partition=g.execution_env)

    # @app.after_request
    # def post_request_logging(response):
    #     print('in post requests')
    #     return response
    #     if hasattr(request, "_start_time"):
    #         request_latency = datetime.utcnow() - request._start_time
    #         request_latency_seconds = request_latency.total_seconds()
    #     else:
    #         request_latency_seconds = 0
    #
    #     response_data = { "timestamp"      : datetime.utcnow().strftime("%d/%b/%Y %H:%M:%S"),
    #                       "status_code"    : response.status_code                           ,
    #                       "latency_seconds": request_latency_seconds                        }
    #     log_msg = {"source": "flask_logging" ,
    #                "type"  : 'response_data' ,
    #                "data"  : response_data  }
    #
    #     #logger.info(log_msg)
    #     cloud_watch_logs.send_log(log_msg)
    #
    #     return response

def create_logging__cbr_request():
    from flask                                            import request, g
    from datetime                                         import datetime
    from osbot_utils.utils.Misc                           import date_time_now
    from cbr_website_beta._cbr_shared.schemas.CBR_Request import CBR_Request

    cbr_request = CBR_Request()

    try:
        request._start_time = datetime.utcnow()

        if '/llms-ui' in request.path:
            return
        headers = {key: value for key, value in request.headers.items()}
        country = headers.get('Cloudfront-Viewer-Country-Name')  # todo refactor to a country and city method
        if not country:  # if 'Cloudfront-Viewer-Country-Name' did not had a value
            country = headers.get('Cloudfront-Viewer-Country', 'NA')  # try Cloudfront-Viewer-Country

        if hasattr(g, 'user_name'):
            cbr_request.user = g.user_name or 'NA'
            #cbr_request.user_role = f'{g.user_groups}' or 'NA'  # todo , fix naming convention
            cbr_request.ip_address = g.ip_address or 'NA'
        cbr_request.path = request.path or 'NA'
        cbr_request.date = date_time_now(date_time_format='%Y-%m-%d')
        cbr_request.level = "DEBUG"
        cbr_request.method = request.method or 'NA'
        cbr_request.referer = request.referrer or 'NA'
        cbr_request.headers = headers
        cbr_request.environ = env_vars_to_log()
        cbr_request.city = headers.get('Cloudfront-Viewer-City', 'NA')
        cbr_request.country = country
        cbr_request.source = 'CBR Website'
    except Exception as error:
        cbr_request.error = str(error)
        cbr_request.message = 'Error creating CBR Request (in create_logging__cbr_request)'
    return cbr_request

