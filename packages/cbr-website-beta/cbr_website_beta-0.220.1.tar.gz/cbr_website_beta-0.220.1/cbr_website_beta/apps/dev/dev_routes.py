from cbr_website_beta.apps.dev                                  import blueprint
from cbr_website_beta.cbr__flask.decorators.allow_annonymous    import admin_only, allow_anonymous


EXPECTED_METHODS_DEV = [ 'dev_blueprint.all_chat_threads'              ,
                         'dev_blueprint.api_odin_update_s3_data'       ,
                         'dev_blueprint.dashboard_widget'              ,
                         'dev_blueprint.dashboard_widgets'             ,
                         'dev_blueprint.dev_client_details'            ,
                         'dev_blueprint.dev_current_sessions'          ,
                         'dev_blueprint.dev_current_user'              ,
                         'dev_blueprint.dev_current_users'             ,
                         'dev_blueprint.dev_debug_views'               ,
                         'dev_blueprint.dev_logs_streams'              ,
                         'dev_blueprint.dev_real_time_code_editor'     ,
                         'dev_blueprint.dev_render_panel'              ,
                         'dev_blueprint.dev_request_details'           ,
                         'dev_blueprint.dev_root'                      ,
                         'dev_blueprint.dev_view'                      ,
                         'dev_blueprint.lambda_shell'                  ,
                         'dev_blueprint.logs_chat_threads'             ,
                         'dev_blueprint.logs_ip_address'               ,
                         'dev_blueprint.logs_odin'                     ,
                         'dev_blueprint.logs_user_sessions'            ,
                         'dev_blueprint.logs_web'                      ,
                         'dev_blueprint.odin_chat'                     ]

EXPECTED_ROUTES__DEV = [ '/dev/'                                       ,
                         '/dev/all-chat-threads'                       ,
                         '/dev/api/odin/update-s3-data'                ,
                         '/dev/client-details'                         ,
                         '/dev/current-sessions'                       ,
                         '/dev/current-user/<user_id>'                 ,
                         '/dev/current-users'                          ,
                         '/dev/dashboard/widget/<widget_name>/<start>' ,
                         '/dev/dashboard/widgets'                      ,
                         '/dev/debug-views'                            ,
                         '/dev/dev-panel'                              ,
                         '/dev/lambda-shell'                           ,
                         '/dev/logs-chat-threads'                      ,
                         '/dev/logs-web'                               ,
                         '/dev/logs-odin'                              ,
                         '/dev/logs-sessions'                          ,
                         '/dev/logs/ip-address'                        ,
                         '/dev/odin/odin-chat'                         ,
                         '/dev/real-time/streams'                      ,
                         '/dev/real-time/code-editor'                  ,
                         '/dev/request-details'                        ,
                         '/dev/view/<class_name>/<method_name>'        ]

EXPECTED_DEV_MENU = {   "All Chat Threads" : "/web/dev/all-chat-threads"     ,
                        "Client Details"   : "/web/dev/client-details"       ,
                        'Code Editor'      : '/web/dev/real-time/code-editor',
                        "Current Sessions" : "/web/dev/current-sessions"     ,
                        "Current Users"    : "/web/dev/current-users"        ,
                        "Dev"              : "/web/dev/"                     ,
                        'Debug Views'      : '/web/dev/debug-views'          ,
                        'Ip Address'       : '/web/dev/logs/ip-address'      ,
                        'Logs Chat Threads': '/web/dev/logs-chat-threads'    ,
                        'Logs Odin'        : '/web/dev/logs-odin'            ,
                        'Logs Sessions'    : '/web/dev/logs-sessions'        ,
                        'Logs Web'         : '/web/dev/logs-web'             ,
                        'Odin Chat'        : '/web/dev/odin/odin-chat'       ,
                        "Request Details"  : "/web/dev/request-details"      ,
                        'Widgets'          : '/web/dev/dashboard/widgets'    ,
                        'Streams'          : '/web/dev/real-time/streams'    }

@blueprint.route('/', strict_slashes=False)
@admin_only
def dev_root():
    from flask import render_template
    from cbr_website_beta.apps.dev.view_data import useful_links, for_danny, prompt_uis, user_management

    #bot_athena  = Athena_Rest_API()
    #git_repo_status = bot_athena.git_repo_status()
    return render_template('dev/index.html',
                           useful_links    = useful_links    ,
                           for_danny       = for_danny       ,
                           prompt_uis      = prompt_uis      ,
                           user_management = user_management )
                           #github_repos=github_repos,

                           #git_repo_status= git_repo_status)

