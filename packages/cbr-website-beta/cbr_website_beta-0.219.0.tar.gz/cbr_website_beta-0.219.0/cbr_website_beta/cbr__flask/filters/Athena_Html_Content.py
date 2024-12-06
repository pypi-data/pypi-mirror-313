from cbr_website_beta.content.CBR__Content__Static  import cbr_content_static
from osbot_utils.base_classes.Type_Safe             import Type_Safe

class Athena_Html_Content(Type_Safe):
    filter_name       : str = 'athena_html_content'

    def __init__(self, app):
        app.jinja_env.filters[self.filter_name] = self.athena_html_content # todo: find a better way to register these filters
        super().__init__()

    def athena_html_content(self, path):
        try:
            content = cbr_content_static.file_contents__for__web_page(path)
            return content
        except Exception as e:
            #dydb_cbr_logging.log_exception(e)
            return "Error in loading athena content"
