from cbr_website_beta.cbr__flask.decorators.allow_annonymous    import allow_anonymous
from cbr_website_beta.apps.user                                 import blueprint
from cbr_website_beta.aws.cognito.Cognito_Auth_Flow             import Cognito_Auth_Flow

LOCAL_DEV_SERVER     = 'http://localhost:5000/'
COGNITO_PROJECT      = 'the-cbr-beta'
COGNITO_REGION       = 'eu-west-2'
COGNITO_CLIENT_ID    = '5ij6l5kdho4umoks5rjfh9cbid'
COGNITO_SIGN_IN      = f'https://{COGNITO_PROJECT}.auth.{COGNITO_REGION}.amazoncognito.com/login?client_id={COGNITO_CLIENT_ID}&response_type=code&scope=email+openid+phone&'
COGNITO_SIGN_OUT     = f'https://{COGNITO_PROJECT}.auth.{COGNITO_REGION}.amazoncognito.com/logout?client_id={COGNITO_CLIENT_ID}&response_type=code&scope=email+openid+phone&'
EXPECTED_USER__HOME  = [ '/admin/impersonate_user/<user_token>' ,
                         '/admin/restore_admin_user'            ,
                         '/login'                               ,
                         '/logout'                              ,
                         '/sign-in'                             ,
                         '/sign-out'                            ,
                         '/unauthorized'                        ,
                         '/user/profile'                        ]


@blueprint.route('/login')
@allow_anonymous
def login():
    from flask import redirect
    from cbr_website_beta.cbr__flask.utils.current_server import current_server

    url = COGNITO_SIGN_IN + f"redirect_uri={current_server()}web/sign-in"
    return redirect(url)

@blueprint.route('/sign-in')
@allow_anonymous
def sign_in():                                                      # todo: refactor to use new user-session REST APIs
    from flask import request, make_response, render_template
    from cbr_shared.cbr_sites.CBR__Shared__Constants    import COOKIE_NAME__CBR__SESSION_ID__USER, COOKIE_NAME__CBR__SESSION_ID__ACTIVE

    sign_in_code      = request.args.get('code')                    # todo: refactor this logic out of this method

    cognito_auth_flow = Cognito_Auth_Flow()
    result = cognito_auth_flow.create_cbr_token_cookie_from_cognito_code(sign_in_code=sign_in_code)

    if result.get('status') != 'ok':
        return result                                                # todo: add better error page
    cookie_data = result.get('data')
    cbr_token       = cookie_data.get('cookie_value')
    user_info       = cookie_data.get('user_info' , {})
    role            = user_info.get('cognito:groups')
    render_kwargs   = {"template_name_or_list": "/home/accounts/logging_in.html",
                       "session_id"           : cbr_token                       }
    response_html   = render_template(**render_kwargs)
    response        = make_response(response_html)

    response.set_cookie(COOKIE_NAME__CBR__SESSION_ID__USER  , cbr_token)
    response.set_cookie(COOKIE_NAME__CBR__SESSION_ID__ACTIVE, cbr_token)

    return response




@blueprint.route('/unauthorized')
@allow_anonymous
def unauthorized():
    from flask import render_template
    return render_template('home/accounts/unauthorized.html')

@blueprint.route('/sign-out')
def sign_out():
    from flask import redirect, make_response
    from cbr_website_beta.cbr__flask.utils.current_server import current_server

    from cbr_shared.cbr_sites.CBR__Shared__Constants import COOKIE_NAME__CBR__SESSION_ID__PERSONA, COOKIE_NAME__CBR__SESSION_ID__USER, COOKIE_NAME__CBR__SESSION_ID__ACTIVE

    redirect_to = redirect(current_server())
    response    = make_response(redirect_to)
    response.set_cookie(COOKIE_NAME__CBR__SESSION_ID__USER   , '', expires=0)
    response.set_cookie(COOKIE_NAME__CBR__SESSION_ID__PERSONA, '', expires=0)
    response.set_cookie(COOKIE_NAME__CBR__SESSION_ID__ACTIVE , '', expires=0)
    return response

# todo: see if we need this (since at the moment this is not wired)
@blueprint.route('/logout')
@allow_anonymous
def logout():
    from flask import redirect
    from cbr_website_beta.cbr__flask.utils.current_server import current_server

    url = COGNITO_SIGN_OUT + f"logout_uri={current_server()}sign-out"

    return redirect(url)

@blueprint.route('/user/profile', methods=['GET', 'POST'])
@allow_anonymous
def profile():
    from cbr_website_beta.apps.user.user_profile import user_profile
    return user_profile()


# new user markdown driven routes

@blueprint.route('/user/<page_name>')
@allow_anonymous
def home(page_name):
    import re
    from flask import render_template

    safe_page_name  = re.sub(r'[^a-z-]', '',page_name)
    title           = safe_page_name.replace('-', ' ').capitalize()
    content_view    = 'includes/component/markdown-content.html'
    markdown_page   = f'en/web-site/user/{safe_page_name}.md'
    template_name   = '/pages/page_with_view.html'
    return render_template(template_name_or_list = template_name,
                           title                 =  title       ,
                           content_view          = content_view ,
                           markdown_page         = markdown_page,
                           disable_cdn           = True         )
