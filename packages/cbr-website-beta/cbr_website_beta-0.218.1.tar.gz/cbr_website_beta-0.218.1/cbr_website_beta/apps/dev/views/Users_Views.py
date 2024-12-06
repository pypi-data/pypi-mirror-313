from flask                                      import render_template
from cbr_shared.cbr_backend.users.S3_DB__Users  import S3_DB__Users
from osbot_utils.testing.Duration               import Duration
from osbot_utils.utils.Lists                    import list_sorted, list_chunks
from osbot_utils.utils.Str                      import safe_str

HTML_TITLE_CURRENT_USERS = 'CBR Current Users'
MAX_USERS_TO_FETCH       = None # 40

class Users_Views:

    def current_user(self, user_id=None):
        user_id = safe_str(user_id)
        return render_template(**self.current_user__render_config(user_id))

    # def current_users(self):
    #     return render_template(**self.current_users__render_config())

    def current_user__render_config(self, user_id):
        user_data = self.data__current_user(user_id)
        return { "template_name_or_list" : "dev/current_user.html" ,
                 "title"                 : HTML_TITLE_CURRENT_USERS ,
                 "user_data"             : user_data            }

    # def current_users__render_config(self):
    #     current_users = self.data__current_users(max=MAX_USERS_TO_FETCH)
    #     return { "template_name_or_list" : "dev/current_users.html" ,
    #              "title"                 : HTML_TITLE_CURRENT_USERS ,
    #              "current_users"         : current_users            }

    def data__current_user(self, user_id):
        db_users = S3_DB__Users()
        user     = db_users.db_user(user_id)
        return user.metadata()

    def data__current_users(self, split_at=6, max=None):
        db_users   = S3_DB__Users()
        users_ids  = []
        with Duration(print_result=False) as duration:
            all_user_ids = sorted(db_users.db_users_ids())
            if max:
                all_user_ids = all_user_ids[:max]
            for user_id in all_user_ids:
                fixed_user_id = user_id.replace('_', ' ')
                users_ids.append(fixed_user_id)

        data = list(list_chunks(users_ids, split_at))
        stats = dict(session_count=len(users_ids),
                     s3_fetch_duration=round(duration.seconds(), 2))
        table_data = dict(stats=stats, data=data)

        return table_data