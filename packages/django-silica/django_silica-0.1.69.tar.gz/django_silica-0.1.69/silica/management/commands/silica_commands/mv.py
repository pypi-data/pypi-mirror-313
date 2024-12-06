from io import StringIO
import os
from silica.utils import pascal_to_snake
from django.core.management.base import BaseCommand, CommandError

def snake_to_camel(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


class Command(BaseCommand):
    help = 'Move a Silica component'
    example = 'silica_mv existing_component_name new_component_name'

    def add_arguments(self, parser):
        parser.add_argument('existing_component_name', type=str)
        parser.add_argument('new_component_name', type=str)
        parser.add_argument('--app', type=str, help='Specify the Django app name')
        parser.add_argument('--silent', action='store_true', help='Run the command in silent mode without output')

    def handle(self, *args, **options):
        existing_component_name: str = options['existing_component_name']
        new_component_name: str = options['new_component_name']
        app_name = options['app']
        existing_subfolders: list[str] = []
        new_subfolders: list[str] = []
        silent = options['silent']


        if silent:
            self.stdout = StringIO()
    
        if '.' in existing_component_name:
            *existing_subfolders, existing_component_name = existing_component_name.split(".")
        if '.' in new_component_name:
            *new_subfolders, new_component_name = new_component_name.split(".")
        
        existing_subfolders = [subfolder.lower() for subfolder in existing_subfolders]
        new_subfolders = [subfolder.lower() for subfolder in new_subfolders]
        existing_component_name = existing_component_name.replace('-', '_')
        new_component_name = new_component_name.replace('-', '_')

        if "_" in existing_component_name:
            existing_component_name = snake_to_camel(existing_component_name)
        else:
            # Capitalize the first letter
            existing_component_name = existing_component_name[0].upper() + existing_component_name[1:]

        if "_" in new_component_name:
            new_component_name = snake_to_camel(new_component_name)
        else:
            # Capitalize the first letter
            new_component_name = new_component_name[0].upper() + new_component_name[1:]

        # Convert component name to snake_case for the template
        existing_snake_component_name = pascal_to_snake(existing_component_name)
        new_snake_component_name = pascal_to_snake(new_component_name)

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
        existing_component_path = os.path.join(base_dir, main_app_name, 'silica', *existing_subfolders, f"{existing_component_name}.py")

        if not os.path.exists(existing_component_path):
            raise CommandError(f"Component {existing_component_name} does not exist.")
        
        new_component_path = os.path.join(base_dir, main_app_name, 'silica', *new_subfolders, f"{new_component_name}.py")

        if os.path.exists(new_component_path):
            raise CommandError(f"Component {new_component_name} already exists.")
        

        # template
        existing_template_path = os.path.join(base_dir, main_app_name, 'templates', 'silica', *existing_subfolders, f"{existing_snake_component_name}.html")

        if not os.path.exists(existing_template_path):
            raise CommandError(f"Template {existing_snake_component_name}.html does not exist.")
        
        new_template_path = os.path.join(base_dir, main_app_name, 'templates', 'silica', *new_subfolders, f"{new_snake_component_name}.html")

        if os.path.exists(new_template_path):
            raise CommandError(f"Template {new_snake_component_name}.html already exists.")
        

        # Move component
        os.rename(existing_template_path, new_template_path)
        os.rename(existing_component_path, new_component_path)

        self.stdout.write(self.style.SUCCESS(f"Component {existing_component_name} moved to {new_component_name}"))
        self.stdout.write(self.style.SUCCESS(f"Template {existing_snake_component_name}.html moved to {new_snake_component_name}.html"))
