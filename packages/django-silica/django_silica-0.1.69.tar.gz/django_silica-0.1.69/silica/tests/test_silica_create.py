from pathlib import Path
from silica.tests.SilicaTestCase import SilicaTestCase
from django.core.management import call_command
from django.conf import settings
import importlib.util


def import_from_path(path: Path, object_name: str):
    # Ensure the path is absolute
    if not path.is_absolute():
        path = path.resolve()

    # Get the module name and import path
    module_name = path.stem
    spec = importlib.util.spec_from_file_location(module_name, path)

    # Load the module from the spec
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Return the desired object from the module
    return getattr(module, object_name)


class ComponentTagTestCase(SilicaTestCase):
    # setup create files of self.files list
    def setUp(self):
        self.files = []

    # teardown delete files of self.files list
    def tearDown(self):
        for file in self.files:
            if file.exists():
                file.unlink()

    def test_template_and_component_name_are_snake_case(self):
        call_command('silica', 'create', "TestUniqueSideBar", "--silent")
        main_app_dir = Path(settings.BASE_DIR) / "example_project"

        # component
        pascal_component_path = main_app_dir / 'silica' / "TestUniqueSideBar.py"
        self.files.append(pascal_component_path)
        snake_component_path = main_app_dir / 'silica' / "test_unique_side_bar.py"
        self.files.append(snake_component_path)

        # template
        pascal_template_path = main_app_dir / 'templates' / 'silica' / "TestUniqueSideBar.html"
        self.files.append(pascal_template_path)
        snake_template_path = main_app_dir / 'templates' / 'silica' / "test_unique_side_bar.html"
        self.files.append(snake_template_path)

        self.assertTrue(pascal_component_path.exists())
        self.assertTrue(snake_template_path.exists())


    def test_silica_create_with_nested_subfolders(self):
        call_command('silica', 'create', "folder1.folder2.folder3.NewComponent", "--silent")
        main_app_dir = Path(settings.BASE_DIR) / "example_project"

        # Component in nested subfolders
        component_path = main_app_dir / 'silica' / 'folder1' / 'folder2' / 'folder3' / "NewComponent.py"
        self.files.append(component_path)

        # Template in nested subfolders
        template_path = main_app_dir / 'templates' / 'silica' / 'folder1' / 'folder2' / 'folder3' / "new_component.html"
        self.files.append(template_path)

        incorrect_component_path = main_app_dir / 'silica' / 'folder1.folder2.folder3' / "NewComponent.py"
        self.files.append(incorrect_component_path)
        incorrect_template_path = main_app_dir / 'templates' / 'silica' / 'folder1.folder2.folder3' / "new_component.html"
        self.files.append(incorrect_template_path)

        self.assertTrue(component_path.exists())
        self.assertTrue(template_path.exists())


    def test_silica_template_name_in_component_definition(self):
        call_command('silica', 'create', "folder1.folder2.folder3.NewComponent", "--silent")
        main_app_dir = Path(settings.BASE_DIR) / "example_project"

        # Component in nested subfolders
        component_path = main_app_dir / 'silica' / 'folder1' / 'folder2' / 'folder3' / "NewComponent.py"
        self.files.append(component_path)

        # Template in nested subfolders
        template_path = main_app_dir / 'templates' / 'silica' / 'folder1' / 'folder2' / 'folder3' / "new_component.html"
        self.files.append(template_path)

        self.assertTrue(component_path.exists())
        self.assertTrue(template_path.exists())

        Component = import_from_path(component_path, "NewComponent")
        self.assertEqual(Component.template_name, "silica/folder1/folder2/folder3/new_component.html")


    def test_command_allows_kebab_case(self):
        call_command('silica', 'create', "some.Sub-folder.some-component", "--silent")
        main_app_dir = Path(settings.BASE_DIR) / "example_project"

        # component
        wrong_component_path = main_app_dir / 'silica' / "some/Sub-folder/some-component.py"
        expected_component_path = main_app_dir / 'silica' / "some/sub-folder/SomeComponent.py"
        self.files.append(expected_component_path)
        self.files.append(wrong_component_path)

        # template
        wrong_template_path = main_app_dir / 'templates' / 'silica' / "some/Sub-folder/some-component.html"
        expected_template_path = main_app_dir / 'templates' / 'silica' / "some/sub-folder/some_component.html"
        self.files.append(expected_template_path)
        self.files.append(wrong_template_path)

        self.assertTrue(expected_component_path.exists())
        self.assertTrue(expected_template_path.exists())


    def test_command_allows_pascal_case(self):
        call_command('silica', 'create', "some.Sub-folder.SomeComponent", "--silent")
        main_app_dir = Path(settings.BASE_DIR) / "example_project"

        # component
        wrong_component_path = main_app_dir / 'silica' / "some/Sub-folder/some-component.py"
        expected_component_path = main_app_dir / 'silica' / "some/sub-folder/SomeComponent.py"
        self.files.append(expected_component_path)
        self.files.append(wrong_component_path)

        # template
        wrong_template_path = main_app_dir / 'templates' / 'silica' / "some/Sub-folder/some-component.html"
        expected_template_path = main_app_dir / 'templates' / 'silica' / "some/sub-folder/some_component.html"
        self.files.append(expected_template_path)
        self.files.append(wrong_template_path)

        self.assertTrue(expected_component_path.exists())
        self.assertTrue(expected_template_path.exists())


    def test_single_word_component_is_capitalized(self):
        call_command('silica', 'create', "some.folder.component", "--silent")
        main_app_dir = Path(settings.BASE_DIR) / "example_project"

        # component
        wrong_component_path = main_app_dir / 'silica' / "some/folder/component.py"
        expected_component_path = main_app_dir / 'silica' / "some/folder/Component.py"
        self.files.append(expected_component_path)
        self.files.append(wrong_component_path)

        # template
        expected_template_path = main_app_dir / 'templates' / 'silica' / "some/folder/component.html"
        self.files.append(expected_template_path)

        self.assertTrue(expected_component_path.exists())
        self.assertTrue(expected_template_path.exists())
