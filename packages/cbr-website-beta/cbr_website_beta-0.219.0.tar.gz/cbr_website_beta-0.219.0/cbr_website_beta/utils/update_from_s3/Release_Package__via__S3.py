import cbr_user_session

import cbr_user_data

import cbr_athena
import cbr_content
import cbr_shared

import cbr_static

import cbr_web_components
import cbr_website_beta
import osbot_fast_api
from   cbr_website_beta.utils.remote_shell.CBR__Remote_Shell__Copy_Files  import CBR__REMOTE_SHELL__FILE_TRANSFER__S3_BUCKET, CBR__REMOTE_SHELL__FILE_TRANSFER__PARENT_FOLDER
from osbot_aws.aws.s3.S3                                                  import S3

from   osbot_utils.decorators.methods.cache_on_self                       import cache_on_self
from osbot_utils.utils.Env import get_env, set_env

from   osbot_utils.base_classes.Type_Safe                                 import Type_Safe
from   osbot_utils.testing.Temp_Folder                                    import Temp_Folder
from   osbot_utils.testing.Temp_Zip                                       import Temp_Zip
from   osbot_utils.utils.Dev                                              import pprint
from   osbot_utils.utils.Files                                            import path_combine, folder_copy, files_list, file_contents
from osbot_utils.utils.Str import str_safe
from   osbot_utils.utils.Zip                                              import zip_bytes__unzip_to_folder

ENV_VAR_NAME__S3_DEV__S3_BUCKET     = 'S3_DEV__BUCKET'
ENV_VAR_NAME__S3_DEV__PARENT_FOLDER = 'S3_DEV__PARENT_FOLDER'
ENV_VAR_NAME__S3_DEV__VERSION       = 'S3_DEV__VERSION'
ENV_VAR_NAME__S3_DEV__PACKAGE_NAME  = 'S3_DEV__PACKAGE_NAME'
DEFAULT_VALUE__PACKAGE_NAME         = 'cbr_website_beta'
DEFAULT_VALUE__TEMP_ZIP_FILE_FOLDER = '/tmp'

