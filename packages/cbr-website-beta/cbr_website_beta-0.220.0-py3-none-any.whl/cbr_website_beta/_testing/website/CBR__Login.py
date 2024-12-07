from os import environ
from urllib.parse import urljoin

from cbr_website_beta._testing.test_utils.TestCase__CBR__Website import TestCase__CBR__Website
from cbr_website_beta._testing.website.CBR__Pages import CBR__Pages


class CBR__Login(TestCase__CBR__Website):

    def setUp(self):
        super().setUp()
        self.cognito_host  = 'https://the-cbr-beta.auth.eu-west-2.amazoncognito.com'
        self.cbr_pages     = CBR__Pages    ()
        #self.cbr_api_pages = CBR__API_Pages()
        self.cbr_pages    .page        = self.page
        #self.cbr_api_pages.page        = self.page
        self.cbr_pages    .target_host = self.target_host
        #self.cbr_api_pages.target_host = self.target_host


    def login__using_javascript(self, username, password):
        self.open_login_page()
        if self.html().tags__attrs('input', index_by='name').get('signInSubmitButton'):
            js_code = f"""const usernames = document.querySelectorAll('input#signInFormUsername');
                         const passwords = document.querySelectorAll('input#signInFormPassword');

                         usernames[1].value='{username}';
                         passwords[1].value='{password}';
                         const usernameField = usernames[1];
                         usernameField.closest('form').submit();
                        """
            self.page.page.evaluate(js_code)

    def open_login_page(self):
        if self.page.info().get('url').get('path') != '/login':
            self.cbr_pages.login()
        hrefs = self.html().hrefs(index_by='text')
        if 'Sign in as a different user?' in hrefs:
            path_logout = hrefs.get('Sign in as a different user?').get('href')
            url_logout = urljoin(self.cognito_host, path_logout)
            self.open(url_logout)
        return self.html()

    def credentials__test_user_1(self):
        username = environ.get('COGNITO_USER_NAME_1')
        password = environ.get('COGNITO_USER_PWD_1')
        return username, password