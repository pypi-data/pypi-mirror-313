from pathlib import Path

from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.conf import settings

from silica.utils import pascal_to_snake

class SilicaMvCommandTestCase(TestCase):
    def setUp(self):
        self.files = []
        self.base_dir = Path(getattr(settings, 'BASE_DIR', None))
        self.main_app_name = 'example_project'

    def tearDown(self):
        for file in self.files:
            if file.exists():
                file.unlink()

    def create_temp_component(self, component_name, subfolders=[]):
        # Convert component name to snake_case for the template
        snake_component_name = pascal_to_snake(component_name)

        component_path = self.base_dir / self.main_app_name / 'silica' / Path(*subfolders) / f"{component_name}.py"
        template_path = self.base_dir / self.main_app_name / 'templates' / 'silica' / Path(*subfolders) / f"{snake_component_name}.html"
        component_path.parent.mkdir(parents=True, exist_ok=True)
        template_path.parent.mkdir(parents=True, exist_ok=True)
        component_path.touch()
        template_path.touch()
        self.files.extend([component_path, template_path])
        return component_path, template_path

    def test_move_component_success(self):
        existing_component_name = "ExistingComponent"
        new_component_name = "NewComponent"

        existing_component_path, existing_template_path = self.create_temp_component(existing_component_name)
        new_component_path = self.base_dir / self.main_app_name / 'silica' / f"{new_component_name}.py"
        new_template_path = self.base_dir / self.main_app_name / 'templates' / 'silica' / f"{pascal_to_snake(new_component_name)}.html"

        call_command('silica', 'mv', existing_component_name, new_component_name, "--silent")

        self.assertFalse(existing_component_path.exists(), "Old component file still exists.")
        self.assertFalse(existing_template_path.exists(), "Old template file still exists.")
        self.assertTrue(new_component_path.exists(), "New component file not found.")
        self.assertTrue(new_template_path.exists(), "New template file not found.")

    def test_move_component_invalid_existing_component(self):
        with self.assertRaises(CommandError):
            call_command('silica', 'mv', 'NonExistentComponent', 'NewComponent', "--silent")

    def test_move_component_to_existing_component(self):
        existing_component_name = "ExistingComponent"
        new_component_name = "NewComponent"

        self.create_temp_component(existing_component_name)
        self.create_temp_component(new_component_name)

        with self.assertRaises(CommandError):
            call_command('silica', 'mv', existing_component_name, new_component_name, "--silent")

    # Assuming the pascal_to_snake function is correctly converting the component names



def test_move_component_with_subfolders(self):
    existing_component_name = "folder1.folder2.ExistingComponent"
    new_component_name = "folder1.folder2.NewComponent"

    # Extract the final component name
    *_, final_new_component_name = new_component_name.split('.')

    existing_component_path, existing_template_path = self.create_temp_component("ExistingComponent", ['folder1', 'folder2'])

    new_component_path = self.base_dir / self.main_app_name / 'silica' / 'folder1' / 'folder2' / f"{final_new_component_name}.py"
    new_template_path = self.base_dir / self.main_app_name / 'templates' / 'silica' / 'folder1' / 'folder2' / f"{pascal_to_snake(final_new_component_name)}.html"

    # Debugging output
    print("Final new component path:", new_component_path)
    print("Final new template path:", new_template_path)

    # Ensure new files do not exist before command execution
    if new_component_path.exists():
        new_component_path.unlink()
    if new_template_path.exists():
        new_template_path.unlink()

    call_command('silica', 'mv', existing_component_name, new_component_name, "--silent")

    # Asserting the existence of new files
    self.assertFalse(existing_component_path.exists(), "Old component file still exists.")
    self.assertFalse(existing_template_path.exists(), "Old template file still exists.")
    self.assertTrue(new_component_path.exists(), "New component file not found.")
    self.assertTrue(new_template_path.exists(), "New template file not found.")
