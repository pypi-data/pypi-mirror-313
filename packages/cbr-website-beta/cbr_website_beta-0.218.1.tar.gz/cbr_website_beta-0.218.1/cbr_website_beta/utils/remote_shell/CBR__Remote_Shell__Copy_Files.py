from cbr_website_beta.utils.remote_shell.CBR__Remote_Shell  import CBR__Remote_Shell
from osbot_aws.aws.s3.S3                                    import S3
from osbot_utils.base_classes.Type_Safe                     import Type_Safe
from osbot_utils.utils.Functions                            import function_source_code

CBR__REMOTE_SHELL__FILE_TRANSFER__S3_BUCKET     = '470426667096--temp-data--eu-west-2'
CBR__REMOTE_SHELL__FILE_TRANSFER__PARENT_FOLDER = 'cbr_lambda_shell__temp_file_transfer'

class CBR__Remote_Shell__Copy_Files(Type_Safe):
    s3_bucket        : str = CBR__REMOTE_SHELL__FILE_TRANSFER__S3_BUCKET
    s3_folder        : str = CBR__REMOTE_SHELL__FILE_TRANSFER__PARENT_FOLDER
    cbr_remote_shell : CBR__Remote_Shell
    s3               : S3

    def create_file__in_s3__from_string(self, file_name, file_contents):
        s3_key = f'{self.s3_folder}/{file_name}'
        self.s3.file_create_from_string(bucket=self.s3_bucket, key=s3_key, file_contents=file_contents)

    def create_python_code__for_function_with_kwargs(self, function, **kwargs):
        function_name = function.__name__
        function_code = function_source_code(function)

        for key, value in kwargs.items():
            function_code = function_code.replace(f'{{{{{key}}}}}', value)

        exec_code = f"{function_code}\nresult= {function_name}()"
        return exec_code

    def execute_function_with_params(self, function, **kwargs):
        python_code = self.create_python_code__for_function_with_kwargs(function, **kwargs)
        return self.cbr_remote_shell.python_exec(python_code)

    #util_methods
    def util__server__file_contents(self, file_name):
        kwargs = { 'file_name': file_name }
        return self.execute_function_with_params(remote_shell__file_contents, **kwargs)

    def util__upload_file__from_string__via_s3(self, file_name, contents):
        self.create_file__in_s3__from_string(file_name, contents)

        kwargs = { 's3_bucket': self.s3_bucket ,
                   's3_folder': self.s3_folder ,
                   'file_name': file_name      }
        return self.execute_function_with_params(remote_shell__s3_download_and_delete, **kwargs)


def remote_shell__sys_modules__list():
    import sys
    module_prefix = "{{module_prefix}}"
    modules = [module for module in sys.modules if module.startswith(module_prefix)]
    return {'modules': modules}

def remote_shell__sys_modules__delete_module():
    module_prefix = "{{module_prefix}}"
    import sys
    if module_prefix:
        to_delete = [module for module in sys.modules if module.startswith(module_prefix)]
        for module in to_delete:
            del sys.modules[module]
    else:
        to_delete = []
    return {'deleted_modules': to_delete}

def remote_shell__file_contents():
    from osbot_utils.utils.Files import file_contents
    file_name = "{{file_name}}"
    file_path = f'/tmp/{file_name}'
    return file_contents(file_path)

def remote_shell__s3_download_and_delete():
    s3_bucket = '{{s3_bucket}}'
    s3_folder = '{{s3_folder}}'
    file_name = '{{file_name}}'

    from osbot_utils.utils.Files import file_delete
    from osbot_aws.aws.s3.S3     import S3
    from osbot_utils.utils.Files import file_exists, file_contents
    s3          = S3()
    s3_key      = f'{s3_folder}/{file_name}'
    target_file = f'/tmp/{file_name}'

    file_delete        (target_file)
    s3.file_download_to(bucket=s3_bucket, key=s3_key, target_file=target_file)
    s3.file_delete     (bucket=s3_bucket, key=s3_key)
    if file_exists(target_file):
        return {'status': 'ok', 'file_contents': file_contents(target_file) }
    else:
        return {'status': 'error', 'message': f'file not found: {target_file}'}

def remote_shell__s3_list_buckets():
    from osbot_aws.aws.s3.S3 import S3
    s3 = S3()
    return  {'buckets': s3.buckets()}
