from cbr_shared.aws.s3.S3_DB_Base   import S3_DB_Base
from osbot_utils.utils.Misc         import timestamp_utc_now, timestamp_to_str_date, timestamp_to_str_time

FILE_NAME_CURRENT_SESSIONS = 'current-sessions.json'
FILE_NAME_USERS_METADATA   = 'users-metadata.json'

class DB_Odin_Data(S3_DB_Base):

    def chat_threads(self):
        return []
        #return DyDB__Chat_Threads().documents()

    def current_sessions(self):
        return self.current_sessions__from_dydb()

    def current_sessions__from_dydb(self):
        from cbr_website_beta.aws.dynamodb.DyDB__Sessions import DyDB__Sessions         # todo: fix circular dependency with the DB_Odin_Data and DyDB__Sessions (the S3 methods below need to be refactored in to separate class )
        dydb_sessions = DyDB__Sessions()
        raw_sessions_data = dydb_sessions.sessions()
        sessions_data = {}
        if raw_sessions_data:
            for raw_session_data in raw_sessions_data:                      # todo: refactor this into a helper method
                session_id = raw_session_data.get('session_id')            #       we need to do this at the moment the data is supposed to be a dict
                sessions_data[session_id] = raw_session_data                #       and indexed by the session_id

        return {'metadata': self.file_metadata('Odin', source='DyDB'),
                'data'    : sessions_data }

    def current_sessions__from_s3(self):
        return self.s3_file_data(self.s3_key__current_sessions())

    def current_sessions__save_to_s3(self, data, saved_by='Odin'):
        file_data = { 'metadata' : self.file_metadata(saved_by=saved_by, source='S3'),
                      'data'     : data                                 }
        return self.s3_save_data(file_data, self.s3_key__current_sessions())

    def file_metadata(self, saved_by, source):
        timestamp      = timestamp_utc_now()
        timestamp_data = timestamp_to_str_date(timestamp)
        timestamp_time = timestamp_to_str_time(timestamp)
        return dict (timestamp      = timestamp     ,
                     timestamp_date = timestamp_data,
                     timestamp_time = timestamp_time,
                     saved_by       = saved_by      ,
                     source         = source       )

    def s3_key__current_sessions(self):
        return f'{self.s3_folder_odin_data()}/{FILE_NAME_CURRENT_SESSIONS}'

    def s3_key__users_metadatas(self):
        return f'{self.s3_folder_odin_data()}/{FILE_NAME_USERS_METADATA}'


    def users_metadatas(self):
        return self.s3_file_data(self.s3_key__users_metadatas())

    def users_metadatas__save(self, users_metatada, saved_by='NA', runtime='NA'):
        file_data = { 'metadata' : self.file_metadata(saved_by, runtime),
                      'data'     : users_metatada                       }
        return self.s3_save_data(file_data, self.s3_key__users_metadatas())