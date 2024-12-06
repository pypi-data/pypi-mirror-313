import importlib
import json
import re
from inspect import getattr_static
from typing import Dict, Any, List
import shortuuid
import uuid

from django.apps import apps
from django.db.models import Model
from django.http import HttpRequest
from django.core.cache import cache
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.utils.decorators import classonlymethod
from django.utils.module_loading import import_string
from silica.mixins.ValidatesProperties import ValidatesProperties

from silica.utils import pascal_to_snake
from silica.errors import SetPropertyException
from silica.SilicaTemplateResponse import SilicaTemplateResponse


class Component(TemplateView, ValidatesProperties):
    component_id: str = ""
    component_name: str = ""
    query_params: dict = {}
    has_rendered: bool = False
    js_calls: list = []
    event_calls: list = []
    lazy: bool = False

    def __init__(self, **kwargs):
        self.response_class = SilicaTemplateResponse

        self.component_id = ""
        self.component_key = ""
        self.component_name = ""
        self.lazy = False

        self.request: HttpRequest = None

        super().__init__(**kwargs)

        if "id" in kwargs:
            self.component_id = kwargs["id"]

        if "component_name" in kwargs:
            self.component_name = kwargs["component_name"]

        if "request" in kwargs:
            self.request = kwargs["request"]

        if "lazy" in kwargs:
            self.lazy = kwargs["lazy"]

        assert self.component_id != "", "Component id must be set"
        assert self.component_name != "", "Component name must be set"

        self._set_template()

    def _set_template(self):
        """Either template_name was provided, or inline_template was provided, or we'll set the template_name based 
        on the component name."""
        # check if lazy loading, if so, set template_name to placeholder
        if self.lazy:
            # todo, inline place holder -> user placeholder -> framework placeholder
            if inline_placeholder := self.inline_placeholder():
                self.template_name = f"::silica-inline::{inline_placeholder}"
                return
            # else:
            #     self.template_name = "silica/placeholder.html"
            # return

        if self.template_name:
            return

        if inline_template := self.inline_template():
            self.template_name = f"::silica-inline::{inline_template}"
            return

        self.template_name = f"silica/{self.get_template_name()}"

    # abstract
    def inline_template(self):
        pass

    # abstract
    def inline_placeholder(self):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["component_id"] = self.component_id

        # Load local attributes into context
        local_state = self._local_state()

        # Loading state from cache into context
        cached_state = self.get_state()

        state = {**local_state, **cached_state}

        for key, value in state.items():
            context[key] = value

        # Set authenticated user
        if self.request and self.request.user.is_authenticated:
            context["user"] = self.request.user

        return context

    def _local_state(self, is_setting=False):
        state = {}
        for attr in dir(self):
            if not self._is_public(attr, is_setting):
                continue
            try:
                value = getattr(self, attr)
                if (
                        not attr.startswith("_")
                        and not callable(value)
                        and not isinstance(
                    getattr(Component, attr, None), classonlymethod
                )
                ):
                    state[attr] = value
            except AttributeError as e:
                print(f"Issue with attribute: {attr} - Error: {e}")

        return state

    def store_state(self):
        # Extracting non-private and non-callable attributes for state
        state = self._local_state(is_setting=True)

        cache.set(f"silica:component:{self.component_id}", state)

    def get_state(self):
        return cache.get(f"silica:component:{self.component_id}", {})

    def get_template_name(self):
        return pascal_to_snake(self.__class__.__name__) + ".html"

    def render(
            self, init_js=False, extra_context=None, request=None, lazy=False
    ) -> str:
        """prepare context and render component in a response"""

        if extra_context is not None:
            self.extra_context = extra_context

        if request:
            self.request = request

        context = self.get_context_data()
        context.update(
            {
                "js_calls": self.js_calls,
                "event_calls": self.event_calls,
            }
        )

        response = self.render_to_response(
            context=context,
            component=self,
            init_js=init_js,
            lazy=lazy,
        )

        if hasattr(response, "render"):
            response.render()

        rendered_component = response.content.decode("utf-8")

        return rendered_component

    @classonlymethod
    def as_view(cls, **initkwargs):
        """This is the first point into a Django view, ensure name is provided from url and initiate ID is set before the view is called."""
        if "component_id" not in initkwargs:
            initkwargs["component_id"] = str(shortuuid.uuid())

        if "component_name" not in initkwargs:
            # Convert the class name from CamelCase to snake_case
            initkwargs["component_name"] = re.sub(
                r"(?<!^)(?=[A-Z])", "-", cls.__name__
            ).lower()

        return super().as_view(**initkwargs)

    @staticmethod
    def create(
            component_id: str,
            component_name: str,
            component_key: str = "",  # will be needed sooner or later
            request: HttpRequest = None,
            kwargs: Dict[str, Any] = {},
    ) -> "Component":
        if "lazy" in kwargs:
            lazy = kwargs["lazy"]
        else:
            lazy = False

        ComponentClass = Component.get_component_class_from_name(component_name)

        component_instance = ComponentClass(
            component_id=component_id,
            component_name=component_name,
            lazy=lazy,
            request=request,
        )
        component_instance._set_state_from_cache()
        component_instance.js_calls = []
        component_instance.event_calls = []

        # Set attributes from {% silica .. %} tag
        for key, value in kwargs.items():
            if component_instance._is_public(key):
                component_instance.set_property(key, value, False)
                setattr(component_instance, key, value)

        return component_instance

    def _set_state_from_cache(self):
        """
        Load state from cache into component instance.
        """
        state = self.get_state()
        for key, value in state.items():
            setattr(self, key, value)

    def render_to_string(self):
        template_name = f"silica/{self.get_template_name()}"
        return render_to_string(template_name, self.get_context_data())

    def reset_js_calls(self):
        self.js_calls = []

    def dispatch(self, request, *args, **kwargs):
        """
        Called by the `as_view` class method when utilizing a component directly as a view.
        """

        # how to provide request in kwargs to mount()?
        self.request = request

        # if any GET variables match query_param 'at' / aliases then set the param key property, we also allow a dict
        # here that doesn't contain an 'as' key, we treat the 'param' key as the url key also
        for key, value in request.GET.items():
            for query_param in self.query_params:
                if isinstance(query_param, dict):
                    if query_param.get("as", query_param.get("param")) == key:
                        # TODO - Could this be firing twice for fresh page loads?
                        self.set_property(query_param.get("param"), value)
                        # setattr(self, query_param.get("param"), value)
                else:
                    if query_param == key:
                        # TODO - Could this be firing twice for fresh page loads?
                        self.set_property(key, value)
                        # setattr(self, key, value)

        if not self.lazy:
            self.mount()

        context = self.get_context_data()
        context.update({"js_calls": self.js_calls})
        context.update({"event_calls": self.event_calls})

        self.store_state()

        rendered_response = self.render_to_response(
            context=context,
            component=self,
            init_js=True,
        )

        return rendered_response

    def process_query_params(self) -> List[Dict[str, Any]]:
        """Determine which query params are to be shown (only show ones that are not equal to their default value)"""
        query_param_list = []

        class_obj = type(self)  # Get the component class

        for param_key in self.query_params:
            if isinstance(param_key, dict):
                # if the query param is a dict, then we'll need to handle it differently
                # we'll need to check if the param is set, and if so, set it to the value of the 'as' key
                # if not, set it to the value of the 'param' key
                param = {
                    "key": param_key.get("param"),
                    "visible": True,
                    "as": param_key.get("as", param_key.get("param")),
                }
            else:
                param = {"key": param_key, "visible": False, "as": None}

            default_value = getattr(class_obj, param["key"], None)
            current_value = getattr(self, param["key"], None)

            if current_value != default_value:
                param["visible"] = True

            query_param_list.append(param)

        return query_param_list

    def _is_public(self, name: str, for_setting: bool = False) -> bool:
        """Determines if the name should be sent in the context."""

        protected_names = (
            "render",
            "request",
            "as_view",
            "view",
            "args",
            "kwargs",
            "content_type",
            "extra_context",
            "http_method_names",
            "template_engine",
            "template_name",
            "dispatch",
            "id",
            "get",
            "get_context_data",
            "get_template_names",
            "render_to_response",
            "http_method_not_allowed",
            "options",
            "setup",
            "fill",
            "view_is_async",
            # Component methods
            "component_id",
            "component_name",
            "component_key",
            "reset",
            "mount",
            "hydrate",
            "updating",
            "update",
            "calling",
            "called",
            "complete",
            "rendered",
            "parent_rendered",
            "validate",
            "is_valid",
            "errors",
            "updated",
            "parent",
            "children",
            "call",
            "js_calls",
            "event_calls",
            "component_cache_key",
            "inline_template",
            "placeholder",
            "processed_query_params",
            "query_params",
            "validation_rules",
        )

        # Check if the attribute is a @property
        is_property = isinstance(getattr_static(self.__class__, name, None), property)

        return not (
                name.startswith("_")
                or name in protected_names
                or (for_setting and is_property)
        )

    def set_property(self, attr, value, with_hooks=True):
        """Set a property on the component."""
        segments = attr.split('.')
        base_attr = segments[0]

        if not self._is_public(base_attr, for_setting=True):
            raise SetPropertyException(f'Attribute "{base_attr}" can not be set.')

        # Single Properties on the component i.e. "day"
        if '.' not in attr:
            if hasattr(self, attr):
                # Check if the property definiton is a list and ensure the passed value is a list. This will be for 
                # query_param, multi-checkboxes or just user defined list property
                if isinstance(getattr(self, attr), list) and not isinstance(value, list):
                    value = [value]

                setattr(self, attr, value)

                if with_hooks:
                    self._invoke_hooks(attr, '', value)
            else:
                raise SetPropertyException(f'"{attr}" does not exist on component "{self.__class__.__name__}".')
            return

        # Model Properties i.e. "user.first_name" If we have validation_rules and the current segment is a Model 
        # instance, we'll need to check if the segment is a key in the validation_rules
        elif hasattr(self, 'validation_rules') and isinstance(getattr(self, base_attr), Model):
            if attr not in self.validation_rules:
                raise SetPropertyException(f'"{attr}" is not a valid key in the validation_rules.')

            setattr(getattr(self, base_attr), segments[1], value)

        else:
            # Nested Non-Model Properties i.e. "some_dict.profile.age"
            obj = self
            for i, segment in enumerate(segments[:-1]):
                # Check if the segment is looking like a list index
                if segment.isdigit() and isinstance(obj, list):
                    segment = int(segment)
                    if segment >= len(obj):
                        raise SetPropertyException(f'Index "{segment}" out of range for list.')

                    obj = obj[segment]

                else:
                    # Check for dict or attribute existence
                    if isinstance(obj, dict) and segment in obj:
                        obj = obj[segment]
                    elif hasattr(obj, segment):
                        obj = getattr(obj, segment)
                    else:
                        raise SetPropertyException(f'Dictionary key or attribute "{segment}" does not exist.')

                if not isinstance(obj, (dict, list, type(self))):
                    raise SetPropertyException('Cannot set property on non-dict/list/component property.')

            # Set the value on the final target
            final_segment = segments[-1]
            if isinstance(final_segment, str) and final_segment.isdigit() and isinstance(obj, list):
                final_segment = int(final_segment)
                if final_segment < len(obj):
                    obj[final_segment] = value
                else:
                    raise SetPropertyException(f'Index "{final_segment}" out of range for list.')

            if isinstance(obj, dict) and final_segment in obj:
                obj[final_segment] = value
            elif hasattr(obj, final_segment):
                setattr(obj, final_segment, value)
            else:
                raise SetPropertyException(f'"{final_segment}" does not exist on property "{attr}".')

            if with_hooks:
                self._invoke_hooks(base_attr, '.'.join(segments[1:]), value)

    def _invoke_hooks(self, base_attr, remaining_path, value):
        # Specific hook for the property
        updated_hook_name = f"updated_{base_attr}"
        if hasattr(self, updated_hook_name):
            if remaining_path:
                getattr(self, updated_hook_name)(remaining_path, value)
            else:
                getattr(self, updated_hook_name)(value)

        # General update hook
        if hasattr(self, "updated"):
            full_path = f"{base_attr}.{remaining_path}" if remaining_path else base_attr
            getattr(self, "updated")(full_path, value)

    def js_call(self, method, *args, **kwargs):
        self.js_calls.append(
            {
                "fn": method,
                "args": args,
                "kwargs": kwargs,
            }
        )

    # Events
    def dispatch_browser_event(self, event_name, payload: Dict = None):
        self.js_call("_silicaDispatchBrowserEvent", event_name, payload)

    def emit(self, event_name, payload: Dict = None):
        """Emit to all component present in the DOM"""
        self.event_calls.append(
            {
                "type": "emit",
                "name": event_name,
                "payload": payload,
            }
        )

    def emit_to(self, component_name, event_name, payload: Dict = None):
        """Emit to a specific component in the dom"""
        self.event_calls.append(
            {
                "type": "emit_to",
                "component_name": component_name,
                "name": event_name,
                "payload": payload,
            }
        )

    def receive_event(self, event_name, payload):
        # if we have a listener for this event, call it
        if hasattr(self, event_name) and callable(getattr(self, event_name)):
            getattr(self, event_name)(payload)

    def get_absolute_path(self):
        module_name = (
            self.__module__
        )  # gives the module name in which the class is defined
        class_name = self.__class__.__name__  # gives the name of the class
        return f"{module_name}.{class_name}"

    def get_component_path(self):
        absolute_path = self.get_absolute_path()
        if ".silica." in absolute_path:
            return absolute_path.split(".silica.", 1)[1].rsplit(".", 1)[0]
        else:
            # Handle this case accordingly.
            # You can return the original string or a placeholder/error message.
            return absolute_path

    # Hooks
    def mount(self):
        pass

    def rendered(self, html):
        """
        Hook that gets called after the component has been rendered.
        """
        pass

    def redirect(self, url):
        self.js_call("_silicaRedirect", url)

    def jsonable_data(self):
        state = self.get_context_data()

        for key, value in state.copy().items():
            if not self._is_jsonable(value):
                del state[key]

        return state

    def _serialize_property_value(self, value):
        if isinstance(value, uuid.UUID):
            return str(value)
        elif self._is_jsonable(value):
            return value
        else:
            return None

    def format_data(self):
        state = self.get_context_data()
        formatted = {}

        for key, value in state.copy().items():
            if self._is_jsonable(value):
                formatted[key] = value
            # check for uuid
            elif isinstance(value, uuid.UUID):
                formatted[key] = str(value)
            elif isinstance(value, Model):
                # We'll only pass back model keys that have been specified in the component's validation_rules, 
                # consider that the keys in validation_rules will be in format of "{model_instance}.{field}" and 
                # we'll want to provide them as a json object
                for rule_key in self.validation_rules.keys():
                    if rule_key.startswith(f"{key}."):
                        formatted[key] = {
                            **formatted.get(key, {}),
                            rule_key.split(".")[1]: self._serialize_property_value(
                                getattr(value, rule_key.split(".")[1])),
                        }

        return formatted

    def create_snapshot(self):
        snapshot = {
            'data': self.format_data(),
            'js_calls': self.js_calls,
            'event_calls': self.event_calls,
            'query_params': self.process_query_params(),
        }
        return snapshot

    def _is_jsonable(self, x):
        if isinstance(x, Model):
            return False
        try:
            json.dumps(x)
            return True
        except (TypeError, OverflowError):
            return False

    @staticmethod
    def get_component_class_from_name(component_name: str):
        for app in apps.get_app_configs():
            # Attempt to load the 'silica' module from each app
            try:
                silica_module = importlib.import_module(
                    f"{app.name}.silica.{component_name}"
                )

                importlib.reload(silica_module)

                # class_name will always be the last portion of the path, the last part of the string after the last 
                # dot, dots may not exist
                class_name = component_name.split(".")[-1]

                # If we don't encounter an ImportError, try to get the component
                component_class = getattr(silica_module, class_name, None)
                if component_class:
                    # If found, use it (or return, or whatever your logic is)
                    return component_class
            except ImportError:
                continue

        # finally, try and import the component_name itself if it's a direct path to a component
        try:
            component_class = import_string(component_name)
            if component_class:
                # If found, use it (or return, or whatever your logic is)
                return component_class
        except ImportError:
            pass

        # If the component wasn't found in any app's 'silica' module, raise an error
        raise ImportError(
            f"Component {component_name} not found in any app's 'silica' module"
        )

    def __repr__(self):
        return f"Component(name='{self.component_name}' id='{self.component_id}')"
