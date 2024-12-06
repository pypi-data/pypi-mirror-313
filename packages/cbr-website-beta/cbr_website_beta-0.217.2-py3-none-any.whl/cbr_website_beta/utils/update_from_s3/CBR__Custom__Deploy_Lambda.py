import logging
from os import environ

from osbot_utils.utils.Env import get_env

from cbr_website_beta.utils.Version                 import version__cbr_website
from osbot_aws.deploy.Deploy_Lambda                 import Deploy_Lambda
from osbot_utils.base_classes.Type_Safe             import Type_Safe
from osbot_aws.AWS_Config                           import  aws_config
from osbot_aws.aws.lambda_.Lambda                   import Lambda
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.utils.Dev                          import pprint
from osbot_utils.utils.Http                         import wait_for_http, GET
from osbot_utils.utils.Misc                         import random_id, date_time_now

from cbr_website_beta.utils.update_from_s3.Release_Package__via__S3 import Release_Package__via__S3

ENV_VAR_NAME__CBR__CUSTOM__ACCOUNT_ID       = 'CBR__CUSTOM__ACCOUNT_ID'
ENV_VAR_NAME__CBR__CUSTOM__TARGET_REGION    = 'CBR__CUSTOM__TARGET_REGION '
ENV_VAR_NAME__CBR__CUSTOM__S3_BUCKET_NAME   = 'S3_DEV__BUCKET'
ENV_VAR_NAME__CBR__CUSTOM__S3_FOLDER        = 'S3_DEV__PARENT_FOLDER'
ENV_VAR_NAME__CBR__CUSTOM__VERSION_FILE     = 'CBR__CUSTOM__VERSION_FILE'
ENV_VAR_NAME__CBR__CUSTOM__LAMBDA_NAME      = 'CBR__CUSTOM__LAMBDA_NAME'
CBR__CONFIG_FILE                             = 'cbr-website.community.toml'
CBR__CONFIG_FILE__LAMBDA_DEPLOYMENT          = 'cbr-website.community-cbr-hosted.toml'
#DOCKER_HUB__VERSION__CBR_WEBSITE_BETA       = 'v0.126.57'
DOCKER_HUB__VERSION__CBR_WEBSITE_BETA       = version__cbr_website
DOCKER_HUB__IMAGE_URI__CBR_WEBSITE_BETA     = f'654654216424.dkr.ecr.eu-west-1.amazonaws.com/cbr-website-beta_lambda:{DOCKER_HUB__VERSION__CBR_WEBSITE_BETA}'