class Release_Package__via__S3(Type_Safe):
    s3 : S3

    # actions

    def unzip_from_s3_to_folder(self, target_folder):
        if self.enabled():
            zip_bytes = self.s3.file_bytes(self.s3_bucket(), self.s3_key())
            zip_bytes__unzip_to_folder(zip_bytes, target_folder)
            return target_folder

    def upload_zip_file_to_s3(self):
        if self.enabled():
            self.s3.file_upload_to_key(file=self.path_temp_zip_file(), bucket=self.s3_bucket(), key=self.s3_key())
            print(f"[Release_Package__via__S3]: Uploaded zip file to S3 bucket: {self.s3_bucket()} with key: {self.s3_key()}")
            return True
        else:
            print("[Release_Package__via__S3]: Skipping upload to S3")
            return False

    def create_zip_with__cbr_website_beta(self):
        if self.enabled():
            source_folder_1 = cbr_website_beta.path
            source_folder_2 = cbr_static.path
            source_folder_3 = cbr_athena.path
            source_folder_4 = cbr_content.path
            source_folder_5 = cbr_web_components.path
            source_folder_6 = cbr_shared.path
            source_folder_7 = osbot_fast_api.path
            source_folder_8 = cbr_user_data.path
            source_folder_9 = cbr_user_session.path

            ignore_pattern = ['*.pyc', '.DS_Store', '__pycache__', '*.env']

            with Temp_Folder(temp_prefix=self.package_name()) as _:
                #destination = path_combine(_.path(), self.package_name())
                destination_1 = path_combine(_.path(), "cbr_website_beta"  ) # todo: refactor this to allow multiple packages as params
                destination_2 = path_combine(_.path(), "cbr_static"        )
                destination_3 = path_combine(_.path(), "cbr_athena"        )
                destination_4 = path_combine(_.path(), "cbr_content"       )
                destination_5 = path_combine(_.path(), "cbr_web_components")
                destination_6 = path_combine(_.path(), "cbr_shared"        )
                destination_7 = path_combine(_.path(), "osbot_fast_api"    )
                destination_8 = path_combine(_.path(), "cbr_user_data"     )
                destination_9 = path_combine(_.path(), "cbr_user_session"  )

                folder_copy(source=source_folder_1, destination=destination_1, ignore_pattern=ignore_pattern)
                folder_copy(source=source_folder_2, destination=destination_2, ignore_pattern=ignore_pattern)
                folder_copy(source=source_folder_3, destination=destination_3, ignore_pattern=ignore_pattern)
                folder_copy(source=source_folder_4, destination=destination_4, ignore_pattern=ignore_pattern)
                folder_copy(source=source_folder_5, destination=destination_5, ignore_pattern=ignore_pattern)
                folder_copy(source=source_folder_6, destination=destination_6, ignore_pattern=ignore_pattern)
                folder_copy(source=source_folder_7, destination=destination_7, ignore_pattern=ignore_pattern)
                folder_copy(source=source_folder_8, destination=destination_8, ignore_pattern=ignore_pattern)
                folder_copy(source=source_folder_9, destination=destination_9, ignore_pattern=ignore_pattern)

                with Temp_Zip(_.path()) as temp_zip:
                    temp_zip.move_to(self.path_temp_zip_file())
                return self.path_temp_zip_file()

    def s3_zip_file_delete(self):
        return self.s3.file_delete(bucket = self.s3_bucket(), key = self.s3_key())

    def s3_zip_file_exists(self):
        return self.s3.file_exists(bucket = self.s3_bucket(), key = self.s3_key())

    def download_to_local_temp(self):
        print()
        print('========== download_to_local_temp ==========')
        target_folder = '/tmp'
        release_from_s3 = Release_Package__via__S3()
        if release_from_s3.disabled():
            print('release_from_s3 is disabled, (i.e. S3_DEV__VERSION was not set). Skipping rest of worklfow...')
        else:
            print('    release_from_s3 is enabled')
            with release_from_s3 as _:
                print(f'   s3_bucket: {_.s3_bucket()}')
                print(f'   s3_key   : {_.s3_key()}')
                # print(f'   s3_bucket: { _.s3_bucket()}')
                if _.s3.file_exists(_.s3_bucket(), _.s3_key()):
                    print('   file exists in S3')
                    _.unzip_from_s3_to_folder(target_folder=target_folder)
                    pprint(f' there were {len(files_list(target_folder))} files extracted')
                    pprint(file_contents('/tmp/cbr_website_cbr/version'))
                    return True
                else:
                    print('   ERROR: file did not exists in S3')
        print('========== download_to_local_temp ==========')
        return False

    def download_zip_file_from_s3__as_bytes(self):
        if self.enabled():
            return self.s3.file_bytes(self.s3_bucket(), self.s3_key())

    # vars
    def enabled(self):
        if self.release_id() and self.s3_bucket():
            return True
        return False

    def disabled(self):
        return self.enabled() is False

    def package_name    (self): return get_env(ENV_VAR_NAME__S3_DEV__PACKAGE_NAME , DEFAULT_VALUE__PACKAGE_NAME                    )
    def s3_bucket       (self): return get_env(ENV_VAR_NAME__S3_DEV__S3_BUCKET    , CBR__REMOTE_SHELL__FILE_TRANSFER__S3_BUCKET    )
    def s3_parent_folder(self): return get_env(ENV_VAR_NAME__S3_DEV__PARENT_FOLDER, CBR__REMOTE_SHELL__FILE_TRANSFER__PARENT_FOLDER)

    @cache_on_self
    def s3_folder(self):
        return f'{self.s3_parent_folder()}/{self.package_name()}'

    @cache_on_self
    def s3_key(self):
        s3_key       = f'{self.s3_folder()}/{self.release_id()}.zip'
        return s3_key

    def release_id(self):
        return get_env(ENV_VAR_NAME__S3_DEV__VERSION)

    def path_temp_zip_file(self):
        zip_file_name = str_safe(f'{self.package_name()}__{self.release_id()}.zip')
        path_zip_file = path_combine(DEFAULT_VALUE__TEMP_ZIP_FILE_FOLDER, zip_file_name)
        return path_zip_file # '/tmp/cbr_website_beta.zip'

    def set_release_id(self, value):
        set_env(ENV_VAR_NAME__S3_DEV__VERSION, value)
        return self

if __name__ == '__main__':
    Release_Package__via__S3().download_to_local_temp()

