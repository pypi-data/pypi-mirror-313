import os
from pathlib import Path

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env import get_env

from osbot_utils.utils.Files import folder_name, parent_folder, current_folder, files_list, files_names, \
    file_name_without_extension, is_not_file


# todo: check is this should moved to OSBot utils, this feel quite a use-case specific method
def convert_paths_into_folder_dict(data_set):
    def insert_into_dict(d, parts):
        if len(parts) == 1:
            if "files" not in d:
                d["files"] = {}
            d["files"][parts[0]] = None  # Or some default value
        else:
            head, *tail = parts
            if head not in d:
                d[head] = {}
            insert_into_dict(d[head], tail)

    folder_dict = {}

    for item in data_set:
        parts = item.split('/')
        insert_into_dict(folder_dict, parts)

    return folder_dict




