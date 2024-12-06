import time

from django.test import override_settings
from django.urls import path

from silica import Component
from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns


TestView = create_test_view(f"""{{% silica '{__name__}.MorphTestComponent' %}}""")

urlpatterns = silica_urlpatterns + [
    path("morph", TestView.as_view()),
]


class MorphTestComponent(Component):
    something = "hello"
    items = [1,2,3,4]

    def update_something(self):
        self.something = "world"

    def inline_template(self):
        return """
            <div>
                {{ something }}
                <div x-data="{'expanded': false}">
                    {% for item in items %}
                        <div id="item_{{ item }}" x-show="{% if forloop.counter > 2 %}expanded{% else %}true{% endif %}">
                            item: "{{ item }}"
                        </div>
                    {% endfor %}

                    <button @click="expanded = !expanded" id="toggle"><span x-text="expanded ? 'Hide' : 'Show more'"></span></button>                        
                </div>  
                <button silica:click.prevent="update_something" id="update_something">Update</button>           
            </div>
        """


@override_settings(ROOT_URLCONF=__name__)
class MorphTestCase(SilicaBrowserTestCase):

    def test_rerenders_doesnt_break_alpine_component(self):
        self.selenium.get(self.live_server_url + '/morph')

        # First let's check we have a working alpine js component
        self.assertIdIsVisible('item_1')
        self.assertIdIsVisible('item_2')
        self.assertIdIsNotVisible('item_3')
        self.assertIdIsNotVisible('item_4')

        self.findElementById('toggle').click()

        self.assertIdIsVisible('item_1')
        self.assertIdIsVisible('item_2')
        self.assertIdIsVisible('item_3')
        self.assertIdIsVisible('item_4')

        # Now let's check that we can update the component without breaking it
        self.findElementById('update_something').click()
        time.sleep(0.2)
        self.assertHtmlContains("world")

        self.assertIdIsVisible('item_1')
        self.assertIdIsVisible('item_2')
        self.assertIdIsVisible('item_3')
        self.assertIdIsVisible('item_4')

        self.findElementById('toggle').click()

        self.assertIdIsVisible('item_1')
        self.assertIdIsVisible('item_2')
        self.assertIdIsNotVisible('item_3')
        self.assertIdIsNotVisible('item_4')


