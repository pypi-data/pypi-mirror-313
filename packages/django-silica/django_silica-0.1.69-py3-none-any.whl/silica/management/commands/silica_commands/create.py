from io import StringIO
import os
from pathlib import Path
import random
from silica.utils import pascal_to_snake
from django.core.management.base import BaseCommand, CommandError

def snake_to_camel(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


class Command(BaseCommand):
    help = 'Creates a new Silica component'
    quotes = [
        'You are in control of your own destiny.',
        'Create something awesome.',
        'Carpe diem.',
    ]
    TEMPLATE_FOR_CLASS = """from silica import Component


class {class_name}(Component):
    template_name = "{template_name}"
    
"""

    TEMPLATE_FOR_INLINE_CLASS = """from silica import Component


class {class_name}(Component):

    def inline_template(self):
        return \"\"\"
            <div>
            {quote}
            </div>
        \"\"\"
    # Your class implementation here
"""

    TEMPLATE_FOR_TEMPLATE = f"""
{{# {random.choice(quotes)} #}}
"""

    def add_arguments(self, parser):
        parser.add_argument('component_name', type=str)
        parser.add_argument('--inline', action='store_true', help='Use inline template')
        parser.add_argument('--app', type=str, help='Specify the Django app name')
        parser.add_argument('--silent', action='store_true', help='Run the command in silent mode without output')

    def handle(self, *args, **options):
        component_name: str = options['component_name']
        use_inline_template = options['inline']
        app_name = options['app']
        silent = options['silent']


        if silent:
            self.stdout = StringIO()

        subfolders: list[str] = []

        if '.' in component_name:
            *subfolders, component_name = component_name.split(".") # list packing

        subfolders = [subfolder.lower() for subfolder in subfolders]
        component_name = component_name.replace('-', '_')

        if "_" in component_name:
            component_name = snake_to_camel(component_name)
        else:
            # Capitalize the first letter
            component_name = component_name[0].upper() + component_name[1:]
        
        # Convert component name to snake_case for the template
        snake_component_name = pascal_to_snake(component_name)


        # Choose the template based on the --inline flag
        if use_inline_template:
            component_template = self.TEMPLATE_FOR_INLINE_CLASS.format(class_name=component_name, quote=random.choice(self.quotes))
            write_template = False
        else:
            write_template = True
            template_name = Path("silica/") / "/".join(subfolders) / f"{snake_component_name}.html"
            component_template = self.TEMPLATE_FOR_CLASS.format(class_name=component_name, template_name=str(template_name))



        if app_name:
            main_app_name = app_name
        else:
            settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
            if not settings_module:
                raise CommandError("DJANGO_SETTINGS_MODULE environment variable not set.")
            main_app_name = settings_module.split('.')[0]

        

        # Get the BASE_DIR from Django settings
        from django.conf import settings
        base_dir = getattr(settings, 'BASE_DIR')
        if not base_dir:
            raise CommandError("Unable to determine the BASE_DIR from Django settings.")

        if not os.path.exists(os.path.join(base_dir, main_app_name)):
            raise CommandError(f"App {main_app_name} not found.")

        component_path = os.path.join(base_dir, main_app_name, 'silica', *subfolders, f"{component_name}.py")
        template_path = os.path.join(base_dir, main_app_name, 'templates', 'silica', *subfolders, f"{snake_component_name}.html")

        # Check if files already exist
        if os.path.exists(component_path) or os.path.exists(template_path):
            raise CommandError(f"Component {component_name} already exists.")

        # Create component file
        os.makedirs(os.path.dirname(component_path), exist_ok=True)
        with open(component_path, 'w') as f:
            f.write(component_template)
            self.stdout.write(self.style.SUCCESS(f"Component created at {component_path}"))

        # Create template file
        if write_template:
            os.makedirs(os.path.dirname(template_path), exist_ok=True)
            with open(template_path, 'w') as f:
                f.write(self.TEMPLATE_FOR_TEMPLATE)
                self.stdout.write(self.style.SUCCESS(f"Template created at {template_path}"))