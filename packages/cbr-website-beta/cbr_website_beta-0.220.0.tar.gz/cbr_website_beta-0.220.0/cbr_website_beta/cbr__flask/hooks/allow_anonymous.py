from flask                                              import request, g, render_template, make_response
from flask                                              import current_app
from cbr_website_beta.cbr__flask.filters.Current_User   import g_user_data, g_user_data_current_username

#@xray_trace("allow_anonymous")
def allow_anonymous():

    auth_data = { "allow"                   : False       ,
                  "redirect_to"             : None        ,
                  "current_user"            : None        ,
                  "static_path"             : False       ,
                  "view_function"           : None        ,
                  "function_allow_anonymous": None        }

    view_function = current_app.view_functions.get(request.endpoint)

    if view_function:
        auth_data["function_allow_anonymous"] = hasattr(view_function, '_allow_anonymous')
        if auth_data["function_allow_anonymous"]:
            auth_data['allow'] = True

    auth_data['current_user'] = g_user_data_current_username()

    if auth_data['current_user']:
        auth_data['allow'] = True

    g.auth_data = auth_data
    if auth_data['allow']:
        return
    else:
        #if cbr_config.login_enabled():                                  # todo: figure out a better way to handle the case when login is disabled
        #return render_template('home/accounts/unauthorized.html')
        response = make_response(render_template('home/accounts/unauthorized.html'))
        response.status_code = 401  # Unauthorized
        return response

# #@xray_trace("admin_only")
# def allow_users():                              # todo: implement logic
#     user_data = Current_User().user_data()
#     return

def admins_only():
    #user_data = Current_User().user_data()
    user_data     = g_user_data()
    view_function = current_app.view_functions.get(request.endpoint)

    if view_function and user_data:
        if hasattr(view_function, '_admins_only'):
            if user_data.securitiy.is_admin_global is False:
                return render_template('home/accounts/unauthorized.html')