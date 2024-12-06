from cbr_website_beta.cbr__fastapi__markdown.routes.Routes__Markdown__Render import Routes__Markdown__Render
from cbr_website_beta.cbr__fastapi__markdown.routes.Routes__Static__Content  import Routes__Static__Content
from osbot_fast_api.api.Fast_API                                             import Fast_API


class CBR__Fast_API__Markdown(Fast_API):

    def setup_routes(self):
        self.add_routes(Routes__Markdown__Render)
        self.add_routes(Routes__Static__Content )
