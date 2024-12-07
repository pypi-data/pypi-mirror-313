from itertools import islice

from cbr_website_beta.aws.s3.DB_Odin_Data import DB_Odin_Data
from cbr_website_beta.data.odin.Analysis__Users_Sessions import Analysis__Users_Sessions
from osbot_aws.aws.dynamo_db.Dynamo_DB__Table import Dynamo_DB__Table
from osbot_utils.testing.Duration import Duration


class DyDB__Sessions(Dynamo_DB__Table):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_name = 'tcb_sessions'
        self.key_name   = 'session_id'

    def add_session(self, session_id, session_data):
        session = {'session_id': session_id,
                   **session_data          }

        return self.add_document(session).get('data').get('document')

    def delete_all(self):
        return self.clear_table().get('data').get('delete_status')

    def delete_session(self, session_id):
        return self.delete_document(session_id).get('data')

    def load_from_s3(self):
        #with Duration('Load session data from S3'):
        db_odin_data = DB_Odin_Data()                                           # todo: fix circular dependency with the DB_Odin_Data and DyDB__Sessions. This S3 logic needs to be refactored in to separate class
        sessions_data = db_odin_data.current_sessions__from_s3().get('data')

        sessions_to_add = []
        sessions_added  = []
        #with Duration('Adding all sessions to DynamoDB'):
        for session_id, session_data in sessions_data.items():
            session_data[self.key_name] = session_id
            sessions_to_add.append(session_data)
            sessions_added.append(session_id)
        self.add_documents(sessions_to_add)
        return sessions_added

    def session(self, session_id):
        return self.document(session_id).get('data')

    # todo implement using new logging DB
    def sessions(self):
        return []
        #return self.documents().get('data')


