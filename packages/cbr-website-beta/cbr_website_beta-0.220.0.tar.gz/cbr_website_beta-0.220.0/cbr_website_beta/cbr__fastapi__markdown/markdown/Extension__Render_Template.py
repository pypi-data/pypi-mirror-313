from markdown import Extension

from cbr_website_beta.cbr__fastapi__markdown.markdown.Pre_Processor__Render_Template import Pre_Processor__Render_Template


#from osbot_markdown.markdown.md__pre_processors.Pre_Processor__Render_Template import Pre_Processor__Render_Template

# todo: SECURITY: check for the security implications of this extension (since although in principle there should be no sensitive data in the
#       render_template views (all sensitive data should be provided to the view), we need to double check this)
class Extension__Render_Template(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(Pre_Processor__Render_Template(md), 'flask_template', 175)
