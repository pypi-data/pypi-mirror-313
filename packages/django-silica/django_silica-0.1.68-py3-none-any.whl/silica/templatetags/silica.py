from typing import Dict

import shortuuid

from silica.utils import kwarg_as_dict
from silica.errors import ComponentNotValid
from silica import Component
from django import template

register = template.Library()


def silica(parser, token):
    parts = token.split_contents()

    if len(parts) < 2:
        raise template.TemplateSyntaxError(
            "%r tag requires at least a single argument" % token.contents.split()[0]
        )

    component_name = parser.compile_filter(parts[1])

    kwargs = {}
    for arg in parts[2:]:
        try:
            kwarg = kwarg_as_dict(arg)
            kwargs.update(kwarg)
        except ValueError:
            pass

    return SilicaNode(component_name=component_name, kwargs=kwargs)


register.tag("silica", silica)


class SilicaNode(template.Node):
    def __init__(self, component_name, kwargs: Dict = {}):
        self.component_name = component_name
        self.kwargs = kwargs
        self.component_key = ""
        self.parent = None

    def render(self, context, **kwargs):
        request = context.get("request", None)

        resolved_kwargs = {}
        for key, value in self.kwargs.items():
            try:
                resolved_value = template.Variable(value).resolve(context)
                resolved_kwargs.update({key: resolved_value})
            except template.VariableDoesNotExist:
                resolved_kwargs.update({key: value})

        if "key" in resolved_kwargs:
            component_key = resolved_kwargs.pop("key")
        else:
            component_key = None

        if "lazy" in resolved_kwargs:
            lazy = resolved_kwargs.pop("lazy")
        else:
            lazy = False

        try:
            component_name = self.component_name.resolve(context)
        except AttributeError:
            raise ComponentNotValid(
                f"Component template is not valid: {self.component_name}."
            )

        resolved_kwargs.update({"lazy": lazy})

        component_id = shortuuid.uuid()

        self.view = Component.create(
            component_id=component_id,
            component_name=component_name,
            component_key=component_key,
            kwargs=resolved_kwargs,
            request=request,
        )

        if request:

            # Oddly, django's request.GET will only either return dict (.items(), .dict()) where it will cut short list/multiples of one key
            # or .lists() where it will force all items as a list, even single values, but we do get the multiples.
            processed_params = {}

            for key, values in request.GET.lists():
                # Store the value directly if there's only one, or as a list if there are multiple
                processed_params[key] = values if len(values) > 1 else values[0]

            for key, value in processed_params.items():
                for query_param in self.view.query_params:
                    if isinstance(query_param, dict):
                        if query_param.get("as", query_param.get("param")) == key:
                            # TODO, should probably not allow dictionary key path setting, just limit to base attribute
                            self.view.set_property(query_param.get("param"), value, False)
                    else:
                        if query_param == key:
                            # TODO, should probably not allow dictionary key path setting, just limit to base attribute
                            self.view.set_property(key, value, False)

            self.request = request

        if not lazy:
            self.view.mount()

        rendered_component = self.view.render(init_js=True, request=request)

        return rendered_component
