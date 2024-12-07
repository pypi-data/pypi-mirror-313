from flask import render_template


class Odin__Panels__Debug:

    def exposed_methods(self):
        return { 'debug_views': self.debug_views,
                 'log_message': self.log_message}


    # exposed methods
    def debug_views(self, **kwargs):
        from cbr_website_beta.apps.dev.Render_Panels__Test_Data import Render_Panels__Test_Data     # handle circular dependency
        render_panels_test_data = Render_Panels__Test_Data()
        views_mappings          = render_panels_test_data.available_classes_and_methods()

        class_name              = kwargs.get('class_name' , 'NA')
        method_name             = kwargs.get('method_name', 'NA')
        method_kwargs           = kwargs.get('class_name' , {}  )

        class_name    = 'odin_logs'
        method_name   = 'cbr_requests'
        method_kwargs = {'env': 'LOCAL', 'hours': 1}


        render_kwargs = dict(template_name_or_list = "dev/debug/debug-views/debug-views.html" ,
                             class_name            = class_name                   ,
                             method_name           = method_name                  ,
                             method_kwargs         = method_kwargs                ,
                             views_mappings        = views_mappings               )
        return render_template(**render_kwargs)

    def log_message(self, message='an message from CBR website'):
        render_kwargs = dict(template_name_or_list = "dev/debug/log-message/log-message.html",
                             message               = message                     )
        return render_template(**render_kwargs)