import time

from django.test import override_settings
from django.urls import path

from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns

from selenium.webdriver.common.by import By

from silica import Component


TestView = create_test_view("""{% silica 'silica.tests.test_magic_methods.MagicMethods' %}""")


urlpatterns = silica_urlpatterns + [
    path("magic-methods", TestView.as_view()),
]

class MagicMethods(Component):
    property = "foo"

    def call_me(self):
        self.property = "boo"

    def call_me_with_arg(self, value):
        self.property = value

    def call_me_with_args(self, value1, value2):
        self.property = value1 + value2

    def inline_template(self):
        return """
            <div x-data>
                property: {{ property }}
                <button @click.prevent="$set('property', 'bar')" id="click_set">Set</button>
                <button @click.prevent="$call('call_me')" id="click_call">Call</button>
                <button @click.prevent="$call('call_me_with_arg', 'ding')" id="click_call_with_arg">Call</button>
                <button @click.prevent="$call('call_me_with_args', 'dong', 'merrily')" id="click_call_with_args">Call</button>
            </div>
        """


@override_settings(ROOT_URLCONF=__name__)
class MagicMethodsBrowserTestCase(SilicaBrowserTestCase):
    def test_magic_set(self):
        self.selenium.get(self.live_server_url + "/magic-methods")

        self.assertTrue("property: foo" in self.get_page_source())

        self.selenium.find_element(By.ID, 'click_set').click()

        time.sleep(0.2)

        self.assertTrue("property: bar" in self.get_page_source())

    def test_magic_call(self):
        self.selenium.get(self.live_server_url + "/magic-methods")

        self.assertTrue("property: foo" in self.get_page_source())

        self.selenium.find_element(By.ID, 'click_call').click()

        time.sleep(0.2)

        self.assertTrue("property: boo" in self.get_page_source())

    def tmp_test_magic_call_with_arg(self):
        pass
        self.selenium.get(self.live_server_url + "/magic-methods")

        self.assertTrue("property: foo" in self.get_page_source())

        self.selenium.find_element(By.ID, 'click_call_with_arg').click()

        time.sleep(0.2)

        self.assertTrue("property: ding" in self.get_page_source())

    def tmp_test_magic_call_with_args(self):
        pass
        self.selenium.get(self.live_server_url + "/magic-methods")

        self.assertTrue("property: foo" in self.get_page_source())

        self.selenium.find_element(By.ID, 'click_call_with_arg').click()

        time.sleep(0.2)

        self.assertTrue("property: ding" in self.get_page_source())
