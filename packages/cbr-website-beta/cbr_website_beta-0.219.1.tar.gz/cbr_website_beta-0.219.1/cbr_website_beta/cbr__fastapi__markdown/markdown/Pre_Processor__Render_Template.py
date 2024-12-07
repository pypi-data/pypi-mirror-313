import re


from markdown.preprocessors import Preprocessor



class Pre_Processor__Render_Template(Preprocessor):
    RE = re.compile(r'{{render_template\("([^"]+)"\)}}')

    def __init__(self, md):
        super().__init__(md)

    def run(self, lines):
        new_lines = []
        for line in lines:
            m = self.RE.search(line)
            if m:
                template_path = m.group(1)
                rendered_template = self.render_template(template_path)
                new_lines.append(rendered_template)
            else:
                new_lines.append(line)
        return new_lines

    def render_template(self, template_path):
        from flask import render_template
        from osbot_utils.utils.Dev import pprint

        try:
            from cbr_website_beta.cbr__fastapi.CBR__Fast_API import cbr_fast_api                # need to do this here to avoid circular dependencies
            flask_app = cbr_fast_api.cbr__flask().app()
            with flask_app.app_context():
                return render_template(template_path)
        except Exception as error:
            pprint(error)
            return f'{type(error).__name__} Error in Pre_Processor__Render_Template: {error}'