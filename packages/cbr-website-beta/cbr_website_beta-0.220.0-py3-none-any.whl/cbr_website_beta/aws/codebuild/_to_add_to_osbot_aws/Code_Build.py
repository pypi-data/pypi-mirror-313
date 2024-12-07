from osbot_aws.apis.CodeBuild import CodeBuild
from osbot_aws.apis.Session import Session
from osbot_utils.decorators.methods.cache_on_self import cache_on_self


class Code_Build(CodeBuild):

    def __init__(self, project_name=None, role_name=None):
        super().__init__(project_name, role_name)

    @cache_on_self
    def client(self):
        return Session().client('codebuild')

    def project_info(self):
        response = self.client().batch_get_projects(names=[self.project_name])
        if response['projects']:
            return response['projects'][0]  # Return details of the first project (should only be one)
        else:
            return "Project not found"