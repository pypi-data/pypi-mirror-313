import time

from django.test import override_settings
from django.urls import path

from silica import Component
from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns


TestView = create_test_view(f"""{{% silica '{__name__}.SilicaInitComponent' %}}""")

urlpatterns = silica_urlpatterns + [
    path("silica-init", TestView.as_view()),
]


class SilicaInitComponent(Component):
    instant_data = "I'm instant"
    mounted_data: str = None
    init_data: str = ''

    def mount(self):
        self.mounted_data = "I'm from mounted"

    def slow_method(self):
        time.sleep(0.4)
        self.init_data = "I'm from an init method"

    def inline_template(self):
        return """
            <div silica:init="slow_method">
                <style>.red { color: red }</style>
                <style>.hidden { display: none }</style>
            
                {{ instant_data }}
                {{ mounted_data }}
                {{ init_data }}       

                <div id="loading-message" silica:loading>I am loading no matter what mate</div>
                <div id="initiating-message" silica:loading.init>I am an initiating message</div>    
                <div id="proceeding-message" silica:loading.proceeding>I am a proceeding message</div>
                <div id="class-message" silica:loading.class="red">I am red whilst loading</div>
                
                <div id="loading-hidden" silica:loading.hidden>I am hidden whilst loading</div> 
                <div id="initiating-hidden" silica:loading.init.hidden>I am hidden whilst initiating</div> 
            </div>
        """


@override_settings(ROOT_URLCONF=__name__)
class SilicaInitTestCase(SilicaBrowserTestCase):

    def test_init_functionality(self):
        self.selenium.get(self.live_server_url + '/silica-init')

        self.assertHtmlContains("I'm instant")
        self.assertHtmlContains("I'm from mounted")
        self.assertHtmlNotContains("I'm from an init method")

        time.sleep(0.5)

        self.assertHtmlContains("I'm from an init method")

    def test_initiating_loader(self):
        self.selenium.get(self.live_server_url + '/silica-init')

        self.assertIdIsVisible('loading-message')
        self.assertIdIsVisible('initiating-message')
        self.assertIdIsVisible('class-message')
        self.assertHtmlContains(' class="red"')
        self.assertIdIsNotVisible('proceeding-message')

        time.sleep(0.5)

        self.assertIdIsNotVisible('loading-message')
        self.assertIdIsNotVisible('initiating-message')
        self.assertIdIsVisible('class-message')
        self.assertHtmlNotContains(' class="red"')
        
    


