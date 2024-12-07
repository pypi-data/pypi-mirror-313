

from cbr_website_beta.aws.s3.DB_Odin_Data import DB_Odin_Data
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Dev import pprint


class Analysis__Users_Data:

    def __init__(self):
        self.db_odin_data = DB_Odin_Data()

    def analysis__users_data(self):
        data = self.users_metadatas__data()
        users_data = []
        def add_field(target, source, field_name, source_field_1, source_field_2):
            target[field_name] = source.get(source_field_1) or source.get(source_field_2) or ''


        for user_metadata in data.values():
            user_data = { 'user_id': user_metadata.get('user_id') }
            add_field(user_data, user_metadata, 'first_name'  , 'First name'          , ''                      )
            add_field(user_data, user_metadata, 'last_name'   , 'Last name'           , ''                      )
            add_field(user_data, user_metadata, 'role'        , 'Role'                , 'title'                 )
            add_field(user_data, user_metadata, 'organisation', 'Organisation'        , 'organisation'          )
            add_field(user_data, user_metadata, 'linkedin'    , 'Linkedin'            , 'linkedin'              )
            add_field(user_data, user_metadata, 'country'     , 'Country'             , 'country'               )
            add_field(user_data, user_metadata, 'sector'      , 'Sector'              , 'sector'                )
            add_field(user_data, user_metadata, 'org_size'    , 'Size of organisation', 'size of organisation'  )
            users_data.append(user_data)

            if 'Additional suggested prompts for Athena, your AI advisor' in user_metadata:
                del user_metadata['Additional suggested prompts for Athena, your AI advisor']
            if 'cognito_data' in user_metadata:
                del user_metadata['cognito_data']
        return users_data

    @cache_on_self
    def users_metadatas(self):
        return self.db_odin_data.users_metadatas()

    def users_metadatas__data(self):
        return self.users_metadatas().get('data')

    def users_metadatas__metadata(self):
        return self.users_metadatas().get('metadata')