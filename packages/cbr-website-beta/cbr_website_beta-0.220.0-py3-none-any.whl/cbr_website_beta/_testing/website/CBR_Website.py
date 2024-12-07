from osbot_playwright.playwright.api.Playwright_Browser import Playwright_Browser
from osbot_playwright.playwright.api.Playwright_Page import Playwright_Page


class CBR_Website(Playwright_Browser):

    def __init__(self, browser, playwright):
        super().__init__()
        self._browser = browser
        self.__playwright = playwright

    def browser(self):
        return self._browser

    def new_page(self, context_index=None):
        page    = self._browser.new_page()
        context = page.context
        return Playwright_Page(context=context, page=page)