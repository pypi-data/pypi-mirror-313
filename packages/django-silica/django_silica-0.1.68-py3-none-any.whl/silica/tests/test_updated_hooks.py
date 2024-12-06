from silica import Component
from silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest


class ComponentWithHook(Component):
    prop1 = 'hello'
    updated_called = 'no'
    updated_prop1_called = 'no'
    another_prop_called = 'no'

    def updated(self, key, value):
        if key == 'prop1':
            self.updated_called = value

    def updated_prop1(self, value):
        self.updated_prop1_called = value

    def inline_template(self):
        return """
            <div>
                props1: {{ prop1 }}
                updated_called: {{ updated_called }}
                updated_prop1_called: {{ updated_prop1_called }}
            </div>
        """


class TestUpdatedHooks(SilicaTestCase):
    def test_updated_hook_is_called(self):
        (
            SilicaTest(component=ComponentWithHook)
            .assertSet('prop1', 'hello')
            .set('prop1', 'world')
            .assertSet('updated_called', 'world')
            .assertSet('updated_prop1_called', 'world')
            .assertSee('props1: world')
            .assertSee('updated_called: world')
            .assertSee('updated_prop1_called: world')
        )