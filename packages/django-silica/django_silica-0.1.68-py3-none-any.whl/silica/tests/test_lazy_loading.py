
from django.test import TestCase, override_settings
from django.urls import path

from silica import Component
from silica.tests.SilicaTestCase import SilicaTest
from silica.tests.SilicaBrowserTestCase import SilicaBrowserTestCase
from silica.tests.utils import create_test_view
from silica.urls import urlpatterns as silica_urlpatterns

TestView = create_test_view(f"""{{% silica '{__name__}.LazyLoading' %}}""")

urlpatterns = silica_urlpatterns + [
    path("lazy", TestView.as_view()),
]


class LazyLoading(Component):
    is_mounted: bool = False

    def mount(self):
        self.is_mounted = True

    def inline_template(self):
        return """
            <div>   
                <h1>I will be lazy loaded!</h1>
            </div>
        """

    def inline_placeholder(self):
        return """
            <div>
                <h1>Loading...</h1>
            </div>
        """


class TestLazyLoading(TestCase):
    def test_mount_is_not_called(self):
        (
            SilicaTest(component=LazyLoading, lazy=True)
            .assertSet("is_mounted", False)
        )

    def test_mount_is_called_on_non_lazy(self):
        (
            SilicaTest(component=LazyLoading, lazy=False)
            .assertSet("is_mounted", True)
        )

    def test_placeholder_is_seen(self):
        (
            SilicaTest(component=LazyLoading, lazy=True)
            .assertSee("Loading...")
        )

    def test_placeholder_is_not_seen_on_non_lazy(self):
        (
            SilicaTest(component=LazyLoading, lazy=False)
            .assertDontSee("Loading...")
        )

    def test_silica_lazy_attribute_is_present_on_initial_render(self):
        (
            SilicaTest(component=LazyLoading, lazy=True)
            .assertSee("silica:lazy")
        )

    def test_silica_lazy_attribute_is_not_present_on_initial_render_on_non_lazy(self):
        (
            SilicaTest(component=LazyLoading, lazy=False)
            .assertDontSee("silica:lazy")
        )


@override_settings(ROOT_URLCONF=__name__)
class BrowserTestLazyLoading(SilicaBrowserTestCase):
    def test_lazy_loaded_component_loads(self):
        self.selenium.get(self.live_server_url + '/lazy')

        self.assertHtmlContains("I will be lazy loaded!")