import time

from django.test import override_settings
from django.urls import path

from selenium.webdriver.common.by import By

from silica import Component
from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica.urls import urlpatterns as silica_urlpatterns


## The test components
class ScalarAssignment(Component):
    test_value: str = None

    def inline_template(self):
        # language=HTML
        return """
            <div>
                <button silica:click.prevent="test_value = 1" id="button">Set</button>
                test value: {{ test_value }}
            </div>
        """


## Urls for the test
urlpatterns = silica_urlpatterns + [
    path("silica/tests/scalar-assignment", ScalarAssignment.as_view()),
]


## The test case
@override_settings(ROOT_URLCONF=__name__)
class PropertyExpressionAssignmentTestCase(SilicaBrowserTestCase):

    def test_scalar_assignment_expression(self):
        self.selenium.get(self.live_server_url + '/silica/tests/scalar-assignment')

        self.selenium.find_element(By.ID, 'button').click()

        # Give time for the requests to complete
        time.sleep(1)

        # Assert that test_value is set to 1 in the dom
        self.assertIn('test_value = 1', self.selenium.page_source)
