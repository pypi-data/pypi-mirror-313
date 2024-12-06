import os
from datetime import datetime
import pyfiglet
from termcolor import colored
from colorama import init

init(autoreset=True)


class BoaHancock:
    def __init__(self, project_name, author):
        self.project_name = project_name
        self.author = author
        self.project_path = os.path.join(os.getcwd(), project_name)
        self.template_path = os.path.join(os.path.dirname(__file__), "templates")

    def create_project_structure(self):
        """
        Create the folder structure for the project.
        """
        os.makedirs(self.project_path, exist_ok=True)
        os.makedirs(os.path.join(self.project_path, f"{self.project_name}"), exist_ok=True)
        os.makedirs(os.path.join(self.project_path, "test"), exist_ok=True)
        print(colored(f"Project structure created at {self.project_path}"), "green")

    def generate_file(self, file_name, content):
        """
        Generate a file with specific content
        """
        file_path = os.path.join(self.project_path, file_name)
        with open(file_path, "w") as f:
            f.write(content)
        print(colored(f"File {file_name} created.", "green"))

    def generate_license(self, license_type):
        """
        Generate a LICENSE file based on selected license_type
        """
        license_file = os.path.join(self.template_path, "LICENSE", f"{license_type}.txt")
        if not os.path.exists(license_file):
            raise ValueError(colored(f"License type {license_type} is not supported.", "red"))

        with open(license_file, "r") as f:
            license_content = f.read().format(year=datetime.now().year, author=self.author)

        self.generate_file("LICENSE", license_content)

    def generate_gitignore(self):
        """
        Generate a .gitignore file from the template.
        """
        gitignore_template = os.path.join(self.template_path, ".gitignore")
        if not os.path.exists(gitignore_template):
            raise FileNotFoundError(colored(".gitignore template not found in templates directory.", "yellow"))

        with open(gitignore_template, "r") as f:
            gitignore_content = f.read()

        self.generate_file(".gitignore", gitignore_content)

    def generate_init(self):
        """
        Generate __init__.py file in the src folder.
        """
        init_template = os.path.join(self.template_path, "__init__.py")
        src_folder = os.path.join(self.project_path, f"{self.project_name}")

        if not os.path.exists(init_template):
            raise FileNotFoundError("__init__ Pro.py template not found in templates directory.")

        with open(init_template, "r") as f:
            init_content = f.read()

        init_file = os.path.join(src_folder, "__init__.py")
        with open(init_file, "w") as f:
            f.write(init_content)
        print(colored("__init__.py created in src folder.", "green"))

    def generate_readme(self):
        """
        Generate a README.md file.
        """
        readme_content = f"# {self.project_name}\n\nA Python project created using Boa Generator."
        self.generate_file("README.md", readme_content)

    def generate_setup(self):
        """
        Generate a setup.py file for the project using a template.
        """
        setup_template = os.path.join(self.template_path, "setup.py")

        if not os.path.exists(setup_template):
            raise FileNotFoundError("setup.py template not found in templates directory.")

        with open(setup_template, "r") as f:
            setup_content = f.read()

        setup_content = setup_content.format(
            project_name=self.project_name,
            author=self.author
        )

        self.generate_file("setup.py", setup_content)

    def create_project(self, license_type):
        """
        Generate the full project.
        """
        self.create_project_structure()
        self.generate_license(license_type)
        self.generate_readme()
        self.generate_setup()
        self.generate_gitignore()
        self.generate_init()


def get_license_choice():
    """
    Display the available licenses from the LICENSE folder.
    """
    license_folder = os.path.join(os.path.dirname(__file__), "templates", "LICENSE")

    available_licenses = [f.replace(".txt", "") for f in os.listdir(license_folder) if f.endswith(".txt")]

    if not available_licenses:
        raise FileNotFoundError("No license templates found in the LICENSE folder.")

    print("Select a License for your project:")
    for idx, license in enumerate(available_licenses, 1):
        print(colored(f"{idx}. {license}", "green"))

    choice = input("Enter the number of the selected license (1-{}): ".format(len(available_licenses)))

    try:
        choice = int(choice)
        if 1 <= choice <= len(available_licenses):
            selected_license = available_licenses[choice - 1]
            return selected_license
        else:
            print("Invalid choice, please select a number between 1 and {}.".format(len(available_licenses)))
            return get_license_choice()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return get_license_choice()


def main():
    ascii_art = pyfiglet.figlet_format("Boa Hancock")
    print(colored(ascii_art, "cyan"))
    print(colored("This is a tool for generating starter templates to create libraries or modules in Python", "blue"))
    print(f"You can see details at {colored('pypi.org', 'blue')} about this tool")
    print(colored(f"And you can follow my GitHub {colored('github.com/Anammkh/boaHancock', 'blue')}", "yellow"))
    print(colored("TETAP SHOLAT, AND THANK YOU", "magenta"))

    project_name = input("\n\nEnter the project name: ")
    author_name = input("Enter the author name: ")
    license_type = get_license_choice()

    project = BoaHancock(project_name=project_name, author=author_name)

    try:
        project.create_project(license_type=license_type)
        print(f"Project '{project_name}' created successfully!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
