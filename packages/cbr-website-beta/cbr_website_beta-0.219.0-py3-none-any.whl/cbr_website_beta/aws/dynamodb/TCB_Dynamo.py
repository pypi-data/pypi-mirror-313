from cbr_website_beta.aws.dynamodb.DyDB__Sessions import DyDB__Sessions
from osbot_aws.aws.dynamo_db.Dynamo_DB import Dynamo_DB

class TCB_Dynamo:

    def __init__(self):
        self.dynamo     = Dynamo_DB()

    def tables(self):
        return self.dynamo.tables()

    def table__sessions(self):
        table = DyDB__Sessions()
        table.create_table()
        return table