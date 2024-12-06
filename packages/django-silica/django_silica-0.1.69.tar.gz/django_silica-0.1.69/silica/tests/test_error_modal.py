import logging
import time

from django.test import override_settings
from django.urls import path
from selenium.webdriver.common.by import By

from silica import Component
from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns


class ComponentWithError(Component):    
    def some_function(self):
        raise ValueError('Something went wrong')

    def inline_template(self):
        return """
            <div silica:init="some_function">
            </div>
        """


TestView = create_test_view(f"""
    {{% silica '{__name__}.ComponentWithError' %}}
    """)


urlpatterns = silica_urlpatterns + [
    path("component-with-error/", TestView.as_view()),
]


@override_settings(ROOT_URLCONF=__name__, DEBUG=True)
class ErrorModalBrowserTestCase(SilicaBrowserTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Store the original logging levels
        cls.original_log_levels = {
            'django.request': logging.getLogger('django.request').level,
            'django.server': logging.getLogger('django.server').level,
        }
        # Set logging levels to suppress expected errors
        logging.getLogger('django.request').setLevel(logging.CRITICAL)
        logging.getLogger('django.server').setLevel(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        # Restore original logging levels
        for logger_name, level in cls.original_log_levels.items():
            logging.getLogger(logger_name).setLevel(level)
        super().tearDownClass()

    def test_error_modal_shows_in_development(self):
        with self.settings(DEBUG=True):
            self.selenium.get(self.live_server_url + '/component-with-error')
            time.sleep(0.4)
            self.assertTrue("error-modal" in self.selenium.page_source)
            # self.selenium.save_screenshot('error_modal.png')
            iframe = self.selenium.find_element(By.ID, 'error-content-frame')
            self.selenium.switch_to.frame(iframe)
            self.assertTrue("Something went wrong" in self.selenium.page_source)
            
    def test_error_modal_shows_in_production(self):
        with self.settings(DEBUG=False):
            self.selenium.get(self.live_server_url + '/component-with-error')
            time.sleep(2)
            self.assertTrue("error-modal" in self.selenium.page_source)
            # self.selenium.save_screenshot('error_modal.png')
            iframe = self.selenium.find_element(By.ID, 'error-content-frame')
            self.selenium.switch_to.frame(iframe)
            self.assertTrue("Server Error (500)" in self.selenium.page_source)
                
