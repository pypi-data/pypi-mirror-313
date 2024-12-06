import unittest
import os
import tempfile
import shutil
from easyprojectstructure.__main__ import is_excluded, get_project_structure


class TestEasyProjectStructure(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory structure
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, "__pycache__"))
        with open(os.path.join(self.test_dir, "test.py"), "w") as f:
            f.write("# test file")
        with open(os.path.join(self.test_dir, "test.pyc"), "w") as f:
            f.write("")
        with open(os.path.join(self.test_dir, "test.txt"), "w") as f:
            f.write("Sample text")
        os.makedirs(os.path.join(self.test_dir, "build"))
        os.makedirs(os.path.join(self.test_dir, "src"))
        with open(os.path.join(self.test_dir, "src", "main.py"), "w") as f:
            f.write('print("Hello World")')

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_is_excluded(self):
        # Test exclusion of patterns
        self.assertTrue(is_excluded("__pycache__", self.test_dir, self.test_dir))
        self.assertTrue(is_excluded("test.pyc", self.test_dir, self.test_dir))
        self.assertFalse(is_excluded("test.py", self.test_dir, self.test_dir))

    def test_get_project_structure(self):
        # Capture the output of get_project_structure
        from io import StringIO
        import sys

        captured_output = StringIO()
        sys.stdout = captured_output
        get_project_structure(
            self.test_dir, os.path.dirname(self.test_dir), root_input=self.test_dir
        )
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        expected_output = os.path.basename(self.test_dir) + "/\n"
        expected_output += "    src/\n"
        expected_output += "        main.py\n"
        expected_output += "    test.py\n"
        expected_output += "    test.txt\n"
        self.assertEqual(output.strip(), expected_output.strip())


if __name__ == "__main__":
    unittest.main()
