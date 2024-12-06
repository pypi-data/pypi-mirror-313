import traceback

from cbr_athena.aws.dynamo_db.DyDB__CBR_Logging                 import DYNAMO_DB__TABLE___REGION_NAME, DYNAMO_DB__TABLE___ACCOUNT_ID
from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website
from osbot_aws.apis.Session                                     import Session
from osbot_aws.aws.dynamo_db.domains.DyDB__Table_With_Timestamp import DyDB__Table_With_Timestamp
from osbot_utils.decorators.methods.cache_on_self               import cache_on_self
from osbot_utils.utils.Misc                                     import date_time_now

DYNAMO_DB__TABLE_NAME__USER_SESSIONS =  f'arn:aws:dynamodb:{DYNAMO_DB__TABLE___REGION_NAME}:{DYNAMO_DB__TABLE___ACCOUNT_ID}:table/{{env}}__cbr_user_sessions'

class DyDB__CBR_User_Sessions(DyDB__Table_With_Timestamp):

    env: str = server_config__cbr_website.env()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_name  = DYNAMO_DB__TABLE_NAME__USER_SESSIONS.format(env=self.env)
        self.disabled    = server_config__cbr_website.aws_disabled()
        self.dynamo_db.client = self.client

    @cache_on_self
    def client(self):
        return Session().client('dynamodb', region_name=DYNAMO_DB__TABLE___REGION_NAME)

    def date_today(self):
        return date_time_now(date_time_format='%Y-%m-%d')

    def documents__today(self):
        if self.disabled:
            return []
        index_name  = 'date'
        index_type  = 'S'
        index_value = date_time_now(date_time_format='%Y-%m-%d')
        documents = self.query_index(index_name=index_name, index_type=index_type, index_value=index_value)
        return documents



dydb_cbr_user_sessions = DyDB__CBR_User_Sessions()
