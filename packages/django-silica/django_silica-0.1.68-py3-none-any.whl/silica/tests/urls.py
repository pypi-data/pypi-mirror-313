from django.urls import path
from django.views.generic import TemplateView


class ComponentTagTest(TemplateView):
    template_name = "component_tag_test.html"


class ComponentSubfolderTest(TemplateView):
    template_name = "component_subfolder_test.html"


class CachePersistTestView(TemplateView):
    template_name = "cache_persist_test_view.html"


class ScriptHydratedView(TemplateView):
    template_name = "script_hydrated_test_view.html"


class MagicMethodsView(TemplateView):
    template_name = "magic_methods_test_view.html"


urlpatterns = [
    path("silica/tests/component-tag-test", ComponentTagTest.as_view()),
    path("silica/tests/component-subfolder-test", ComponentSubfolderTest.as_view()),
    path("silica/tests/script-tags-are-hydrated", ScriptHydratedView.as_view()),
    path("silica/tests/magic-methods", MagicMethodsView.as_view()),
    # ... add more testing URLs as needed
]
