from unittest                                           import TestCase
from urllib.parse                                       import urljoin
from playwright.sync_api                                import PlaywrightContextManager, sync_playwright, Browser
from cbr_website_beta._testing.website.CBR_Website      import CBR_Website
from cbr_website_beta.apps.home.home_routes import COGNITO_SIGN_IN
from osbot_playwright.playwright.api.Playwright_Page    import Playwright_Page

from osbot_utils.utils.Env import load_dotenv
from osbot_utils.utils.Files                            import folder_create, path_combine, files_list, files_names
from osbot_utils.utils.Json                             import to_json_str, from_json_str
from osbot_utils.utils.Str                              import str_safe
from tests.integration.test_integration_tests import DEFAULT_TESTCASE__CBR_WEBSITE_TARGET, skip_if_dev_server_offline

DEFAULT_SCREENSHOTS_FOLDER           = '/tmp/cbr_screenshots'

class TestCase__CBR__Website(TestCase):
    context_manager   : PlaywrightContextManager
    playwright        : sync_playwright
    browser           : Browser
    tcb_website       : CBR_Website
    page              : Playwright_Page
    target_host       : str
    folder_screenshots: str


    @classmethod
    @skip_if_dev_server_offline
    def setUpClass(cls):
        load_dotenv()
        cls.target_host        = DEFAULT_TESTCASE__CBR_WEBSITE_TARGET
        cls.folder_screenshots = DEFAULT_SCREENSHOTS_FOLDER
        folder_create(cls.folder_screenshots )
        cls.browser_create()

    @classmethod
    def tearDownClass(cls):
        cls.context_manager.__exit__()

    def setUp(self):
        self.capture_screenshots = True

    def tearDown(self):
        if self.capture_screenshots:
            file_name = self._testMethodName.replace('test_', '')
            self.screenshot(file_name)

    @classmethod
    def browser_create(cls):
        cls.context_manager = sync_playwright()
        cls.playwright      = cls.context_manager.start()
        cls.browser         = cls.playwright.chromium.launch(headless=True)
        cls.tcb_website     = CBR_Website(cls.browser, cls.playwright)
        cls.page            = cls.tcb_website.new_page()

    @classmethod
    def browser_close(cls):
        cls.context_manager.__exit__()

    def browser_recreate(self):
        self.browser_close()
        self.browser_create()

    def cognito__url__signin(self):
        return COGNITO_SIGN_IN.format(cbr_domain=self.target_host)

    def html(self):
        return self.page.html()

    def open(self,path=''):
        url = urljoin(self.target_host, path)
        self.page.open(url)
        return self.html()

    def open_json(self,path=''):
        url = urljoin(self.target_host, path)
        self.page.open(url)
        text = self.page.html().text()
        return from_json_str(text)

    def screenshot(self,file_name=None):
        if not file_name:
            file_name = 'screenshot'
        file_name = str_safe(file_name) + '.png'
        screenshot_path = path_combine(self.folder_screenshots,file_name)
        return self.page.screenshot(path=screenshot_path)

    def url(self):
        return self.page.url()