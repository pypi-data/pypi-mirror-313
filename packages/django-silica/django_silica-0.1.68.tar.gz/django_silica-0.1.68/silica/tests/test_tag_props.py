from django.test import Client, override_settings
from django.urls import path

from silica import Component
from silica.tests.SilicaTestCase import SilicaTest, SilicaTestCase
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns


class TagProps(Component):
    bool_val: bool = False
    no_value = None
    # int_val: int = 0
    # float_val: float = 0.0
    # str_val: str = ""
    # list_val: list = []
    # dict_val: dict = {}
    # none_val: None = None

    def inline_template(self):
        return """
            <div>   
                bool_val: {{ bool_val }}<br>
                no_value: {{ no_value }}<br>
            </div>
        """


TestView = create_test_view("""    
    {% silica 'silica.tests.test_tag_props.TagProps' bool_val="True" %}
""")


urlpatterns = silica_urlpatterns + [
    path("tag-props", TestView.as_view()),
]


@override_settings(ROOT_URLCONF=__name__)
class TestTagProps(SilicaTestCase):
    def test_props_can_be_set_programmatically(self):
        (
            SilicaTest(component=TagProps, bool_val=None)
            .assertSet("bool_val", None)
        )

    def test_props_can_be_set_via_tag(self):
        client = Client()
        response = client.get("/tag-props")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "bool_val: True")