from cbr_website_beta.aws.apigateway.web_sockets.CBR__WS__DyDB  import CBR__WS__DyDB
from osbot_aws.aws.apigateway.API_Gateway_Management_API        import API_Gateway_Management_API
from osbot_utils.decorators.methods.cache_on_self               import cache_on_self
from osbot_aws.AWS_Config                                       import aws_config
from osbot_utils.base_classes.Kwargs_To_Self                    import Kwargs_To_Self
from osbot_utils.utils.Lists                                    import list_group_by
from osbot_utils.utils.Misc                                     import timestamp_to_str_time, timestamp_utc_now

class WS__Users(Kwargs_To_Self):
    dydb_ws     : CBR__WS__DyDB
    api_gateway : API_Gateway_Management_API

    def __init__(self):
        super().__init__()
        self.api_gateway = API_Gateway_Management_API(endpoint_url=self.boto3_endpoint_url())

    def active_connections__docs_metadata(self):
        try:
            return  self.dydb_ws.query_index('status','S', 'active')

        except Exception as e:
            print(f'Exception: {e}')
            return []

    def active_connections(self):
        docs_metadata = self.active_connections__docs_metadata()
        return [document.get('id') for document in docs_metadata]

    def action_connections__by_name(self):
        return list_group_by(values=self.active_connections__docs_metadata(), group_by='connection_name')

    def connection_id__for_name(self, name):
        name_connection_ids = self.connection_ids__for_name(name)
        if len(name_connection_ids) > 0:                    # if there are connection_ids with this name
            return name_connection_ids[0]                   # return  the first one

    def connection_ids__for_name(self, name):
        user_connections = self.action_connections__by_name().get(name, [])
        return [connection.get('id') for connection in user_connections]

    def user_messages(self, connection_id):
        return self.dydb_ws.document(connection_id)

    def send_to_active_connections(self, topic, data):
        active_connections = self.active_connections()
        print(active_connections)
        for connection_id in active_connections:
            self.send_ws_message(connection_id, topic, data)

            #with Duration(prefix=f'Sending messager to  on {connection_id}'):
            #dydb_document = self.dydb_ws.dydb_document(document_id=connection_id,load_data=False)
            #dydb_document.add_to_list('messages', {'sent_to_active_connections': data})


        return {'status': 'ok', 'data': data, 'active_connections': active_connections}

    def send_ws_message(self, connection_id, topic, data):
        try:
            timestamp = timestamp_utc_now()
            client_message = dict(when  = timestamp_to_str_time(timestamp),
                                  topic = topic                           ,
                                  data  = data                            )
            self.api_gateway.post_to_connection(connection_id, client_message)
            print(f'sent ws message to: {connection_id}')
            return True
        except Exception as e:
            print(f'[ERROR] failed to send  ws message to: {connection_id} | {e}')
            return False

    def send_ws_message__to_name(self,target_name, topic, data):
        connection_ids = self.connection_ids__for_name(target_name)
        if connection_ids:
            for connection_id in connection_ids:
                self.send_ws_message(connection_id, topic, data)
                print(f"message sent to '{target_name}'")
            return
        print(f"no connection found with name '{target_name}'")

    def api_gw__id(self):
        return 'ow2twc6ee4'  # todo : move to env variable

    def api_gw__region_name(self):
        return aws_config.region_name()

    def api_gw__stage(self):
        return 'prod'

    @cache_on_self
    def boto3_endpoint_url(self):

        endpoint_url = f'https://{self.api_gw__id()}.execute-api.{self.api_gw__region_name()}.amazonaws.com/{self.api_gw__stage()}'
        return endpoint_url

    def wss_endpoint_url(self):
        endpoint_url = f"wss://{self.api_gw__id()}.execute-api.{self.api_gw__region_name()}.amazonaws.com/{self.api_gw__stage()}"
        return endpoint_url
