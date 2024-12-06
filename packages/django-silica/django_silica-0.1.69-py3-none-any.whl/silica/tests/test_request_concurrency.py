import time

from django.test import override_settings
from django.urls import path
from selenium.webdriver.common.by import By

from silica import Component
from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns

TestView = create_test_view(f"""{{% silica '{__name__}.ConcurrencyTest' %}}""")

urlpatterns = silica_urlpatterns + [
    path("concurrency", TestView.as_view()),
]


class ConcurrencyTest(Component):
    ui_value: str = None

    def slow_first(self):
        time.sleep(2)
        self.ui_value = "data_from_request_1"

    def slow_second(self):
        time.sleep(1)
        self.ui_value = "data_from_request_2"

    def inline_template(self):
        return """
            <div>
                <button id="slow_request_first" silica:click.prevent="slow_first">Slow</button>
                <button id="quick_request_second" silica:click.prevent="slow_second">Quick</button>
                <div id="updated_element">{{ ui_value }}</div>
            </div>
        """


@override_settings(ROOT_URLCONF=__name__)
class ConcurrencyTestCase(SilicaBrowserTestCase):

    def test_a_slower_earlier_request_doesnt_overwrite_a_later_quicker_request(self):
        # Navigate to the page
        self.selenium.get(self.live_server_url + '/concurrency')

        # Trigger the first request
        self.selenium.find_element(By.ID, 'slow_request_first').click()

        # Without waiting, trigger the second request
        self.selenium.find_element(By.ID, 'quick_request_second').click()

        # Give time for the requests to complete
        time.sleep(3)

        # Wait for a UI element that gets updated by the responses
        updated_element = self.selenium.find_element(By.ID, 'updated_element')

        # Check that the updated_element contains data from the 2nd request ONLY.
        self.assertNotIn('data_from_request_1', updated_element.text)
        self.assertIn('data_from_request_2', updated_element.text)
