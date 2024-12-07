# from osbot_aws.aws.dynamo_db.DyDB__Timeseries import DyDB__Timeseries
# from osbot_utils.utils.Misc import timestamp_utc_now
#
#
# class DyDB__Chat_Threads(DyDB__Timeseries):
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.table_name          = 'tcb_chat_threads'
#         self.key_name            = 'thread_id'
#         self.key_attribute_type  = 'S'
#         self.index_name          = 'chats_by_user'
#         self.partition_key_name  = 'user'
#         self.partition_key_value = 'user_x'
#         self.data_field_name     = 'chat_thread'
#
#     def add_document(self, document, partition=None):
#         if self.key_name not in document:
#             document[self.key_name] = self.dynamo_db.random_id()     # If key is present, generate a random UUID as the key
#         return self.dynamo_db.document_add(table_name=self.table_name, key_name=self.key_name, document=document)
#
#     def add_chat_thread(self, user_name, thread_id, index, data_type, data):
#         data['timestamp'] = timestamp_utc_now()                         # make sure each request has a unique timestamp
#         data['index'    ] = index                                       # for now store the index in the data
#         data['data_type'] = data_type                                   # for now store the data_type in the data
#         document = { self.primary_key         : self.dynamo_db.random_id()  ,
#                      self.key_name            : thread_id              ,
#                      self.partition_key_name  : user_name                   ,
#                      self.data_field_name     : data                        }
#
#         return self.add_document(document)
#
#     def documents(self,partition=None):
#         return self.dynamo_db.documents_all(table_name=self.table_name)