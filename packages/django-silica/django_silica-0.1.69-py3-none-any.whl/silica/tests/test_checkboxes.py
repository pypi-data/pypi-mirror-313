import time
from typing import List, Dict

from django.test import override_settings
from django.urls import path

from selenium.webdriver.common.by import By

from silica import Component
from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns


TestView = create_test_view(f"""{{% silica '{__name__}.CheckboxComponent' %}}""")

urlpatterns = silica_urlpatterns + [
    path("checkboxes", TestView.as_view()),
]


class CheckboxComponent(Component):
    prop1: bool = True
    prop2: int = 1
    prop3 = None
    prop4: str = 'hello'
    prop5: List = ['item1']
    prop6: Dict = {
        'consent': True
    }
    prop7: Dict = {
        'items': ['foo']
    }
    prop8: List = []
    prop9: List = []

    def inline_template(self):
        return """
            <div>
                <p>
                    prop1: {{ prop1 }}
                    <input type="checkbox" silica:model="prop1" id="checkbox1">
                </p>
                
                <p>
                    prop2: {{ prop2 }}
                    <input type="checkbox" silica:model="prop2" id="checkbox2">
                </p>
                
                <p>
                    prop3: {{ prop3 }}            
                    <input type="checkbox" silica:model="prop3" id="checkbox3">
                </p>
                
                <p>
                    prop4: {{ prop4 }}
                    <input type="checkbox" silica:model="prop4" id="checkbox4">
                </p>
                
                <p>
                    prop5: [{% for item in prop5 %}{{ item }}{% endfor %}]
                    <input type="checkbox" silica:model="prop5" id="item1" value="item1">
                    <input type="checkbox" silica:model="prop5" id="another_item" value="another_item">
                </p>     
                
                <p>
                    prop6: [{{ prop6.consent }}]
                    <input type="checkbox" silica:model="prop6.consent" id="checkbox6">
                </p>                
                
                <p>
                    prop7: [{% for item in prop7.items %}{{ item }}{% endfor %}]
                    <input type="checkbox" silica:model="prop7.items" id="foo" value="foo">
                    <input type="checkbox" silica:model="prop7.items" id="bar" value="bar">
                </p>
                
                <p>
                    prop8: [{% for item in prop8.items %}{{ item }}{% endfor %}]
                    <input type="checkbox" silica:model="prop8" id="checkbox8">
                </p>  
                
                <p>
                    prop9: [{% for item in prop9.items %}{{ item }}{% endfor %}]
                    <input type="checkbox" silica:model="prop9" id="checkbox9" value="">
                </p>                
            </div>
        """


@override_settings(ROOT_URLCONF=__name__)
class CheckboxesTestCase(SilicaBrowserTestCase):

    def test_boolean_checkboxes(self):
        self.selenium.get(self.live_server_url + '/checkboxes')

        self.assertTrue("prop1: True" in self.selenium.page_source)
        self.assertTrue("prop2: 1" in self.selenium.page_source)
        self.assertTrue("prop3: None" in self.selenium.page_source)
        self.assertTrue("prop4: hello" in self.selenium.page_source)
        self.assertTrue("prop5: [item1]" in self.selenium.page_source)

        # Checkbox 1
        self.selenium.find_element(By.ID, 'checkbox1').click()
        time.sleep(0.2)
        self.assertTrue("prop1: False" in self.selenium.page_source)

        # Checkbox 2
        self.selenium.find_element(By.ID, 'checkbox2').click()
        time.sleep(0.2)
        self.assertTrue("prop1: False" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'checkbox2').click()
        time.sleep(0.2)
        self.assertTrue("prop2: True" in self.selenium.page_source)

        # Checkbox 3
        self.selenium.find_element(By.ID, 'checkbox3').click()
        time.sleep(0.2)
        self.assertTrue("prop3: True" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'checkbox3').click()
        time.sleep(0.2)
        self.assertTrue("prop3: False" in self.selenium.page_source)

        # Checkbox 4
        self.selenium.find_element(By.ID, 'checkbox4').click()
        time.sleep(0.2)
        self.assertTrue("prop4: False" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'checkbox4').click()
        time.sleep(0.2)
        self.assertTrue("prop4: True" in self.selenium.page_source)

    def test_boolean_checkboxes_in_nested_dictionary(self):
        self.selenium.get(self.live_server_url + '/checkboxes')

        self.assertTrue("prop6: [True]" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'checkbox6').click()
        time.sleep(0.2)
        self.assertTrue("prop6: [False]" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'checkbox6').click()
        time.sleep(0.2)
        self.assertTrue("prop6: [True]" in self.selenium.page_source)

    def test_multi_value_checkboxes(self):
        self.selenium.get(self.live_server_url + '/checkboxes')

        self.assertTrue("prop5: [item1]" in self.selenium.page_source)

        # Checkbox 5
        self.selenium.find_element(By.ID, 'item1').click()
        time.sleep(0.2)
        self.assertTrue("prop5: []" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'another_item').click()
        time.sleep(0.2)
        self.assertTrue("prop5: [another_item]" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'item1').click()
        time.sleep(0.2)
        self.assertTrue("prop5: [another_itemitem1]" in self.selenium.page_source)


    def test_multi_value_checkboxes_in_nested_dictionary(self):
        self.selenium.get(self.live_server_url + '/checkboxes')

        self.assertTrue("prop7: [foo]" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'foo').click()
        time.sleep(0.4)
        self.assertTrue("prop7: []" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'bar').click()
        time.sleep(0.2)
        self.assertTrue("prop7: [bar]" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'foo').click()
        time.sleep(0.2)
        self.assertTrue("prop7: [barfoo]" in self.selenium.page_source)


    def test_we_require_a_value_to_be_set_for_multi_value_checkbox(self):
        self.selenium.get(self.live_server_url + '/checkboxes')

        self.assertTrue("prop8: []" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'checkbox8').click()
        time.sleep(0.2)
        self.assertTrue("prop8: []" in self.selenium.page_source)
        self.assertConsoleLogContains("silica:model for checkbox prop8 is set to an array but the checkbox does not have a valid value attribute")


    def test_we_require_a_valid_value_to_be_set_for_multi_value_checkbox(self):
        self.selenium.get(self.live_server_url + '/checkboxes')

        self.assertTrue("prop9: []" in self.selenium.page_source)

        self.selenium.find_element(By.ID, 'checkbox9').click()
        time.sleep(0.2)
        self.assertTrue("prop9: []" in self.selenium.page_source)
        self.assertConsoleLogContains("silica:model for checkbox prop9 is set to an array but the checkbox does not have a valid value attribute")
