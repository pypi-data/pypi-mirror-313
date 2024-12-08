from os import environ

from osbot_utils.base_classes.Type_Safe import Type_Safe

ENV_VARS_TO_REPLACE = ['OPEN_AI__API_KEY', 'OPENAI_API_KEY', 'OPEN_ROUTER_API_KEY', 'OPENROUTER_API_KEY',  # todo: fix this duplicate use
                       'GROQ_API_KEY', 'TOGETHER_AI_API_KEY', 'MISTRAL_API_KEY', 'SAMBANOVA_API_KEY', 'IP_DATA__API_KEY' ,
                       'PINECONE_API_KEY' 'COGNITO_USER_POOL_ID' , 'COGNITO_CLIENT_ID', 'COGNITO_USER_PWD_1',
                       'BROWSERLESS__API_KEY' , 'NGROK__AUTH_TOKEN' , 'CODI_API_KEY' , 'APPLITOOLS_API_KEY' ,
                       'BROWSER_STACK_USER_NAME', 'BROWSER_STACK_ACCESS_KEY' ,
                       'LAMBDA_SHELL__AUTH_KEY',
                       'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY','AWS_SESSION_TOKEN',
                       'DEPLOY__AWS_ACCESS_KEY_ID', 'DEPLOY__AWS_SECRET_ACCESS_KEY']        # todo: find a way to pick up vars that shouldn't be here, ideally this should be using a allow-list instead of an deny-list

ENV_VARS_REPLACE_VALUE = "*****"

class Env_Vars__With_No_Secrets(Type_Safe):
    extra_vars_to_replace: list
    replace_value        : str = ENV_VARS_REPLACE_VALUE

    def raw_env_vars(self):
        return dict(environ)

    def create(self):
        fixed_env_vars = self.raw_env_vars()
        target_var_names = self.env_vars_to_replace() +  self.extra_vars_to_replace
        for var_name in target_var_names:
            if var_name in fixed_env_vars:
                fixed_env_vars[var_name] = self.replace_value
        return fixed_env_vars

    def env_vars_to_replace(self):
        return ENV_VARS_TO_REPLACE