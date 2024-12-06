from django.test import override_settings
from django.urls import path

from silica import Component
from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns


class Component(Component):
    count = 1
    change_prop = False

    def mount(self):
        if self.change_prop:
            self.count += 1

    def inline_template(self):
        return """
            <div>
                count:{{ count }} 
            </div>
        """


Page1View = create_test_view("""    
    <h1>Page 1</h1>
    <a href="page_2" id="visit_page_2">page 2</a>
    {% silica 'silica.tests.test_class_property_modification.Component' change_prop='True' %}
""")


Page2View = create_test_view("""   
    <h1>Page 2</h1>
    {% silica 'silica.tests.test_class_property_modification.Component' change_prop='False' %}
""")


urlpatterns = silica_urlpatterns + [
    path("page_1", Page1View.as_view()),
    path("page_2", Page2View.as_view())
]


@override_settings(ROOT_URLCONF=__name__)
class ClassPropertyModTestCase(SilicaBrowserTestCase):
    def test_modifying_class_property_doesnt_affect_future_instances(self):

        self.selenium.get(self.live_server_url + '/page_1')
        self.assertTrue('count:2' in self.selenium.page_source)

        self.selenium.get(self.live_server_url + '/page_2')
        self.assertTrue('count:1' in self.selenium.page_source)