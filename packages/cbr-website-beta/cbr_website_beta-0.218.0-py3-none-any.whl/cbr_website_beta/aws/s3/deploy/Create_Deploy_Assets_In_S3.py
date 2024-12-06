#from cbr_website_beta                               import static
from cbr_website_beta.aws.s3.S3                     import S3
from cbr_website_beta.utils.Site_Utils              import Site_Utils
from osbot_aws.AWS_Config                           import aws_config
from cbr_website_beta.utils.Version                 import version
from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.utils.Dev                          import pprint
from osbot_utils.utils.Files                        import files_list, path_combine

BUCKET__STATIC_ASSETS  = '{account_id}-cbr'
S3_FOLDER__CLOUD_FRONT = 'cbr_website_static'
FOLDER_NAME__DIST      = 'dist'
S3_FOLDER__DIST        = f'{S3_FOLDER__CLOUD_FRONT}/{FOLDER_NAME__DIST}'


class Create_Deploy_Assets_In_S3(Kwargs_To_Self):
    version    : str

    def __init__(self):
        super().__init__()
        self.version = version

    @cache_on_self
    def s3(self):
        return S3()

    def map_local_files_to_s3_keys(self):
        path_static_files = path_combine(static.path, FOLDER_NAME__DIST)

        js_files          = files_list(path_static_files, '*.js')
        files_to_upload   = {}
        for local_file_path in js_files:
            virtual_file_path = local_file_path.replace(path_static_files, '')
            s3_key            = self.s3_key_for_uploaded_file(virtual_file_path)
            files_to_upload[s3_key] = local_file_path
        return files_to_upload

    def s3_key_for_uploaded_file(self, virtual_path):
        s3_key = f"{S3_FOLDER__DIST}/{self.version}{virtual_path}"
        return s3_key

    def target_bucket(self):
        return BUCKET__STATIC_ASSETS.format(account_id=aws_config.account_id())

    def upload_files_to_s3(self):
        print()
        s3_bucket         = self.target_bucket()
        s3_keys_for_files = self.map_local_files_to_s3_keys()
        for s3_key, local_file_path in s3_keys_for_files.items():
            print(f'uploading: {s3_key}')
            self.s3().file_upload_to_key(local_file_path, s3_bucket, s3_key)
        return f'Uploaded {len(s3_keys_for_files)} files to s3'

