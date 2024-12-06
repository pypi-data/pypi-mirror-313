from time import sleep

from django.test import override_settings
from django.urls import path

from silica import Component
from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns


TestView = create_test_view(f"""{{% silica '{__name__}.MagicProxy' %}}""")

urlpatterns = silica_urlpatterns + [
    path("proxy", TestView.as_view()),
]


class MagicProxy(Component):
    prop = "hello"
    items = [1,2,3,4]

    def updated_prop(self, value):
        pass

    def inline_template(self):
        return """
            <div x-data>
                Getter: <span x-text="`hello ${$silica.prop}`"></span>
                <button id="update_prop" @click="$silica.prop = 'world'">Set</button>
                prop: {{ prop }}
            </div>
        """


@override_settings(ROOT_URLCONF=__name__)
class MagicProxyTest(SilicaBrowserTestCase):

    def test_magice_silica_proxy(self):
        self.selenium.get(self.live_server_url + '/proxy')

        self.assertHtmlContains('hello hello')
        self.findElementById('update_prop').click()
        sleep(0.3)
        self.assertHtmlContains("prop: world")



