from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import Context, Template


def create_test_view(inline_template_string, context_dict=None):
    """
    Dynamically creates a class-based view with the provided inline template string and context.

    :param inline_template_string: The template string to be rendered.
    :param context_dict: Optional dictionary to be used as context for rendering the template.
    :return: A class-based view dynamically generated.
    """
    if context_dict is None:
        context_dict = {}

    class DynamicTestView(TemplateView):
        def get(self, request, *args, **kwargs):
            context_dict['request'] = request

            template = Template("""
                <html>
                <head>
                {% load silica %}
                {% load silica_scripts %}
                {% silica_scripts %} 
                <link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgo=">
                </head>
                <body>   
            """ + inline_template_string + """
                </body>
                </html>
            """)
            context = Context(context_dict)
            rendered_template = template.render(context)
            return HttpResponse(rendered_template)

    return DynamicTestView


def data_get(data, path, default=None):
    """
    Retrieves a value from a nested data structure using "dot" notation.
    This function is designed to work with dictionaries, lists, tuples, and objects.
    It also supports keys with dots by using square bracket notation.

    Parameters
    ----------
    data : any
        The data structure from which to retrieve the value.
        This can be a nested structure of dictionaries, lists, tuples, and objects.
    path : str
        The path to the value to be retrieved. Use dot notation for nested structures.
        Use square brackets for keys that contain dots.
        Example: 'user.name[first.name]' would look for data['user']['name']['first.name']
    default : any, optional
        The default value to return if the specified path is not found in the data structure.
        By default, it is None.

    Returns
    -------
    any
        The value found at the specified path in the data structure.
        If the path is not found, the default value is returned.

    Examples
    --------
    # Nested dictionary example
    data = {'user': {'name': {'first.name': 'John', 'last': 'Doe'}}}
    print(data_get(data, 'user.name[first.name]'))  # Outputs: John

    # List example
    data = ['John', 'Doe']
    print(data_get(data, '0'))  # Outputs: John

    # Mixed example with dotted key
    data = {'users': [{'name.full': 'John Doe'}, {'name.full': 'Jane Doe'}]}
    print(data_get(data, 'users.1[name.full]'))  # Outputs: Jane Doe

    # Object example
    class User:
        def __init__(self, name):
            self.name = {'full.name': name}
    data = User('John Doe')
    print(data_get(data, 'name[full.name]'))  # Outputs: John Doe
    """

    def get_item(obj, key):
        if isinstance(obj, dict):
            return obj.get(key, default)
        elif isinstance(obj, (list, tuple)) and key.isdigit():
            index = int(key)
            return obj[index] if 0 <= index < len(obj) else default
        elif hasattr(obj, key):
            return getattr(obj, key)
        else:
            return default

    def parse_path(path):
        parts = []
        current = ''
        bracket_depth = 0
        for char in path:
            if char == '.' and bracket_depth == 0:
                if current:
                    parts.append(current)
                    current = ''
            elif char == '[':
                bracket_depth += 1
                if bracket_depth == 1 and current:
                    parts.append(current)
                    current = ''
                else:
                    current += char
            elif char == ']':
                bracket_depth -= 1
                if bracket_depth == 0:
                    parts.append(current)
                    current = ''
                else:
                    current += char
            else:
                current += char
        if current:
            parts.append(current)
        return parts

    parts = parse_path(path)
    for part in parts:
        if data is None:
            return default
        data = get_item(data, part)
    return data
