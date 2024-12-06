import time

from django.test import override_settings
from django.urls import path
from selenium.webdriver.common.by import By

from silica import Component
from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns


TestView = create_test_view(f"""{{% silica '{__name__}.SilicaLoadingTargetExceptComponent' %}}""")

urlpatterns = silica_urlpatterns + [
    path("silica-loading-target-except", TestView.as_view()),
]


class SilicaLoadingTargetExceptComponent(Component):
    def specific_call(self):
        time.sleep(0.4)

    def generic_call(self):
        time.sleep(0.4)

    def inline_template(self):
        return """
            <div>
                <div silica:loading silica:target.except="generic_call">
                    I'm specific loading
                </div>
                
                <div silica:loading>
                    I'm generic loading
                </div>
                
                <button id="generic_call" silica:click="generic_call">Click me</button>
            </div>
        """


@override_settings(ROOT_URLCONF=__name__)
class SilicaInitTestCase(SilicaBrowserTestCase):
    def test_target_except_modifier(self):
        self.selenium.get(self.live_server_url + '/silica-loading-target-except')

        self.assertDontSee("I'm specific loading")
        self.assertDontSee("I'm generic loading")

        self.selenium.find_element(By.ID, 'generic_call').click()
        time.sleep(0.1)
        
        self.assertDontSee("I'm specific loading")
        self.assertSee("I'm generic loading")

