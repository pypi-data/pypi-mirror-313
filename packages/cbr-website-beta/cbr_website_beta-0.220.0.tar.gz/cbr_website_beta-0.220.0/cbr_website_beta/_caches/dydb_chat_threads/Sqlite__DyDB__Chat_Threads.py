import json
from os import environ

from osbot_aws.aws.dynamo_db.Dynamo_DB import Dynamo_DB
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import path_combine, folder_exists, files_list, file_contents, file_lines, file_name, \
    file_exists, file_contents_gz, current_temp_folder
from osbot_utils.utils.Json import json_file_load, json_loads, json_parse, json_lines_file_load, json_file_contents_gz, \
    json_lines_file_load_gz, json_dumps
from osbot_utils.utils.Misc import list_set, to_int

ENV_NAME__PATH_LOCAL_DATA         = 'PATH_LOCAL_DATA'
ENV_NAME__FOLDER_NAME_DYDB_BACKUP = 'FOLDER_NAME_DYDB_BACKUP'
ENV_NAME__PATH_LOCAL_DBS          = 'PATH_LOCAL_DBS'
DB_NAME                           = 'cbr_chat_threads.sqlite'
TABLE_NAME__DYDB_DATA             = 'dydb_data'
TABLE_NAME__CBR_CHAT_THREADS      = 'cbr_chat_threads'

class Table_DyDB_Data(Kwargs_To_Self):
    chat_thread : str
    dy_id       : str
    thread_id   : str
    user        : str

class Table_Chat_Threads(Kwargs_To_Self):
    dy_id          : str
    thread_id      : str
    user           : str
    answer         : str
    data_type      : str
    req_index      : int
    timestamp      : int
    histories      : str
    images         : str
    max_tokens     : int
    model          : str
    seed           : int
    system_prompts : str
    temperature    : int
    user_prompt    : str

class Sqlite__DyDB__Chat_Threads(Kwargs_To_Self):
    path_local_data         : str
    folder_name_dydb_backup : str
    db_chat_threads         : Sqlite__Database

    @cache_on_self
    def path_dydb_backup_files(self):
        if not self.path_local_data:
            self.path_local_data         = environ.get(ENV_NAME__PATH_LOCAL_DATA         , '')
        if not self.folder_name_dydb_backup:
            self.folder_name_dydb_backup = environ.get(ENV_NAME__FOLDER_NAME_DYDB_BACKUP , '')
        if self.path_local_data and self.folder_name_dydb_backup:
            return path_combine(self.path_local_data, self.folder_name_dydb_backup)
        return None

    def dydb_backup_files(self):
        return files_list(self.path_dydb_backup_files())

    def manifest_files(self):
        file_path = path_combine(self.path_dydb_backup_files(), 'manifest-files.json')
        return json_lines_file_load(file_path)

    def manifest_files_contents(self):
        path_dydb_backup_files = self.path_dydb_backup_files()
        files_contents         = {}
        for manifest_file_name in self.manifest_files_names():
            manifest_file_path = path_combine(path_dydb_backup_files, manifest_file_name)
            if file_exists(manifest_file_path):
                file_data = json_lines_file_load_gz(manifest_file_path)
                files_contents[manifest_file_name] = file_data
        return files_contents

    def manifest_files_names(self):
        files_names = []
        for manifest_file in self.manifest_files():
            data_file_s3_key   = manifest_file.get('dataFileS3Key')
            manifest_file_name = file_name(data_file_s3_key, check_if_exists=False)
            files_names.append(manifest_file_name)
        return files_names

    def manifest_summary(self):
        file_path = path_combine(self.path_dydb_backup_files(), 'manifest-summary.json')
        return json_file_load(file_path)

    def has_dydb_backup_files(self):
        path_dydb_backup_files = self.path_dydb_backup_files()
        if folder_exists(path_dydb_backup_files):
            if len(files_list(path_dydb_backup_files)):
                return True
        return False

    def path_db_folder(self):
        return environ.get(ENV_NAME__PATH_LOCAL_DBS) or current_temp_folder()

    def path_db(self):
        return path_combine(self.path_db_folder(), DB_NAME)

    @cache_on_self
    def sqlite_database(self):
        return Sqlite__Database(db_path=self.path_db())

    @cache_on_self
    def table__cbr_chat_threads(self):
        table = self.sqlite_database().table(TABLE_NAME__CBR_CHAT_THREADS)
        #table.delete()
        table.row_schema = Table_Chat_Threads
        if table.not_exists():
            table.create()
        return table

    @cache_on_self
    def table__dydb_data(self):
        table = self.sqlite_database().table(TABLE_NAME__DYDB_DATA)
        table.row_schema = Table_DyDB_Data
        if table.not_exists():
            table.create()
        return table

    def table__dydb_data__add_data_from_backup(self):
        dynamo_db = Dynamo_DB()
        table = self.table__dydb_data()
        #table.clear()
        table_size = table.size()
        if table_size > 0:
            return table_size
        backup_files_contents = self.manifest_files_contents()
        for file_name, file_data in backup_files_contents.items():
            for entry in file_data:
                item        = entry.get('Item')
                item_data   = dynamo_db.document_deserialise(item)
                new_db_obj = table.new_row_obj()
                new_db_obj.chat_thread = json_dumps(item_data.get('chat_thread'))
                new_db_obj.dy_id       = item_data.get('dy_id')
                new_db_obj.thread_id   = item_data.get('thread_id')
                new_db_obj.user        = item_data.get('user')
                table.row_add_and_commit(new_db_obj)
            #break
        return len(table.rows())


    def table__cbr_chat_threads__load_data(self):
        table          = self.table__cbr_chat_threads()
        #table.clear()
        table_size = table.size()
        if table_size > 0:
            return table_size
        table_raw_data = self.table__dydb_data()
        raw_data = table_raw_data.rows()
        for item in raw_data:
            chat_thread_raw = item.get('chat_thread'     )
            dy_id           = item.get('dy_id'           )
            thread_id       = item.get('thread_id'       )
            user            = item.get('user'            )
            chat_thread     = json_loads(chat_thread_raw )
            data            = chat_thread.get('data' , {})
            row_data = dict(dy_id           = dy_id     ,
                            thread_id       = thread_id ,
                            user            = user      ,
                            answer          =            chat_thread.get('answer'            )             ,
                            data_type       =            chat_thread.get('data_type'         )             ,
                            req_index       = to_int    (chat_thread.get('index'             ),None),
                            timestamp       = to_int    (chat_thread.get('timestamp'         ),None),
                            histories       = json_dumps(data       .get('histories'     , [])            ),
                            images          = json_dumps(data       .get('images'        , [])            ),
                            max_tokens      = to_int    (data       .get('max_tokens'        ),None),
                            model           =            data       .get('model'             )             ,
                            seed            = to_int    (data       .get('seed'              ),None),
                            system_prompts  = json_dumps(data       .get('system_prompts', [])            ),
                            temperature     = to_int    (data       .get('temperature'       ),None),
                            user_prompt     =            data       .get('user_prompt'       )             )
            table.add_row(**row_data)

        table.commit()

        return len(table.rows())

