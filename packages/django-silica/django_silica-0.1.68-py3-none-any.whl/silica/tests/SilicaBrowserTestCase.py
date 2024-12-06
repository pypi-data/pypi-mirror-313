from urllib.parse import urlparse, parse_qs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from django.test import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from silica.tests.urls import urlpatterns as silica_test_url_patterns
from silica.urls import urlpatterns as silica_urlpatterns

urlpatterns = silica_urlpatterns + silica_test_url_patterns


@override_settings(ROOT_URLCONF=__name__)
class SilicaBrowserTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        CHROME_PATH = '/usr/bin/chromium'
        CHROMEDRIVER_PATH = '/usr/bin/chromedriver'

        options = Options()

        # Basic required options
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Connection stability improvements
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-features=NetworkService')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--force-device-scale-factor=1')

        # Memory & process management
        options.add_argument('--single-process')  # Important for connection stability
        options.add_argument('--disable-breakpad')
        options.add_argument('--disable-extensions')

        # Browser window settings
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--start-maximized')

        # Logging
        options.add_argument('--log-level=3')  # FATAL only
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

        # Additional stability settings
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-site-isolation-trials')

        options.binary_location = CHROME_PATH

        service = Service(
            CHROMEDRIVER_PATH,
            service_args=['--verbose']
        )

        cls.selenium = webdriver.Chrome(options=options, service=service)
        cls.selenium.set_page_load_timeout(10)


    def get_query_param(self, param):
        url = self.selenium.current_url
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get(param, [None])[0]

    def get_url(self):
        return self.selenium.current_url

    def get_page_source(self):
        return self.selenium.page_source

    def get_console_log(self):
        return self.selenium.get_log('browser')

    def assertConsoleLogContains(self, text):
        logs = self.get_console_log()
        for log in logs:
            if text in log['message']:
                return self.assertTrue(True)
        return self.assertTrue(False, f'"{text}" is not seen in the console logs: {logs}')

    def assertHtmlContains(self, text):
        assert text in self.selenium.page_source, f'"{text}" is not seen in the page source'
        return self

    def assertHtmlNotContains(self, text):
        assert text not in self.selenium.page_source, f'"{text}" is seen in the page source'
        return self

    def findElementById(self, element_id):
        return self.selenium.find_element(By.ID, element_id)

    def assertElementIsVisible(self, element):
        self.assertTrue(element.is_displayed())
        return self

    def assertIdIsVisible(self, element_id):
        element = self.findElementById(element_id)
        self.assertTrue(element.is_displayed())
        return self

    def assertIdIsNotVisible(self, element_id):
        element = self.findElementById(element_id)
        self.assertFalse(element.is_displayed())
        return self

    def assertSee(self, text):
        page_text = self.selenium.find_element(By.TAG_NAME, 'body').text
        self.assertIn(text, page_text, f"'{text}' was not found in the visible rendered content")
        return self

    def assertDontSee(self, text):
        page_text = self.selenium.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn(text, page_text, f"'{text}' was found in the visible rendered content, but it shouldn't be there")
        return self

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
        pass
