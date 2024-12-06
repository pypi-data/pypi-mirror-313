from silica import Component
from silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest


class Methods(Component):
    test_value = 1

    fruit = "banana"

    def set_apple(self):
        self.fruit = "apple"

    def set_fruit(self, fruit=""):
        self.fruit = fruit

    def inline_template(self):
        return """
            <div>
                {{ fruit }}
                <a silica:click="set_apple()">set apple</a>
            </div>        
        """


class MethodsTestCase(SilicaTestCase):
    def test_method_calling_without_args(self):
        (
            SilicaTest(component=Methods)
            .assertSet("fruit", "banana")
            .assertSee("banana")
            .call("set_apple")
            .assertSet("fruit", "apple")
        )

    def test_method_calling_with_args(self):
        (
            SilicaTest(component=Methods)
            .call("set_fruit", "cherry")
            .assertSet("fruit", "cherry")
            .assertSee("cherry")
        )
