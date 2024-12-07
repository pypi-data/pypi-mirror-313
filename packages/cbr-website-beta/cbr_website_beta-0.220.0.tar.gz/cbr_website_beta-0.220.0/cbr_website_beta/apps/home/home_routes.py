from cbr_website_beta._cbr_shared.dynamo_db.DyDB__CBR_Logging   import DyDB__CBR_Logging
from cbr_website_beta.cbr__flask.decorators.allow_annonymous    import allow_anonymous
from cbr_website_beta.apps.home                                 import blueprint



COGNITO_SIGN_IN       = 'https://the-cbr-beta.auth.eu-west-2.amazoncognito.com/login?client_id=5ij6l5kdho4umoks5rjfh9cbid&response_type=code&scope=email+openid+phone&redirect_uri={cbr_domain}/web/sign-in'
COGNITO_SIGN_OUT      = 'https://the-cbr-beta.auth.eu-west-2.amazoncognito.com/logout?client_id=5ij6l5kdho4umoks5rjfh9cbid&response_type=code&scope=email+openid+phone&logout_uri={cbr_domain}/web/sign-out'
CBR_DOMAIN            = 'https://www.thecyberboardroom.com'
#DEV_DOMAIN            = 'http://localhost:5000'
EXPECTED_ROUTES__HOME = [ '/<path:path>' , '/terms_and_conditions', '/service-worker.js']

EXPECTED_METHODS_HOME = ['home_blueprint.path_path'                 ,
                         'home_blueprint.service_worker'            ,
                         'home_blueprint.terms_and_conditions'      ,
                         'llms_blueprint.just_chat_ui'              ,
                         'llms_blueprint.multiple_athenas'          ,
                         'llms_blueprint.no_system_prompt'          ]

dydb_cbr_logging = DyDB__CBR_Logging()

def running_in_aws():
    import os
    return 'AWS_EXECUTION_ENV' in os.environ


@blueprint.route('/service-worker.js')
@allow_anonymous
def service_worker():
    from cbr_website_beta.utils.Version import version
    from flask import render_template, make_response

    content  = render_template('scripts/service-worker.js', version=version)
    response = make_response(content)
    response.headers['Content-Type'] = 'application/javascript'
    return response


@blueprint.route('/terms_and_conditions')
@allow_anonymous
def terms_and_conditions():
    from flask import render_template

    return render_template('home/terms_and_conditions.html')

@blueprint.route('/<path:path>')
@allow_anonymous
def path_path(path):            # todo: remove the need for this route
    from jinja2 import TemplateNotFound
    from flask import render_template, request
    from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website

    try:
        #if path == 'athena'  : path = 'athena/index.html'           # todo: find a better to map these top level paths
        if path == 'content' : path = 'content/index.html'
        if path.endswith("/"): path += "index.html"
        elif not path.endswith('.html'):    path += '.html'

        # Detect the current page
        kwargs = dict(template_name_or_list = "home/" + path                                             ,
                      breadcrumbs           = map_breadcrumbs(request)                                   ,
                      url_athena            = server_config__cbr_website.target_athena_url() + '/open_ai/prompt_with_system__stream',  # todo: refactor direct render of the multiple athena UIs
                      page_title            = 'title'                                                    )

        return render_template(**kwargs)

    except TemplateNotFound as error:
        print(f"***** error 404 : {error}")
        return render_template('home/page-404.html', path=path), 404

    except Exception as error:
        print(f"***** error 500 : {error}")
        dydb_cbr_logging.log_exception(error)
        return render_template('home/page-500.html'), 500

@blueprint.route('/screenshot/<path:path>')
@allow_anonymous
def screenshot_for_path(path=None):
    from osbot_utils.utils.Misc import base64_to_bytes
    from osbot_utils.utils.Http import GET_json
    from cbr_website_beta.cbr__flask.utils.current_server import current_server
    from flask                                             import Response

    target_server = current_server()
    if ':5001' in target_server:
        target_server   = "https://dev.cyber-boardroom.com/"
    url_for_screenshot  = f'{target_server}{path}'                                                                                  # todo: add path validation
    screenshot_data_url = f'https://serverless-flows.dev.aws.cyber-boardroom.com/browser/url-screenshot?url={url_for_screenshot}'   # todo: refactor to separate class for serverless-flows
    screenshot_data     = GET_json(screenshot_data_url)
    screenshot_bytes    = base64_to_bytes(screenshot_data.get('screenshot_base64'))

    return Response(
        screenshot_bytes,
        content_type='image/png'
    )

# Helper - Extract current page name from request
def map_breadcrumbs(request):
    from cbr_website_beta.utils.Page_Utils import Page_Utils
    return Page_Utils().map_breadcrumbs(request)
    # breadcrumbs = [
    #     # {'name': 'Home', 'url'  : '#'},
    #     # {'name': 'Section A'    , 'url': '#'},
    #     # {'name': 'Blank Page!!!', 'url': None}
    # ]
    # path = ''
    # for key in request.path.split('/'):
    #     path += '/{key}'
    #     breadcrumbs.append({'name': key, 'url': path})
    # pprint(breadcrumbs)
    # return breadcrumbs
    # try:
    #     segment = request.path.split('/')[-1]
    #     if segment == '':
    #         segment = 'index'
    #     return segment
    # except:
    #     return None


@blueprint.route('/webc')
@allow_anonymous
def webc():
    from flask import render_template
    from cbr_website_beta.cbr__flask.utils.reset_flask_cache import reset_flask_cache

    reset_flask_cache()
    title         = "WebC version"
    template_name = "/pages/page-with-webc.html"
    return render_template(template_name_or_list=template_name,title=title)

@blueprint.route('/webc-dev')
@blueprint.route('/webc-dev/')
@blueprint.route('/webc-dev/<path:path>')
@allow_anonymous
def webc_dev(path=None):
    from flask import render_template
    from cbr_website_beta.cbr__flask.utils.reset_flask_cache import reset_flask_cache

    reset_flask_cache()
    title         = "WebC (Dev) version"
    template_name = "/pages/page-with-webc-dev.html"
    return render_template(template_name_or_list=template_name,title=title)
