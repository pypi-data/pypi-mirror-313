import cbr_content

import cbr_web_components
import cbr_website_beta
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Files            import file_contents, path_combine

class Version(Type_Safe):

    FILE_NAME_VERSION = 'version'

    def path_code_root(self):
        return cbr_website_beta.path

    def path_version_file(self):
        return path_combine(self.path_code_root(), self.FILE_NAME_VERSION)

    def value(self):
        value = file_contents(self.path_version_file()) or ""
        return value.strip()

    def version__cbr_content(self):                     # todo: add a generic module to get the version files from specific modules
        version_file = path_combine(cbr_content.path, 'version')
        return file_contents(version_file).strip()

    def version__cbr_web_components(self):
        version_file = path_combine(cbr_web_components.path,  'version')
        return file_contents(version_file).strip()

version = Version().value()     # todo: replace use of this method with the version__cbr_website

version__cbr_website        = Version().value()
version__cbr_content        = Version().version__cbr_content()
version__cbr_web_components = Version().version__cbr_web_components()