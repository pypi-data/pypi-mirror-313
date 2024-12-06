import time

from django.test import override_settings
from django.urls import path

from selenium.webdriver.common.by import By

from silica import Component
from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns


TestView = create_test_view(f"""{{% silica '{__name__}.DebounceComponent' %}}""")

urlpatterns = silica_urlpatterns + [
    path("debounce", TestView.as_view()),
]


class DebounceComponent(Component):
    text = ''
    updated_count = 0
    
    def updated_text(self, value):
        self.text = value
        self.updated_count += 1
        
    def change_text(self):
        self.text = 'changed'

    def inline_template(self):
        return """
            <div>
                default: "{{ text }}"
                custom 600ms: "{{ text }}"
                <input type="text" id="text" silica:model.debounce="text">              
                <input type="text" id="text_600" silica:model.debounce.600ms="text">
                <button id="change_text_btn" silica:click="change_text">Change text</button>              
            </div>
        """


@override_settings(ROOT_URLCONF=__name__)
class DebounceTestCase(SilicaBrowserTestCase):

    def test_that_debounce_is_delaying_send(self):
        self.selenium.get(self.live_server_url + '/debounce')
        
        element = self.selenium.find_element(By.ID, 'text')
        element.send_keys('a')
        
        time.sleep(0.2)
        
        self.assertHtmlContains('default: ""')

    def test_that_debounce_resolves_after_default_timeout_of_300ms(self):
        self.selenium.get(self.live_server_url + '/debounce')
        
        element = self.selenium.find_element(By.ID, 'text')
        element.send_keys('a')
        
        time.sleep(0.4)
        
        self.assertHtmlContains('default: "a"')

    def test_that_debounce_waits_for_a_custom_timeout(self):
        self.selenium.get(self.live_server_url + '/debounce')
        
        element = self.selenium.find_element(By.ID, 'text_600')
        element.send_keys('b')
        
        time.sleep(0.4)
        
        self.assertHtmlNotContains('custom 600ms: "b"')

    def test_that_debounce_resolves_after_a_custom_timeout(self):
        self.selenium.get(self.live_server_url + '/debounce')
        
        element = self.selenium.find_element(By.ID, 'text_600')
        element.send_keys('b')
        
        time.sleep(0.65)
        
        self.assertHtmlContains('custom 600ms: "b"')
        
    def test_that_inputs_with_debounce_modifier_are_updated_from_backend_update(self):
        self.selenium.get(self.live_server_url + '/debounce')
        
        btn = self.selenium.find_element(By.ID, 'change_text_btn')
        btn.click()
        
        time.sleep(0.2)
        
        input = self.selenium.find_element(By.ID, 'text')
        self.assertEqual(input.get_attribute('value'), 'changed')
        self.assertHtmlContains('default: "changed"')
        
  