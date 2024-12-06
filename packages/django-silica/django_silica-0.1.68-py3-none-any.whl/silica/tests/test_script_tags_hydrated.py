import time

from selenium.webdriver.common.by import By

from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica import Component


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


class ScriptHydrationTestCase(SilicaBrowserTestCase):
    def test_script_tag_is_hydrated(self):
        self.selenium.get(self.live_server_url + "/silica/tests/script-tags-are-hydrated")

        self.selenium.find_element(By.ID, 'button').click()
        time.sleep(0.2)

        self.assertConsoleLogContains("yoo")




