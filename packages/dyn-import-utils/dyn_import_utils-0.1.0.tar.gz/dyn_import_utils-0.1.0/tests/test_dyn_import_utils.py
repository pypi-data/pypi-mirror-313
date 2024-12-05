import unittest
import os
import tempfile
import shutil
import dyn_import_utils

class TestDynImporter(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test modules/packages
        self.temp_dir = tempfile.mkdtemp()

        # Create a test module
        self.module_code = "def hello(): return 'Hello, world!'"
        self.module_path = os.path.join(self.temp_dir, "test_module.py")
        with open(self.module_path, "w") as f:
            f.write(self.module_code)

        # Create a test package
        self.package_dir = os.path.join(self.temp_dir, "test_package")
        os.mkdir(self.package_dir)
        with open(os.path.join(self.package_dir, "__init__.py"), "w") as f:
            f.write(self.module_code)

    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.temp_dir)

    def test_import_module(self):
        module = dyn_import_utils.import_module(self.module_path)
        self.assertTrue(hasattr(module, "hello"))
        self.assertEqual(module.hello(), "Hello, world!")

    def test_import_package(self):
        package = dyn_import_utils.import_package(self.package_dir)
        self.assertTrue(hasattr(package, "hello"))
        self.assertEqual(package.hello(), "Hello, world!")

    def test_add_sys_path(self):
        path = self.temp_dir
        dyn_import_utils.add_sys_path(path)
        self.assertIn(path, os.sys.path)

if __name__ == "__main__":
    unittest.main()

