import time
from typing import Dict

from django.test import override_settings
from django.urls import path

from selenium.webdriver.common.by import By

from silica import Component
from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns

TestView = create_test_view(f"""{{% silica '{__name__}.DictionaryModelComponent' %}}""")

urlpatterns = silica_urlpatterns + [
    path("dict-models", TestView.as_view()),
]


class DictionaryModelComponent(Component):
    my_object: Dict = {}
    another = {
        'key1': 'value1',
    }
    nesting = {
        'key1': {
            'key2': 'value2',
        }
    }
    form = {
        'consent': False
    }

    def inline_template(self):
        return """
            <div>
                <p>
                    not permitted: '{{ my_object.doesnt_exist }}'
                    <input type="input" silica:model="my_object.doesnt_exist" id="ex1">
                </p>
                
                <p>
                    simple: '{{ another.key1 }}'
                    <input type="input" silica:model="another.key1" id="ex2">
                </p>
                
                <p>
                    2 levels: '{{ nesting.key1.key2 }}'            
                    <input type="input" silica:model="nesting.key1.key2" id="ex3">
                </p>
                
                <p>
                    checkbox consent: '{{ form.consent }}'
                    <input type="checkbox" silica:model="form.consent" id="ex4">
                </p>          
            </div>
        """


@override_settings(ROOT_URLCONF=__name__)
class DictionaryModelsTestCase(SilicaBrowserTestCase):

    def test_new_property_keys_cant_be_added(self):
        self.selenium.get(self.live_server_url + '/dict-models')

        self.assertTrue("not permitted: ''" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'ex1').send_keys('n')
        time.sleep(0.5)

        self.assertTrue("not permitted: 'new'" not in self.selenium.page_source)
        self.assertConsoleLogContains('the server responded with a status of 422 (Unprocessable Entity)')

    def test_dictionaries_key_binding(self):
        self.selenium.get(self.live_server_url + '/dict-models')

        self.assertTrue("simple: 'value1'" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'ex2').send_keys('n')
        self.selenium.find_element(By.ID, 'ex2').send_keys('e')
        self.selenium.find_element(By.ID, 'ex2').send_keys('w')
        time.sleep(0.5)
        self.assertTrue("simple: 'value1new'" in self.selenium.page_source)

    def test_dictionary_keys_2_levels_deep(self):
        self.selenium.get(self.live_server_url + '/dict-models')

        self.assertTrue("2 levels: 'value2'" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'ex3').send_keys('h')
        self.selenium.find_element(By.ID, 'ex3').send_keys('e')
        self.selenium.find_element(By.ID, 'ex3').send_keys('y')
        time.sleep(0.5)
        self.assertTrue("2 levels: 'value2hey'" in self.selenium.page_source)

    def test_checkbox_model_on_nested(self):
        self.selenium.get(self.live_server_url + '/dict-models')

        self.assertTrue("checkbox consent: 'False'" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'ex4').click()
        time.sleep(0.5)
        self.assertTrue("checkbox consent: 'True'" in self.selenium.page_source)