class CBR__Custom__Deploy_Lambda(Type_Safe):

    @cache_on_self
    def deploy_lambda(self):
        if self.setup_not_ok():
            return None
        lambda_name = self.lambda_name()
        return Deploy_Lambda(lambda_name)

    def cbr_custom__create_lambda(self):
        if self.setup_not_ok():
            return False

        deploy_lambda = self.deploy_lambda()
        if deploy_lambda.exists() is False:
            image_uri    = self.docker_image_uri()
            deploy_lambda.set_container_image(image_uri)
            #deploy_lambda.set_env_variable('PORT', '3000')
            result      = deploy_lambda.lambda_function().create()
            if result.get('status') == 'ok':
                print(f" ... Created Lambda function: {self.lambda_name()}")
                deploy_lambda.lambda_function().function_url_create_with_public_access(invoke_mode="RESPONSE_STREAM")
            else:
                pprint(result)
                raise Exception(f"failed to create lambda")
        else:
            print(f" ... Lambda already exists: {self.lambda_name()}")
            version = version__cbr_website
            if version.endswith('.0'):  # only update the image if the version is a release version
                print(" ... updating lambda image")
                try:
                    image_uri = f'654654216424.dkr.ecr.eu-west-1.amazonaws.com/cbr-website-beta_lambda:{version}'
                    deploy_lambda.set_container_image(image_uri)
                    deploy_lambda.lambda_function().update_lambda_code()
                    print(" ... waiting for lambda update to complete")
                    deploy_lambda.lambda_function().wait_for_function_update_to_complete()
                except Exception as error:
                    print(f"Error inside update lambda image: {error}")
            else:
                print(" ... not a .0 version, skipping image update")
            print(" ... all done")
        return True




    def update_lambda__to__version(self):
        # account_id      = environ.get(ENV_VAR_NAME__CBR__CUSTOM__ACCOUNT_ID    , '470426667096'                                           )
        # target_region   = environ.get(ENV_VAR_NAME__CBR__CUSTOM__TARGET_REGION , 'eu-west-1'                                              )
        # s3_bucket_name  = environ.get(ENV_VAR_NAME__CBR__CUSTOM__S3_BUCKET_NAME, '470426667096--temp-data--eu-west-2'                     )
        # s3_folder       = environ.get(ENV_VAR_NAME__CBR__CUSTOM__S3_FOLDER     , 'cbr_lambda_shell__temp_file_transfer/cbr_website_beta/' )
        # version_file    = environ.get(ENV_VAR_NAME__CBR__CUSTOM__VERSION_FILE  ) # 'custom-version.zip'
        # lambda_name     = environ.get(ENV_VAR_NAME__CBR__CUSTOM__LAMBDA_NAME   ) # 'cbr_website_beta__custom__dev'

        print("===== Updating lambda to version ====")
        print(f"    account_id     : {self.account_id     () }")
        print(f"    target_region  : {self.target_region  () }")
        print(f"    s3_bucket_name : {self.s3_bucket_name () }")
        print(f"    s3_folder      : {self.s3_folder      () }")
        print(f"    version_file   : {self.version_file   () }")
        print(f"    lambda_name    : {self.lambda_name    () }")
        print(f"    cbr_config_file: {self.cbr_config_file() }")

        if self.setup_ok() is False:
            print("... stopping install ... missing environment variables")
            return
        print("... all good, starting install ...")
        self.cbr_custom__create_lambda()
        self.cbr_custom__configure_lambda(self.lambda_name())

    def cbr_config_file(self):
        return get_env('CBR__CONFIG_FILE', CBR__CONFIG_FILE)

    def cbr_custom__configure_lambda(self, server_name):
        if self.setup_not_ok():
            return False
        print("    .configuring lambda environment variables")
        aws_lambda = Lambda(self.lambda_name())
        env_variables = { 'AWS_LWA_INVOKE_MODE'  : 'response_stream'                  ,
                          'AWS_ACCOUNT_ID'       : self.account_id()                  ,
                          'CBR__CONFIG_FILE'     : self.cbr_config_file()             ,
                          'CBR__SERVER_NAME'     : server_name                        ,
                          'CBR_UPDATE_AT'        : date_time_now()                    ,
                          'EXECUTION_ENV'        : 'DEV'                              ,
                          'IP_DATA__API_KEY'     : environ.get('IP_DATA__API_KEY', ''),
                          'PORT'                 : '3000'                             ,
                          'S3_DEV__BUCKET'       : self.s3_bucket_name()              ,
                          'S3_DEV__PARENT_FOLDER': self.s3_folder()                   ,
                          'S3_DEV__VERSION'      : self.version_file()                }

        aws_lambda.set_env_variables(env_variables)
        aws_lambda.update_lambda_configuration()

        logging.info(f"Waiting for lambda update to complete")
        aws_lambda.wait_for_function_update_to_complete()
        logging.info(f"Waiting for lambda update to complete")
        aws_lambda.wait_for_state_active()
        function_url = aws_lambda.function_url()
        pprint(f"update all done, try it out at {function_url}web/home")

        logging.info(f"Waiting for the website to be available")
        url_version = f"{function_url}web/version"
        print(url_version)
        wait_for_http(url_version, wait_for=1)
        pprint(f"Version from live site: {GET(url_version)}")
        return True

    def setup_ok(self):
        if   not self.account_id     (): print("missing account_id"     )
        elif not self.target_region  (): print("missing target_region"  )
        elif not self.s3_bucket_name (): print("missing s3_bucket_name" )
        elif not self.s3_folder      (): print("missing s3_folder"      )
        elif not self.version_file   (): print("missing version_file"   )
        elif not  self.lambda_name   (): print("missing lambda_name"    )
        else:
            aws_config.set_aws_session_region_name(self.target_region())
            return True

        return False

    def setup_not_ok(self):
        return self.setup_ok() is False

    def account_id      (self): return environ.get(ENV_VAR_NAME__CBR__CUSTOM__ACCOUNT_ID      , '470426667096'                                          )
    def target_region   (self): return environ.get(ENV_VAR_NAME__CBR__CUSTOM__TARGET_REGION   , 'eu-west-1'                                             )
    def s3_bucket_name  (self): return environ.get(ENV_VAR_NAME__CBR__CUSTOM__S3_BUCKET_NAME  , '470426667096--temp-data--eu-west-2'                    )
    def s3_folder       (self): return environ.get(ENV_VAR_NAME__CBR__CUSTOM__S3_FOLDER       , 'cbr_lambda_shell__temp_file_transfer/cbr_website_beta/')
    def version_file    (self): return environ.get(ENV_VAR_NAME__CBR__CUSTOM__VERSION_FILE    )  # 'custom-version.zip'
    def lambda_name     (self): return environ.get(ENV_VAR_NAME__CBR__CUSTOM__LAMBDA_NAME     )  # 'cbr_website_beta__custom__dev'
    def docker_image_uri(self): return DOCKER_HUB__IMAGE_URI__CBR_WEBSITE_BETA


if __name__ == "__main__":
    CBR__Custom__Deploy_Lambda().update_lambda__to__version()