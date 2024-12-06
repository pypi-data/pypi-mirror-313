import os
import shutil
import unittest
from datetime import datetime
from Boa.generator import BoaHancock


class TestBoaHancock(unittest.TestCase):

    def setUp(self):
        """
        Setup test environment before each test.
        """
        self.project_name = "TestProject"
        self.author = "TestAuthor"
        self.generator = BoaHancock(self.project_name, self.author)
        self.license_type = "mit"
        if os.path.exists(self.project_name):
            shutil.rmtree(self.project_name)

    def tearDown(self):
        """
        Clean up test environment after each test.
        """
        if os.path.exists(self.project_name):
            shutil.rmtree(self.project_name)

    def test_create_project_structure(self):
        """
        Test if the project structure is created correctly.
        """
        self.generator.create_project_structure()
        self.assertTrue(os.path.exists(self.project_name))
        self.assertTrue(os.path.exists(os.path.join(self.project_name, "src")))
        self.assertTrue(os.path.exists(os.path.join(self.project_name, "test")))

    def test_generate_license(self):
        """
        Test if the LICENSE file is generated correctly.
        """
        self.generator.create_project_structure()
        self.generator.generate_license(self.license_type)
        license_path = os.path.join(self.project_name, "LICENSE")
        self.assertTrue(os.path.exists(license_path))
        with open(license_path, "r") as f:
            content = f.read()
        self.assertIn("MIT License", content)
        self.assertIn(str(datetime.now().year), content)
        self.assertIn(self.author, content)

    def test_generate_readme(self):
        """
        Test if the README.md file is generated correctly.
        """
        self.generator.create_project_structure()
        self.generator.generate_readme()
        readme_path = os.path.join(self.project_name, "README.md")
        self.assertTrue(os.path.exists(readme_path))
        with open(readme_path, "r") as f:
            content = f.read()
        self.assertIn(f"# {self.project_name}", content)
        self.assertIn("A Python project created using Template Generator.", content)

    def test_generate_setup(self):
        """
        Test if the setup.py file is generated correctly.
        """
        self.generator.create_project_structure()
        self.generator.generate_setup()
        setup_path = os.path.join(self.project_name, "setup.py")
        self.assertTrue(os.path.exists(setup_path))
        with open(setup_path, "r") as f:
            content = f.read()
        self.assertIn(f"name=\"{self.project_name}\"", content)  # Verify project name in setup.py
        self.assertIn(f"author=\"{self.author}\"", content)  # Verify author name in setup.py

    def test_generate_gitignore(self):
        """
        Test if the .gitignore file is generated correctly.
        """
        self.generator.create_project_structure()
        self.generator.generate_gitignore()
        gitignore_path = os.path.join(self.project_name, ".gitignore")
        self.assertTrue(os.path.exists(gitignore_path))
        with open(gitignore_path, "r") as f:
            content = f.read()
        self.assertIn("__pycache__", content)

    def test_generate_init(self):
        """
        Test if the __init__.py file is generated correctly.
        """
        self.generator.create_project_structure()
        self.generator.generate_init()
        init_path = os.path.join(self.project_name, "src", "__init__.py")
        self.assertTrue(os.path.exists(init_path))
        with open(init_path, "r") as f:
            content = f.read()
        self.assertIn(f"# {self.project_name} module", content)


if __name__ == "__main__":
    unittest.main()

