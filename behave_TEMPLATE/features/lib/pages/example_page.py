from selenium.webdriver.common.by import By

from features.lib.pages.BasePage import BasePage


class CustomerShopLocator(BasePage):

    def __init__(self, context):

        BasePage.__init__(
            self,
            context.driver,
            base_url='https://www.somewebsite.com')

    locator_dictionary = {
        "someElementName": (By.CSS_SELECTOR, 'some_css_selector')
    }