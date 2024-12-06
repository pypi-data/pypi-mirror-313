from flask import render_template

from cbr_website_beta.aws.apigateway.web_sockets.WS__Users import WS__Users


class Odin__Panels__Real_Time:

    def __init__(self):
        self.ws_users = WS__Users()

    def exposed_methods(self):                                                  # todo: find a better name for this method and move into base class
        return { 'chat_prompt' : self.chat_prompt,
                 'log_streams' : self.log_streams ,
                 'code_editor' : self.code_editor}

    def log_streams(self):
        return render_template(**self.logs_streams__kwargs())

    def logs_streams__kwargs(self):
        user_data = {'active_connections': self.ws_users.active_connections(),
                     'endpoint_url': self.ws_users.wss_endpoint_url()}
        return {"template_name_or_list": "dev/odin/panels/log-streams/log-streams.html",
                "title": "Logs Streams!!",
                "user_data": user_data}

    def code_editor(self):
        return render_template(**self.code_editor__kwargs())

    def code_editor__kwargs(self):
        user_data = {'endpoint_url': self.ws_users.wss_endpoint_url()}
        return {"template_name_or_list": "dev/odin/panels/code-editor/code-editor.html",
                "title": "Code editor",
                "user_data": user_data}

    def chat_prompt(self):
        render_kwargs = {"template_name_or_list": "dev/odin/panels/odin-chat/odin-chat.html",
                         "title": "Odin Chat",}
        return render_template(**render_kwargs)
