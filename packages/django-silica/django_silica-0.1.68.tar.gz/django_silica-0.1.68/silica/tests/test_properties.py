from silica import Component
from silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest


class Properties(Component):
    foo = "bar"

    @property
    def ding(self):
        return 'dong'

    def inline_template(self):
        return """
            <div>
            foo: {{ foo }}
            ding: {{ ding }}
            </div>
        """


class PropertiesTestCase(SilicaTestCase):
    def test_can_set_properties(self):
        (
            SilicaTest(component=Properties)
            .assertSet("foo", "bar")
            .assertSee("bar")
            .set("foo", "boo")
            .assertSet("foo", "boo")
            .assertSee("boo")
        )

    def test_python_property(self):
        (
            SilicaTest(component=Properties)
            .assertSee("ding: dong")
        )
