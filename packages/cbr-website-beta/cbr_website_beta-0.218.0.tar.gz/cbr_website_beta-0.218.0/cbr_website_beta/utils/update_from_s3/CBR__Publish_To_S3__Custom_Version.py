from osbot_utils.utils.Env import get_env, set_env

import cbr_website_beta
from cbr_website_beta.utils.update_from_s3.Release_Package__via__S3 import Release_Package__via__S3
from osbot_utils.helpers.Zip_Bytes                                  import Zip_Bytes
from osbot_utils.utils.Files import path_combine, file_delete
from osbot_utils.utils.Json import json_load, from_json_str, to_json_str

FILE_PATTERNS__CBR_WEBSITE_BETA                 = ["^(?!.*DS_Store).*"]#[".*.py", ".*.html", ".*.css", ".*.js", "^(.*/)?version$"]
FILE_PATTERNS__CUSTOM_CODE                      = ["^(?!.*DS_Store).*"]
ENV_VAR_NAME__CBR__CUSTOM__PACKAGES_TO_INSTALL  = 'CBR__CUSTOM__PACKAGES_TO_INSTALL'
ENV_VAR_NAME__CBR__CUSTOM__PATH_CUSTOM_CODE     = 'CBR__CUSTOM__PATH_CUSTOM_CODE'

class CBR__Publish_To_S3__Custom_Version(Release_Package__via__S3):

    zip_bytes: Zip_Bytes

    def add_code_files__from_package(self, package_name):
        import importlib
        module         = importlib.import_module(package_name)
        target_package = importlib.import_module(package_name)
        code_folder    = target_package.path
        package_name   = package_name + '/'
        #cbr_code_folder = cbr_website_beta.path

        with self.zip_bytes as _:
            _.add_folder__from_disk__with_prefix (code_folder, package_name, *FILE_PATTERNS__CBR_WEBSITE_BETA)
            _.remove_files                       ( ".*.pyc")
        return self

    def add_code_files__custom_folder(self, custom_folder_path=None):
        if custom_folder_path:
            with self.zip_bytes as _:
                _.add_folder__from_disk(custom_folder_path, *FILE_PATTERNS__CUSTOM_CODE)
                return _.list()

    def create_zip_file(self, packages,  path_custom_files=None):
        for package in packages:
            self.add_code_files__from_package(package)
        self.add_code_files__custom_folder(path_custom_files)
        self.zip_bytes.save_to(self.path_temp_zip_file())
        return self

    def execute_workflow(self):
        packages          = self.packages_to_install()
        path_custom_files = self.path_custom_files()
        print(f'   packages         : {packages}'         )
        print(f'   path_custom_files: {path_custom_files}')

        if packages and path_custom_files and self.enabled():
            file_delete(self.path_temp_zip_file())
            self.s3_zip_file_delete()
            self.create_zip_file(packages, path_custom_files)
            self.upload_zip_file_to_s3()
            return self.s3_zip_file_exists()
        return False

    def packages_to_install(self):
        value = get_env(ENV_VAR_NAME__CBR__CUSTOM__PACKAGES_TO_INSTALL,'')
        return from_json_str(value)

    def path_custom_files(self):
        return get_env(ENV_VAR_NAME__CBR__CUSTOM__PATH_CUSTOM_CODE, '')

    def set_packages_to_install(self,value):
        set_env(ENV_VAR_NAME__CBR__CUSTOM__PACKAGES_TO_INSTALL, to_json_str(value))
        return self

    def set_path_custom_files(self,value):
        set_env(ENV_VAR_NAME__CBR__CUSTOM__PATH_CUSTOM_CODE, value)
        return self

if __name__ == '__main__':
    if CBR__Publish_To_S3__Custom_Version().execute_workflow():
        print("======== CBR__Publish_To_S3__Custom_Version: OK           ==========")
    else:
        print("======== CBR__Publish_To_S3__Custom_Version: Not enabled ==========")