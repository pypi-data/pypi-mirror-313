from cbr_athena.aws.dynamo_db.DyDB__CBR_Logging                 import DYNAMO_DB__TABLE___REGION_NAME, DYNAMO_DB__TABLE___ACCOUNT_ID
from osbot_aws.aws.dynamo_db.domains.DyDB__Table_With_Timestamp import DyDB__Table_With_Timestamp
from osbot_utils.decorators.methods.cache_on_self               import cache_on_self
from osbot_utils.utils.Misc                                     import date_time_now

DYNAMO_DB__TABLE_NAME__CBR_LOGGING = f'arn:aws:dynamodb:{DYNAMO_DB__TABLE___REGION_NAME}:{DYNAMO_DB__TABLE___ACCOUNT_ID}:table/{{env}}__cbr_logging'

#TABLE_CBR_LOGGING__INDEXES_NAMES   = [ 'date', 'level', 'message', 'source', 'topic']

class DyDB__CBR_Logging(DyDB__Table_With_Timestamp):

    def __init__(self, **kwargs):
        from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website

        super().__init__(**kwargs)
        self.env           = server_config__cbr_website.env()
        self.table_name    = DYNAMO_DB__TABLE_NAME__CBR_LOGGING.format(env=self.env)
        self.disabled      = server_config__cbr_website.aws_disabled()
        self.dynamo_db.client = self.client

    @cache_on_self
    def client(self):
        from osbot_aws.apis.Session import Session

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

    def log_error(self, message, log_data):
        from cbr_website_beta._cbr_shared.schemas.CBR_Logging import CBR_Logging

        if self.disabled:
            return
        try:
            with CBR_Logging() as _:
                _.date        = self.date_today()
                _.message     = message
                _.level       = 'ERROR'
                _.source      = 'odin'
                _.status_code = '500'
                _.extra_data  = log_data
                result = self.add_document(_.json())
                document_id = result.get('document', {}).get('id')
                print(f'>>>> added error as {document_id} to {self.table_name}')

        except Exception as e:
            print('>>>>> MAJOR ERROR in log_error <<<<')
            from osbot_utils.utils.Dev import pprint
            pprint(e)               # todo: add to logging

    def log_exception(self, exception):
        import traceback

        if self.disabled:
            return
        stack_trace = traceback.format_exc()
        log_data = {
            'error': str(exception),
            'stack_trace': stack_trace,
            'description': 'Internal Server Error occurred.'
        }
        message = f"ERROR 500: { log_data.get('error') }"
        self.log_error(message, log_data)

    def add_log_message(self, message, **kwargs):
        from cbr_website_beta._cbr_shared.schemas.CBR_Logging import CBR_Logging

        if self.disabled:
            return
        cbr_logging = CBR_Logging(message=message, **kwargs)
        cbr_logging.date = self.date_today()
        document = cbr_logging.json()

        result = self.add_document(document)

        document_id = result.get('document', {}).get('id')
        return document_id



    def query__today__last_n_hours(self, hours=1):
        if self.disabled:
            return []
        filter_key   = 'date'
        filter_value = self.date_today()
        documents = self.query_index_last_n_hours(filter_key, filter_value, hours)
        return documents

    def query__today__last_n_hours__where_header__matches(self, header_name, header_value, hours=1):
        if self.disabled:
            return []
        filter_key   = 'date'
        filter_value = self.date_today()
        query_filter = { 'filter_expression'     : "#extra_data.#event.#headers.#websocket_key = :websocket_key_value",
                         'expression_attr_names' : { '#extra_data'         : 'extra_data'        ,
                                                     '#event'              : 'event'             ,
                                                     '#headers'            : 'headers'           ,
                                                     '#websocket_key'      : header_name},
                         'expression_attr_values': { ':websocket_key_value': {'S': header_value} }}
        documents = self.query_index_last_n_hours(filter_key, filter_value, hours, query_filter)
        return documents

    def query__today__last_n_hours__where_field__contains(self, field_name, field_value, hours=1, field_type='S'):
        if self.disabled:
            return []
        filter_key      = 'date'
        filter_value    = self.date_today()
        query_filter    = {'filter_expression'     : "contains(#key, :value)"              ,
                           'expression_attr_names' : { '#key'  : field_name               },
                           'expression_attr_values': { ':value': {field_type: field_value}}}
        documents = self.query_index_last_n_hours(filter_key, filter_value, hours, query_filter)
        return documents


dydb_cbr_logging = DyDB__CBR_Logging()