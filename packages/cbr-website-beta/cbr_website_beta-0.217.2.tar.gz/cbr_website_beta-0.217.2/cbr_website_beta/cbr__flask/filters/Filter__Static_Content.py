from cbr_website_beta.content.CBR__Content__Static  import cbr_content_static
from osbot_utils.utils.Dev                          import pprint


class Filter__Static_Content():

    filter_name = 'static_content'

    def __init__(self, app):
        app.jinja_env.filters[self.filter_name] = self.static_content


    def static_content(self,target, lang='en'):
        return cbr_content_static.file_contents__for__web_page(target,language=lang)