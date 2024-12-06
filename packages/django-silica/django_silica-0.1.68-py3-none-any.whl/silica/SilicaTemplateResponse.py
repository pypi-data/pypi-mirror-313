from __future__ import annotations

import json

import urllib.parse

from django.template.response import TemplateResponse
from django.urls import set_urlconf
from django.conf import settings

from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

from silica.errors import SingleRootNodeError

app_urls = getattr(settings, "ROOT_URLCONF", None)


class SilicaTemplateResponse(TemplateResponse):
    def __init__(
            self,
            request,
            template,
            context=None,
            content_type=None,
            status=None,
            charset=None,
            using=None,
            headers=None,
            component: "Component" = None,
            init_js=False,
            lazy=False,
    ):
        super().__init__(
            template=template,
            request=request,
            context=context,
            content_type=content_type,
            status=status,
            charset=charset,
            using=using,
        )
        self.component = component
        self.init_js = init_js
        self.lazy = lazy

    def render(self):
        set_urlconf(app_urls)

        response = super().render()

        if not self.component or not self.component.component_id:
            return response

        template_string = response.content.decode("utf-8").strip()

        # Assuming there's only one root element in the template
        soup = BeautifulSoup(template_string, "html.parser")

        if len(soup.contents) != 1:
            raise SingleRootNodeError(
                f'Silica template for component "{self.component.__module__}" must include a single root element')

        root_node = soup.contents[0]

        root_node.attrs["silica:id"] = self.component.component_id
        root_node.attrs["silica:name"] = self.component.component_name

        if self.init_js and not self.component.lazy:
            snapshot = self.component.create_snapshot()
            snapshot_json = json.dumps(snapshot)
            snapshot_url_encoded = urllib.parse.quote(snapshot_json)
            root_node.attrs["silica:initial-data"] = snapshot_url_encoded

        if self.component.lazy:
            root_node.attrs["silica:lazy"] = "true"
            # root_node.attrs["silica:initial-data"] = "{}"

        self.component.has_rendered = True

        soup.smooth()
        rendered_template = soup.encode(formatter=UnsortedAttributes()).decode("utf-8")

        self.component.rendered(rendered_template)
        self.component.store_state()

        response.content = rendered_template

        return response


class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v
