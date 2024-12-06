from flask import render_template

from cbr_website_beta.apps.dev.odin.Odin__Panels__Session_Management import Odin__Panels__Session_Management
from osbot_utils.utils.Str import str_safe


class Render_View:

    def debug_views(self, class_name, method_name, **method_kwargs):
        template_file = "dev/panels-debug.html"
        kwargs = self.dev_panels__render_kwargs(template_file, class_name, method_name, **method_kwargs)
        return render_template(**kwargs)

    def debug_views__render_kwargs(self):
        return { "template_name_or_list" : "dev/panels.html"    ,
                 "title"                 : "Debug Views"        }

    def render_view(self, class_name, method_name, **method_kwargs):
        template_file = "dev/panels.html"
        kwargs        = self.dev_panels__render_kwargs(template_file, class_name, method_name, **method_kwargs)
        return render_template(**kwargs)

    def dev_panels__render_kwargs(self, template_file, class_name, method_name, **method_kwargs):
        return { "template_name_or_list" : template_file        ,
                 "title"                 : "Dev Panels"         ,
                 "class_name"            : str_safe(class_name) ,
                 "method_name"           : str_safe(method_name),
                 "method_kwargs"         : method_kwargs        }