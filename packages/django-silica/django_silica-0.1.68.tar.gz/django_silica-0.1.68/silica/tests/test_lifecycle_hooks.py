from silica import Component
from silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest


class Lifecycle(Component):
    called_mount = 0
    called_updated = None
    called_updated_property = None

    property = None
    dict_property = {
        "foo": "bar",
        "baz": {
            "jim": "bob"
        }
    }

    def mount(self):
        self.called_mount += 1

    def updated_property(self, value):
        self.called_updated_property = value

    def updated(self, prop, value):
        self.called_updated = f"{prop}={value}"

    def updated_dict_property(self, key, value):
        self.called_updated_property = f"{key}={value}"

    def inline_template(self):
        return """
            <div>
                hi!
            </div>        
        """


class LifecycleTestCase(SilicaTestCase):
    def test_mount_is_called_once(self):
        (
            # Initial request
            SilicaTest(component=Lifecycle)
            .assertSet("called_mount", 1)
            .set("property", "test")
            .assertSet("called_updated_property", "test")
            .assertSet("called_updated", "property=test")
            .set("dict_property.foo", "baz")
            .assertSet("called_updated_property", "foo=baz")
            .assertSet("called_updated", "dict_property.foo=baz")
            .set("dict_property.baz.jim", "jon")
            .assertSet("called_updated_property", "baz.jim=jon")
            .assertSet("called_updated", "dict_property.baz.jim=jon")
        )

