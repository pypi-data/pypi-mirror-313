from cbr_website_beta.aws.codebuild._to_add_to_osbot_aws.Code_Build import Code_Build

CODE_BUILD_PROJECT_NAME = 'CBR_Website__Tests__Unit'

class CBR_Code_Build:

    def __init__(self):
        self.project_name = CODE_BUILD_PROJECT_NAME
        self.role_name    = ''
        self.code_build = Code_Build(project_name=self.project_name)

    def build_ids(self):
        return self.code_build.all_builds_ids(use_paginator=True)

    def project_info(self):
        return self.code_build.project_info()

    def start_build(self):
        return self.code_build.build_start()