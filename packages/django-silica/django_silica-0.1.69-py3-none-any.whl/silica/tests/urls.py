from django.urls import path
from django.views.generic import TemplateView


class ComponentTagTest(TemplateView):
    template_name = "component_tag_test.html"


class ComponentSubfolderTest(TemplateView):
    template_name = "component_subfolder_test.html"

urlpatterns = [
    path("silica/tests/component-tag-test", ComponentTagTest.as_view()),
    path("silica/tests/component-subfolder-test", ComponentSubfolderTest.as_view()),
]
