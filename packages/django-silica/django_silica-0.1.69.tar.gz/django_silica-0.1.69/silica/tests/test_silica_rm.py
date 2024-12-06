from django.test import TestCase
from django.core.management import call_command
from django.conf import settings
from unittest.mock import patch
from pathlib import Path

from silica.utils import pascal_to_snake

class SilicaRmCommandTestCase(TestCase):
    def setUp(self):
        self.files = []
        self.base_dir = Path(getattr(settings, 'BASE_DIR', None))
        self.main_app_name = 'example_project'

    def tearDown(self):
        for file in self.files:
            if file.exists():
                file.unlink()

    def create_temp_component(self, component_name, subfolders=[]):
        snake_component_name = pascal_to_snake(component_name)
        component_path = self.base_dir / self.main_app_name / 'silica' / Path(*subfolders) / f"{component_name}.py"
        template_path = self.base_dir / self.main_app_name / 'templates' / 'silica' / Path(*subfolders) / f"{snake_component_name}.html"
        component_path.parent.mkdir(parents=True, exist_ok=True)
        template_path.parent.mkdir(parents=True, exist_ok=True)
        component_path.touch()
        template_path.touch()
        self.files.extend([component_path, template_path])
        return component_path, template_path

    def test_remove_component_success(self):
        component_name = "TestComponent"
        component_path, template_path = self.create_temp_component(component_name)

        with patch('builtins.input', return_value='y'):
            call_command('silica', 'rm', component_name, "--silent")

        self.assertFalse(component_path.exists(), "Component file was not removed.")
        self.assertFalse(template_path.exists(), "Template file was not removed.")

    def test_remove_component_skip_confirmation(self):
        component_name = "TestComponent"
        component_path, template_path = self.create_temp_component(component_name)

        call_command('silica', 'rm', component_name, '-y', "--silent")

        self.assertFalse(component_path.exists(), "Component file was not removed.")
        self.assertFalse(template_path.exists(), "Template file was not removed.")

    def test_remove_nonexistent_component(self):
        component_name = "NonExistentComponent"
        # Convert component name to snake_case for the template
        snake_component_name = pascal_to_snake(component_name)

        # Construct paths for the component and template
        component_path = self.base_dir / self.main_app_name / 'silica' / f"{component_name}.py"
        template_path = self.base_dir / self.main_app_name / 'templates' / 'silica' / f"{snake_component_name}.html"

        # Ensure the files do not exist before command execution
        self.assertFalse(component_path.exists(), "Non-existent component file found.")
        self.assertFalse(template_path.exists(), "Non-existent template file found.")

        # Execute the command
        call_command('silica', 'rm', component_name, "--silent")

        # Assert that the files still do not exist after command execution
        self.assertFalse(component_path.exists(), "Non-existent component file was mistakenly created.")
        self.assertFalse(template_path.exists(), "Non-existent template file was mistakenly created.")

    # Additional tests for handling subfolders, invalid component names, etc., can be added as needed.
