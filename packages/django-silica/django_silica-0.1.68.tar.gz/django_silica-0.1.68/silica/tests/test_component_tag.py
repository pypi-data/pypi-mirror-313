from pathlib import Path
from silica.tests.SilicaTestCase import SilicaTestCase
import importlib.util
from django.test import Client


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


    def test_short_tag_can_be_called(self):
        client = Client()
        response = client.get("/silica/tests/component-tag-test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I'm component called with short name!")


    def test_components_in_subfolders_can_be_called(self):
        client = Client()
        response = client.get("/silica/tests/component-subfolder-test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I'm component in subfolder!")
