import cbr_website_beta
from fastapi                                      import Request
from cbr_website_beta.utils.Version               import version__cbr_web_components
from osbot_fast_api.api.Fast_API_Routes           import Fast_API_Routes
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Files                      import path_combine_safe
from osbot_utils.utils.Str                        import str_safe

URL__CDN_SERVER    ="https://static.dev.aws.cyber-boardroom.com/cbr-web-components"
PAGE__MAIN_PAGE      = 'pages/page-cbr.html'
PAGE__MAIN_PAGE__DEV = 'pages/page-cbr-dev.html'


class CBR__WebC__Routes(Fast_API_Routes):
    tag       : str = 'ui'


    def cbr_webc(self, request: Request, version=None, path=None):
        if version:
            version = str_safe(version)
        else:
            version = version__cbr_web_components
        if version == 'dev':
            template_path = PAGE__MAIN_PAGE__DEV
        else:
            template_path = PAGE__MAIN_PAGE
        params  = dict(cdn_server = URL__CDN_SERVER,
                       request    = request        ,
                       version    = version        )
        return self.templates().TemplateResponse(template_path,params)

    def redirect_to_latest(self):
        from fastapi.responses import RedirectResponse

        path = f'/{self.tag}/{version__cbr_web_components}'
        return RedirectResponse(url=path)

    @cache_on_self
    def templates(self):
        from fastapi.templating import Jinja2Templates
        return Jinja2Templates(directory=path_combine_safe(cbr_website_beta.path, 'apps/templates'))

    def setup_routes(self):
        self.router.add_api_route(path=''                       , endpoint=self.redirect_to_latest, methods=['GET'])
        self.router.add_api_route(path='/'                      , endpoint=self.redirect_to_latest, methods=['GET'])
        self.router.add_api_route(path='/{version}'             , endpoint=self.cbr_webc          , methods=['GET'])
        self.router.add_api_route(path='/{version}/'            , endpoint=self.cbr_webc          , methods=['GET'])
        self.router.add_api_route(path='/{version}/{path:path}' , endpoint=self.cbr_webc          , methods=['GET'])