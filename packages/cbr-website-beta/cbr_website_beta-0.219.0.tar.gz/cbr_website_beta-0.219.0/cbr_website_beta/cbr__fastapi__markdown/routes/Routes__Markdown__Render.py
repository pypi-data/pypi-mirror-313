from pydantic import BaseModel

from osbot_markdown.markdown.Markdown_Parser        import Markdown_Parser
from cbr_website_beta.content.CBR__Content__Static  import CBR__Content__Static
from osbot_fast_api.api.Fast_API_Routes             import Fast_API_Routes

ROUTE_PATH__RENDER        = 'render'
EXPECTED_SITE_INFO_ROUTES = ['/extensions']

class Markdown_Text(BaseModel):
    text : str

class Routes__Markdown__Render(Fast_API_Routes):
    cbr_content_static: CBR__Content__Static
    markdown_parser   : Markdown_Parser
    tag               : str = ROUTE_PATH__RENDER

    def extensions(self):
        return f'{self.markdown_parser.extensions()}'

    def markdown_file_to_html_and_metadata(self, path='/'):
        markdown_text = self.cbr_content_static.file_contents(path)
        return self.markdown_parser.markdown_to_html_and_metadata(markdown_text)

    def markdown_to_html(self, markdown_text: Markdown_Text):
        return self.markdown_parser.markdown_to_html(markdown_text.text)

    def markdown_to_html_and_metadata(self, markdown_text: Markdown_Text):
        return self.markdown_parser.markdown_to_html_and_metadata(markdown_text.text)

    def setup_routes(self):
        self.add_route_get (self.extensions                        )
        self.add_route_get (self.markdown_file_to_html_and_metadata)
        self.add_route_post(self.markdown_to_html                  )
        self.add_route_post(self.markdown_to_html_and_metadata     )
