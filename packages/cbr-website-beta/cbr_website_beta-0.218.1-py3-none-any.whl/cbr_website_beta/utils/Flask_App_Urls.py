import os

from osbot_utils.utils.Misc                                 import list_set
from cbr_website_beta.utils._for_osbot.for_OSBot_Utils      import convert_paths_into_folder_dict
from osbot_utils.utils.Files                                import path_combine, files_list


class Flask_App_Urls:

    def __init__(self, app):
        self.app = app

    # get the list of all possible virtual paths to files that exists on disk
    def paths_to_static_pages(self, start_from=None):
        template_directory = self.template_folder()
        all_files          = files_list(template_directory)
        all_possible_paths = set()

        for file in all_files:
            # Remove the prefix of the template directory and the '.html' suffix
            path = os.path.relpath(file, template_directory)[:-5].replace("\\", "/")  # Replace backslashes on Windows
            original_path = path

            # Rule 1
            if path == 'athena':
                all_possible_paths.add('athena')
                path = 'athena/index'
            # Rule 2
            elif path == 'content':
                all_possible_paths.add('content')
                path = 'content/index'
            # Rule 3
            if path.endswith('/'):
                path += 'index'

            # Rule 3 (handle bug) # todo: fix this bug
            if start_from =='home' and path=='includes/home':           # handle coner case cause by the fact that the template name is the same as the folder (we need a better way to map these files and the attack surface)
                all_possible_paths.add('/home')
                all_possible_paths.add('/home.html')
                continue
            # Add both the URL form and the .html form for each path
            if start_from:
                if start_from not in path:
                    continue
                else:
                    path          = path         [len(start_from):]
                    original_path = original_path[len(start_from):]
            all_possible_paths.add(path)
            all_possible_paths.add(original_path + '.html')

        return list_set(all_possible_paths)

    def paths_to_static_pages_as_dict(self):
        return convert_paths_into_folder_dict(self.paths_to_static_pages())

    def root_path(self):
        return self.app.root_path

    def template_folder(self):
        return path_combine(self.root_path(), self.app.template_folder)