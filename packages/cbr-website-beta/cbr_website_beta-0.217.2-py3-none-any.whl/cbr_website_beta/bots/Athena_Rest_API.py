import requests

from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website
from cbr_website_beta.bots.schemas.Log_Entry      import Log_Entry


PATH__ROOT                        = '/'
PATH__DOCS                        = '/docs'
PATH__OPEN_API_JSON               = '/openapi.json'
PATH__CONFIG__VERSION             = '/config/version'
# PATH__CONFIG__CYBER_SECURE_ORG    = '/content/building_a_cybersecure_organisation'
# PATH__CONFIG__CYBER_IN_BOARD      = '/content/cybersecurity_in_the_boardroom'
# PATH__CONFIG__DIGITAL_TRUST       = "/content/importance_of_digital_trust"
# PATH__CONFIG__INCIDENT_MANAGEMENT = '/content/incident_management'
PATH__LOGGING__ADD_LOG_ENTRY      = '/logging/add_log_entry'
PATH__OPENAI__PROMPT_WITH_STREAM  = '/open_ai/prompt_with_system__stream'
PATH__USER__CREATE_USER_SESSION   = '/user/create_user_session'

class Athena_Rest_API:
    # utils
    def athena_url(self):
        athena_path_from_config = server_config__cbr_website.target_athena_url()
        port                    = server_config__cbr_website.cbr_host__port()
        url_from_config         = f'http://localhost:{port}{athena_path_from_config}'    # todo: need a better solution to handle these calls to athena
        return url_from_config

    def requests_get(self, path):
        url = self.athena_url() + path
        response = requests.get(url)
        if response.headers.get('Content-Type') == 'application/json':
            return response.json()
        return response.text

    def requests_post(self, path, data):
        url = self.athena_url() + path
        response = requests.post(url, json=data)
        if response.headers.get('Content-Type') == 'application/json':
            return response.json()
        return response.text
    # methods
    #def athena_prompt   (self): return self.requests_get('/athena_prompt'   )
    #def first_question  (self): return self.requests_get('/first_question'  )
    #def git_repo_status (self): return self.requests_get('/git_repo_status' )
    def open_api        (self): return self.requests_get('/openapi.json'    )
    #def ping            (self): return self.requests_get('/ping'            )
    def root            (self): return self.requests_get('/'                )
    def version         (self): return self.requests_get('/config/version'  )

    # def content__building_a_cyber_secure_organisation(self):
    #     return self.requests_get(PATH__CONFIG__CYBER_SECURE_ORG)

    def open_ai__prompt_with_stream(self, data ):
        return self.requests_post(PATH__OPENAI__PROMPT_WITH_STREAM, data)

    def logging__send_log_entry(self, log_entry: Log_Entry):
        json_data = log_entry.dict()
        return self.requests_post(PATH__LOGGING__ADD_LOG_ENTRY, json_data)

    def user__create_session(self, create_user_session):
        json_data = create_user_session.dict()
        return self.requests_post(PATH__USER__CREATE_USER_SESSION, json_data)