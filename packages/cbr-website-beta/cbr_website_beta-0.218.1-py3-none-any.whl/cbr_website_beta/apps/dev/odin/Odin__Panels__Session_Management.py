from flask import render_template

from cbr_website_beta.data.odin.Analysis__Users_Data import Analysis__Users_Data
from cbr_website_beta.data.odin.Analysis__Users_Sessions import Analysis__Users_Sessions
from osbot_utils.utils.Misc import timestamp_to_str_date, timestamp_to_str_time

HTML_TITLE_CURRENT_SESSIONS = 'CBR Current Sessions'
HTML_TITLE_CURRENT_USERS    = 'CBR Current Users'

class Odin__Panels__Session_Management:

    def __init__(self):
        self.analysis__users_data = Analysis__Users_Data()

    def exposed_methods(self):                                                  # todo: find a better name for this method and move into base class
        return { 'sample_panel'    : self.sample_panel           ,
                 'current_sessions': self.view__current_sessions ,
                 'current_users'   : self.view__current_users    }

    def view__current_sessions(self):
        render_kwargs =  self.current_sessions__render_kwargs()
        return render_template(**render_kwargs)

    def view__current_users(self):
        render_kwargs =  self.current_users__render_kwargs()
        return render_template(**render_kwargs)

    def sample_panel(self, var_1='var_1', var_2='var_2'):
        return f"<h3>this is a sample panel with {var_1} and {var_2}</h3>"


    # helper methods (to refactor into separate class)

    def current_users__render_kwargs(self):

        users_data = self.analysis__users_data.analysis__users_data()
        metadata   = self.analysis__users_data.users_metadatas__metadata()


        return { "template_name_or_list" : "dev/current_users.html" ,
                 "title"                 : HTML_TITLE_CURRENT_USERS ,
                 "current_users"         : users_data               ,
                 'metadata'              : metadata                 }


    def current_sessions__render_kwargs(self):
        analysis__users_sessions = Analysis__Users_Sessions()
        view_data                = analysis__users_sessions.view_data__current_sessions()
        table_data               = view_data.get('table_data')
        metadata                 = view_data.get('metadata'  )
        sessions_by_user         = analysis__users_sessions.analysis__sessions_by_user()

        return { "template_name_or_list" : "dev/current_sessions.html" ,
                 "title"                 : HTML_TITLE_CURRENT_SESSIONS ,
                 "table_data"            : table_data                  ,
                 'metadata'              : metadata                    ,
                 'sessions_by_user'      : sessions_by_user            }






