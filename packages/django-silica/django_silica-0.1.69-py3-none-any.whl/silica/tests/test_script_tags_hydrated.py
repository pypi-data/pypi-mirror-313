import time

from django.test import override_settings
from django.urls import path
from selenium.webdriver.common.by import By

from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica import Component
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns

TestView = create_test_view("""{% silica 'silica.tests.test_script_tags_hydrated.TestComponent' %}""")


urlpatterns = silica_urlpatterns + [
    path("hydrate-scripts", TestView.as_view())
]


class TestComponent(Component):
    show_content = False

    def inline_template(self):
        return """
            <div>
                {% if show_content %}
                    <script>
                        console.log('yoo')
                    </script>
                {% endif %}
                <button silica:click.prevent="show_content = 1" id="button">Show content</button>
            </div>
        """


@override_settings(ROOT_URLCONF=__name__)
class ScriptHydrationTestCase(SilicaBrowserTestCase):
    def test_script_tag_is_hydrated(self):
        self.selenium.get(self.live_server_url + "/hydrate-scripts")

        self.selenium.find_element(By.ID, 'button').click()
        time.sleep(0.2)

        self.assertConsoleLogContains("yoo")