@blueprint.route('/all-chat-threads')
@admin_only
def all_chat_threads():
    from cbr_website_beta.apps.dev.views.Render_View import Render_View

    class_name  = 'odin_chat_threads'
    method_name = 'all_chat_threads'
    return Render_View().render_view(class_name, method_name)


@blueprint.route('/client-details')
@admin_only
def dev_client_details():
    from cbr_website_beta.apps.dev.views.Debug_Views import Debug_Views

    return Debug_Views().client_details()

@blueprint.route('/dashboard/widgets')
@admin_only
def dashboard_widgets():
    from cbr_website_beta.apps.dev.views.Render_View import Render_View

    class_name = 'odin_dashboard_widgets'
    method_name = 'dashboard_metrics'
    return Render_View().render_view(class_name, method_name)

@blueprint.route('/dashboard/widget/<widget_name>/<start>')
@admin_only
def dashboard_widget(widget_name, start):
    import io
    from flask import send_file
    from cbr_website_beta.apps.dev.Render_Panels import Render_Panels


    render_panels = Render_Panels()
    class_name    = 'odin_dashboard_widgets'
    method_name   = 'widget_screenshot'
    method_kwargs = dict(widget_name = widget_name,
                         start      = f"-PT{start}H"             ,
                         end        = "P0D"               )
    render_kwargs = dict(class_name  = class_name  ,method_name = method_name, **method_kwargs)
    image_bytes   = render_panels.render_panel(**render_kwargs)

    result_io = io.BytesIO(image_bytes)
    result_io.seek(0)  # Go to the beginning of the file-like object

    # Return the file-like object as a PNG image
    return send_file(result_io, mimetype='image/png', as_attachment=False)


@blueprint.route('/logs-chat-threads')
@admin_only
def logs_chat_threads():
    from flask import request
    from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website
    from cbr_website_beta.apps.dev.views.Render_View import Render_View


    current_env   = server_config__cbr_website.env()
    hours         = request.args.get('hours'    , default=1          , type=int)
    env           = request.args.get('partition', default=current_env, type=str)
    class_name    = 'odin_logs'
    method_name   = 'cbr_chat_threads'
    method_kwargs = dict(hours=hours, env=env)
    return Render_View().render_view(class_name, method_name, **method_kwargs)

@blueprint.route('/logs-web')
@admin_only
def logs_web():
    from flask import request
    from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website
    from cbr_website_beta.apps.dev.views.Render_View import Render_View


    current_env   = server_config__cbr_website.env()
    hours         = request.args.get('hours'    , default=1          , type=int)
    env           = request.args.get('partition', default=current_env, type=str)
    class_name    = 'odin_logs'
    method_name   = 'cbr_requests'
    method_kwargs = dict(hours=hours, env=env)
    return Render_View().render_view(class_name, method_name, **method_kwargs)

@blueprint.route('/logs-odin')
@admin_only
def logs_odin():
    from flask import request
    from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website
    from cbr_website_beta.apps.dev.views.Render_View import Render_View

    current_env   = server_config__cbr_website.env()
    hours         = request.args.get('hours'    , default=1          , type=int)
    env           = request.args.get('partition', default=current_env, type=str)
    class_name    = 'odin_logs'
    method_name   = 'cbr_logging'
    method_kwargs = dict(hours=hours, env=env)
    return Render_View().render_view(class_name, method_name, **method_kwargs)

@blueprint.route('/logs-sessions')
@admin_only
def logs_user_sessions():
    from flask import request
    from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website
    from cbr_website_beta.apps.dev.views.Render_View import Render_View

    current_env   = server_config__cbr_website.env()
    hours         = request.args.get('hours'    , default=1          , type=int)
    env           = request.args.get('partition', default=current_env, type=str)
    class_name    = 'odin_logs'
    method_name   = 'cbr_user_sessions'
    method_kwargs = dict(hours=hours, env=env)
    return Render_View().render_view(class_name, method_name, **method_kwargs)

@blueprint.route('/logs/ip-address')
@admin_only
def logs_ip_address():
    from flask import request
    from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website
    from cbr_website_beta.apps.dev.views.Render_View import Render_View

    current_env   = server_config__cbr_website.env()
    hours         = request.args.get('hours'     , default=5          , type=int)
    env           = request.args.get('env'       , default=current_env, type=str)
    ip_address    = request.args.get('ip_address', default='NA'       , type=str)
    class_name    = 'odin_logs'
    method_name   = 'ip_address'
    method_kwargs = dict(hours=hours, env=env, ip_address=ip_address)
    return Render_View().render_view(class_name, method_name, **method_kwargs)

