from osbot_markdown.markdown.Markdown_Parser              import markdown_parser
from osbot_utils.base_classes.Type_Safe                   import Type_Safe
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Files import Sqlite__DB__Files
from osbot_utils.utils.Files                              import files_list, file_exists, file_contents, path_combine_safe, parent_folder, folders_names_in_folder, file_save, files_names_in_folder, file_extension
from osbot_utils.utils.Json                               import json_load_file
from osbot_utils.utils.Misc                               import remove
from osbot_utils.utils.Status                             import status_ok
from osbot_utils.utils.Toml                               import toml_file_load

FOLDER_NAME__WEB_PAGES                  = 'web-pages'
FOLDER_NAME__BASE_FOLDER                = 'docs'
CBR_CONTENT_FILES__SUPPORTED_EXTENSIONS = ['.md']
CBR_DATA_FILES__SUPPORTED_EXTENSIONS    = ['.json', '.toml']

class CBR__Content__Static(Type_Safe):

    def all_content(self):
        all_content = {}
        for file_path in self.content_files__md():
            all_content[file_path] = self.file_contents(file_path)
        return all_content

    def all_contents__in_sqlite_db(self):
        db_files =  Sqlite__DB__Files()
        for file, contents in self.all_content().items():
            #file_metadata = {}
            db_files.add_file(file, contents)
        return db_files

    def base_folder(self, target_file):
        base_folder    = FOLDER_NAME__BASE_FOLDER
        file_location  = self.path_web_page(target_file)
        root_folder    = self.path_web_pages()
        file_path      = path_combine_safe(root_folder, file_location)
        if file_path:
            folder_path  = parent_folder(file_path)
            child_folder = folder_path.replace(root_folder, '')
            if child_folder != '/':
                base_folder += child_folder[1:]
        return base_folder

    def content_files(self, pattern="*"):
        return files_list(self.path_static_content(), pattern=pattern)

    def content_files__md(self):
        base_folder = self.path_static_content() + '/'
        md_files = []
        for file_path in self.content_files(pattern="*.md"):
            md_file = remove(file_path, base_folder)
            md_files.append(md_file)
        return md_files

    def file_contents(self, target_file):
        full_path = self.path_static_content_file(target_file)
        if file_extension(full_path) not in CBR_CONTENT_FILES__SUPPORTED_EXTENSIONS:
            return "Error: File extension not supported"
        if file_exists(full_path):
            return file_contents(full_path)

    def file_data(self, target_file):
        full_path        = self.path_static_content_file(target_file)
        target_extension = file_extension(full_path)
        if target_extension not in CBR_DATA_FILES__SUPPORTED_EXTENSIONS:
            return "Error: File extension not supported"
        if file_exists(full_path):
            if target_extension == '.json':
                return json_load_file(full_path)
            if target_extension == '.toml':
                return toml_file_load(full_path)

    def file_contents__raw__for__web_page(self, file_name, language='en', file_extension='md'):
        target_file        = self.path_web_page(file_name=file_name, language=language, file_extension=file_extension)
        file_contents__raw = self.file_contents(target_file)
        return file_contents__raw

    def file_contents__for__web_page(self, file_name, language='en', file_extension='md'):
        file_contents__raw    = self.file_contents__raw__for__web_page(file_name, language=language, file_extension=file_extension)
        if file_contents__raw:
            file_contents__parsed = self.parse_file_contents(file_contents__raw, file_extension=file_extension)
            return file_contents__parsed
        return '(no content)'


    def files(self, target):
        path_folder = self.parent_folder_of_target(target)
        #return files_in_folder(path_folder)
        return files_names_in_folder(path_folder)

    def folders(self, target):
        path_folder = self.parent_folder_of_target(target)
        return folders_names_in_folder(path_folder)

    def parse_file_contents(self, file_contents, file_extension):
        if file_extension == 'md':
            return markdown_parser.content_to_html(file_contents)
        return ''

    def parent_folder_of_target(self, target):
        relative_path = self.path_web_page(target)
        full_path     = self.path_static_content_file(relative_path)
        path_folder   = parent_folder(full_path)
        return path_folder

    def path_static_content_file(self,relative_path):
        return path_combine_safe(self.path_static_content(), relative_path)

    def path_web_page(self, file_name, language='en', file_extension='md'):
        return f'{self.path_web_pages(language)}/{file_name}.{file_extension}'

    def path_web_pages(self,language='en'):
        return f"{language}/{FOLDER_NAME__WEB_PAGES}"

    def path_to_file(self, file_location):
        return path_combine_safe(self.path_static_content(), file_location)

    def path_static_content(self):
        import cbr_content

        return cbr_content.path

    def parent_folder(self, target_file):
        base_folder = self.base_folder(target_file)
        if base_folder != FOLDER_NAME__BASE_FOLDER:
            return parent_folder(base_folder, use_full_path=False)
        return base_folder

    def save_file_contents__for__web_page(self, file_name, contents, language='en', file_extension='md'):
        target_file = self.path_web_page(file_name=file_name,language=language, file_extension=file_extension)
        full_path   = self.path_static_content_file(target_file)
        file_save(contents, full_path)
        return status_ok()

cbr_content_static = CBR__Content__Static()