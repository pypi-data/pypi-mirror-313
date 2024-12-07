from decimal                                                        import Decimal
from cbr_athena.aws.dynamo_db.DyDB__CBR_Logging                     import DYNAMO_DB__TABLE___REGION_NAME, DYNAMO_DB__TABLE___ACCOUNT_ID
from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website
from cbr_website_beta._cbr_shared.schemas.CBR_Request               import CBR_Request
from osbot_aws.apis.Session                                         import Session
from osbot_aws.aws.dynamo_db.domains.DyDB__Table_With_Timestamp     import DyDB__Table_With_Timestamp
from osbot_utils.decorators.methods.cache_on_self                   import cache_on_self
from osbot_utils.utils.Dev                                          import pprint
from osbot_utils.utils.Misc                                         import date_time_now

DYNAMO_DB__TABLE_NAME__CBR_REQUESTS =  f'arn:aws:dynamodb:{DYNAMO_DB__TABLE___REGION_NAME}:{DYNAMO_DB__TABLE___ACCOUNT_ID}:table/{{env}}__cbr_requests'
TABLE_CBR_REQUESTS__INDEXES_NAMES   = [ 'date'      , 'ip_address', 'host'      , 'level'      , 'method'     ,
                                        'path'      , 'referer'   , 'req_id'    , 'session_id' , 'status_code',
                                        'source'    , 'user'      , 'user_role' , 'user_status'               ]

class DyDB__CBR_Requests(DyDB__Table_With_Timestamp):

    env : str = server_config__cbr_website.env()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_name    = DYNAMO_DB__TABLE_NAME__CBR_REQUESTS.format(env=self.env)
        self.table_indexes = TABLE_CBR_REQUESTS__INDEXES_NAMES
        self.disabled      = server_config__cbr_website.aws_disabled()
        self.dynamo_db.client = self.client

    @cache_on_self
    def client(self):
        return Session().client('dynamodb', region_name=DYNAMO_DB__TABLE___REGION_NAME)

    def date_today(self):
        return date_time_now(date_time_format='%Y-%m-%d')

    def log_request(self, cbr_request: CBR_Request):
        if self.disabled:
            return
        if type(cbr_request) is not CBR_Request:            # only allow cbr_request
            return
        document = cbr_request.json()
        return self.add_document(document)

    def log_request_response(self, request, response, duration):
        if self.disabled:
            return
        try:
            headers     = {key: value for key, value in request.headers.items()}
            cbr_request = CBR_Request()
            # indexes
            cbr_request.date        = self.date_today()
            cbr_request.host        = headers.get('host')
            cbr_request.ip_address  = request.client.host
            cbr_request.level       = 'DEBUG'
            cbr_request.method      = request.method
            cbr_request.path        = request.url.path
            cbr_request.source      = 'odin'
            cbr_request.status_code = str(response.status_code)

            # other
            cbr_request.duration    = Decimal(round(duration, 2))
            cbr_request.headers     = headers
            cbr_request.query       = dict(request.query_params)

            self.add_document(cbr_request.json())
        except Exception as e:
            print('>>>>> MAJOR ERROR in log_request_response <<<<')
            pprint(e)               # todo: add to logging


dydb_cbr_requests = DyDB__CBR_Requests()