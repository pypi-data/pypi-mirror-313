from osbot_aws.aws.apigateway.apigw_dydb.WS__DyDB import WS__DyDB

TABLE_NAME__CBR__WS__DyDB = 'web_sockets'

class CBR__WS__DyDB(WS__DyDB):

    def __init__ (self):
        super().__init__()
        self.table_name = TABLE_NAME__CBR__WS__DyDB

    def handle_route(self, connection_id, source=None, lambda_event=None):
        dydb_document = self.dydb_document(connection_id, load_data=False)
        dydb_document.increment_field('request_count', 1)
        return super().handle_route(connection_id, source, lambda_event)