@blueprint.route('/odin/odin-chat')
@admin_only
def odin_chat():
    from cbr_website_beta.apps.dev.views.Render_View import Render_View

    class_name  = 'odin_real_time'
    method_name = 'chat_prompt'
    return Render_View().render_view(class_name, method_name)


@blueprint.route('/real-time/streams')
@admin_only
def dev_logs_streams():
    from cbr_website_beta.apps.dev.views.Render_View import Render_View

    class_name  = 'odin_real_time'
    method_name = 'log_streams'
    return Render_View().render_view(class_name, method_name)

@blueprint.route('/real-time/code-editor')
@admin_only
def dev_real_time_code_editor():
    from cbr_website_beta.apps.dev.views.Render_View import Render_View

    class_name  = 'odin_real_time'
    method_name = 'code_editor'
    return Render_View().render_view(class_name, method_name)

@blueprint.route('/request-details')
@admin_only
def dev_request_details():
    from cbr_website_beta.apps.dev.views.Debug_Views import Debug_Views
    return Debug_Views().request_details()

# @blueprint.route('/request-logs')
# @admin_only
# def dev_request_logs():
#     return Logs_Views().request_logs()

@blueprint.route('/current-sessions')
@admin_only
def dev_current_sessions():
    from cbr_website_beta.apps.dev.views.Render_View import Render_View

    class_name = 'odin_session_management'
    method_name = 'current_sessions'
    return Render_View().render_view(class_name, method_name)

    #return Sessions_Views().current_sessions()

@blueprint.route('/current-user/<user_id>')
@admin_only
def dev_current_user(user_id:str=None):
    from cbr_website_beta.apps.dev.views.Users_Views import Users_Views

    return Users_Views().current_user(user_id)

@blueprint.route('/current-users')
@admin_only
def dev_current_users():
    from cbr_website_beta.apps.dev.views.Render_View import Render_View

    class_name  = 'odin_session_management'                                      # todo: find a better to map these Render_View methods
    method_name = 'current_users'
    return Render_View().render_view(class_name, method_name)
    #return Users_Views().current_users()


@blueprint.route('/dev-panel', methods=['POST'])
@admin_only
def dev_render_panel():                                 # todo refactor this from this class into the Render_Panels class
    from flask import request, jsonify
    from cbr_website_beta.apps.dev.Render_Panels import Render_Panels

    if request.is_json:
        try:
            data          = request.get_json()
            class_name    = data.get('class_name')
            method_name   = data.get('method_name')
            method_kwargs = data.get('method_kwargs', {})

            if not class_name or not method_name:
                return jsonify({'status': 'error', 'message': 'class_name and method_name are required'}), 400

            result = Render_Panels().render_panel(class_name, method_name, **method_kwargs)
            return jsonify(result)
        except Exception as error:
            return jsonify({'status': 'error', 'message': f'Error: {error}'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Request must be JSON'}), 400

@blueprint.route('/view/<class_name>/<method_name>')
@admin_only
def dev_view(class_name, method_name):
    from cbr_website_beta.apps.dev.views.Render_View import Render_View

    return Render_View().render_view(class_name, method_name)


# @blueprint.route('/odin-actions')
# @admin_only
# def dev_odin_actions():
#     return Views__Dev__Odin().odin_actions()

# @blueprint.route('/tree-view')
# @admin_only
# def dev_tree_view():
#     return view__tree_view()

# @blueprint.route('/s3-explorer')
# @admin_only
# def dev_s3_explorer():
#     class_name  = 'odin_s3_explorer'
#     method_name = 's3_browser'
#     return Render_View().render_view(class_name, method_name)

@blueprint.route('/debug-views')
@admin_only
def dev_debug_views():
    from cbr_website_beta.apps.dev.views.Render_View import Render_View

    class_name    = 'odin_debug'
    method_name   = 'debug_views'
    method_kwargs = dict()
    return Render_View().debug_views(class_name, method_name, ** method_kwargs)
    #return view__tree_view()


@blueprint.route('/lambda-shell', methods=['POST'])
@allow_anonymous
def lambda_shell():
    from osbot_aws.apis.shell.Lambda_Shell import Lambda_Shell, SHELL_VAR
    from flask import request
    event = request.get_json()
    if event:
        shell_server = Lambda_Shell(event.get(SHELL_VAR))
        if shell_server.valid_shell_request():
            return shell_server.invoke()
    return '...this is not the lambda shell you are looking for ....'