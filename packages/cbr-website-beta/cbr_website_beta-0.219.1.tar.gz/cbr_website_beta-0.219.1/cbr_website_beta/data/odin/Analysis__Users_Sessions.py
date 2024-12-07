from cbr_website_beta.aws.s3.DB_Odin_Data           import DB_Odin_Data
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.utils.Dev                          import pprint
from osbot_utils.utils.Misc                         import timestamp_to_str_date, timestamp_to_str_time


class Analysis__Users_Sessions:

    def __init__(self):
        self.db_odin_data = DB_Odin_Data()

    def analysis__sessions_by_user(self):
        data = self.sessions__data()
        consolidated_view = {}

        for session in data.values():
            username  = session['data']['username']
            timestamp = session['timestamp']
            role      = session['data'].get('cognito:groups')
            if type(role) is list:
                role = role[0]
            else:
                role = 'normal user'

            if username not in consolidated_view:
                consolidated_view[username] = {'number_of_sessions': 1, 'latest_timestamp': timestamp, 'username': username }
                consolidated_view[username]['session_date'] = timestamp_to_str_date(timestamp)
                consolidated_view[username]['session_time'] = timestamp_to_str_time(timestamp)
                consolidated_view[username]['user_role'   ] = role
                consolidated_view[username]['session_id'  ] = session['session_id']
            else:
                consolidated_view[username]['number_of_sessions'] += 1
                if timestamp > consolidated_view[username]['latest_timestamp']:
                    consolidated_view[username]['latest_timestamp' ] = timestamp
                    consolidated_view[username]['session_date'     ] = timestamp_to_str_date(timestamp)
                    consolidated_view[username]['session_time'     ] = timestamp_to_str_time(timestamp)
                    consolidated_view[username]['session_id'       ] = session['session_id']


        # for user in consolidated_view.values():
        #     del user['latest_timestamp']

        return list(consolidated_view.values())

    @cache_on_self
    def sessions(self):
        return self.db_odin_data.current_sessions()

    def sessions__data(self):
        return self.sessions().get('data')

    def sessions__metadata(self):
        return self.sessions().get('metadata')


    def table_data__current_sessions(self, data):
        table_data = []

        for session_id, session_data in data.items():
            data         = session_data.get('data', {})
            user_groups  = data.get('cognito:groups'   )
            username     = data.get('username'         )
            user_id      = data.get('sub'              )
            source       = session_data.get('source'   )
            timestamp    = session_data.get('timestamp')
            row = dict( username    = username                           ,
                        date        = timestamp_to_str_date(timestamp)   ,
                        time        = timestamp_to_str_time(timestamp)   ,
                        user_groups = user_groups                        ,
                        session_id  = session_id                         ,
                        source      = source                             ,
                        user_id     = user_id                            )

            table_data.append(row)

        return table_data

    def view_data__current_sessions(self):
        data        = self.sessions__data()
        metadata    = self.sessions__metadata()
        table_data  = self.table_data__current_sessions(data)
        return { 'table_data' : table_data, 'metadata' : metadata }
