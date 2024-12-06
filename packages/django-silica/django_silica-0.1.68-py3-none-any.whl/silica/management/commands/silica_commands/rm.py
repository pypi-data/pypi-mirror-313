from io import StringIO
import os
from silica.utils import pascal_to_snake
from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_string


def snake_to_camel(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


class Command(BaseCommand):
    concept = """rm [component] - remove the component file and template path, with a prompt "Are you sure you want to remove this component?"""
    help = "remove a Silica component"
    example = "silica_rm component_name"

    def add_arguments(self, parser):
        parser.add_argument('component_name', type=str)
        parser.add_argument('--app', type=str, help='Specify the Django app name')
        parser.add_argument('-y', action='store_true', help='Do not prompt for confirmation')
        parser.add_argument('--silent', action='store_true', help='Run the command in silent mode without output')

    def handle(self, *args, **options):
        component_name: str = options['component_name']
        app_name = options['app']
        skip_confirmation = options['y']
        subfolders: list[str] = []
        silent = options['silent']


        if silent:
            self.stdout = StringIO()
    
        if '.' in component_name:
            *subfolders, component_name = component_name.split(".")

        
        subfolders = [subfolder.lower() for subfolder in subfolders]
        component_name = component_name.replace('-', '_')

        if "_" in component_name:
            component_name = snake_to_camel(component_name)
        else:
            # Capitalize the first letter
            component_name = component_name[0].upper() + component_name[1:]

        # Convert component name to snake_case for the template
        existing_snake_component_name = pascal_to_snake(component_name)

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


        # component
        component_path = os.path.join(base_dir, main_app_name, 'silica', *subfolders, f"{component_name}.py")

        # template
        template_path = os.path.join(base_dir, main_app_name, 'templates', 'silica', *subfolders, f"{existing_snake_component_name}.html")

        # check if component exists
        component_exists = os.path.exists(component_path)
        template_exists = os.path.exists(template_path)

        # import component
        try:
            dotted_path = f"{main_app_name}.silica.{component_name}.{component_name}"
            component_class = import_string(dotted_path)
            if component_class:
                # check if component has inline_template method
                inline_component: bool = hasattr(component_class, 'inline_template')
        except ImportError:
            inline_component: bool = False

        if component_exists or template_exists:
            if skip_confirmation:
                # Remove without confirmation
                if component_exists:
                    os.remove(component_path)
                    if inline_component:
                        self.stdout.write(self.style.WARNING(f"Inline component {component_path} removed."))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Component {component_path} removed."))
                if template_exists:
                    os.remove(template_path)
                    self.stdout.write(self.style.SUCCESS(f"Template {template_path} removed."))
            else:
                # Confirmation for each cases
                if component_exists and template_exists:
                    confirmation_message = f"Are you sure you want to remove the component {component_path} and its template {template_path}?"
                elif component_exists:
                    if inline_component:
                        confirmation_message = f"Are you sure you want to remove the inline component {component_path}?"
                    else:
                        confirmation_message = f"Are you sure you want to remove the component {component_path}?"
                elif template_exists:
                    confirmation_message = f"Are you sure you want to remove the template {template_path}?"

                self.stdout.write(self.style.WARNING(confirmation_message))
                confirmation = input("Y/n: ")
                if confirmation.lower() == "y":
                    if component_exists:
                        os.remove(component_path)
                        self.stdout.write(self.style.SUCCESS(f"Component {component_path} removed."))
                    if template_exists:
                        os.remove(template_path)
                        self.stdout.write(self.style.SUCCESS(f"Template {template_path} removed."))
        else:
            self.stdout.write(self.style.ERROR(f"Component {component_path} and template {template_path} not found."))