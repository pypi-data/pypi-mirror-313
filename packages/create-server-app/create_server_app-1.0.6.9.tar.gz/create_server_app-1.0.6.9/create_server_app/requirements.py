import os
import subprocess
import pkg_resources
import re

def create_requirements_file(project_name):
    def parse_requirement(req_line):
        """
        Parse a requirement string to extract the package name and version constraint.
        Handles cases like:
        - Flask
        - pytest>=8.0.0
        - pymongo==4.8.0
        """
        match = re.match(r"([a-zA-Z0-9\-_]+)([><=~!]*.*)?", req_line.strip())
        if match:
            package = match.group(1)
            version = match.group(2) or ""
            return package, version
        return None, None

    # Create a requirements.txt for the project
    requirements_content = """Flask==3.0.3
pytest==8.3.3
pytest-cov==6.0.0
pymongo==4.8.0
pydantic
"""
    requirements_path = os.path.join(project_name, 'requirements.txt')
    with open(requirements_path, 'w') as f:
        f.write(requirements_content)

    try:
        with open(requirements_path) as req_file:
            requirements = req_file.readlines()

        installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
        to_install = []

        for req in requirements:
            req = req.strip()
            if not req or req.startswith("#"):
                continue

            pkg_name, version_constraint = parse_requirement(req)
            if not pkg_name:
                print(f"Skipping invalid requirement line: {req}")
                continue

            if pkg_name.lower() in installed_packages:
                installed_version = installed_packages[pkg_name.lower()]
                if version_constraint:
                    if not pkg_resources.Requirement.parse(req).specifier.contains(installed_version, prereleases=True):
                        print(f"'{pkg_name}' does not satisfy '{version_constraint}'. Adding to install list.")
                        to_install.append(req)
                    else:
                        print(f"'{pkg_name} ({installed_version})' satisfies '{version_constraint}'. Skipping.")
                else:
                    print(f"'{pkg_name} ({installed_version})' is installed with no specific constraint. Skipping.")
            else:
                print(f"'{pkg_name}' is not installed. Adding to install list.")
                to_install.append(req)

        if to_install:
            subprocess.check_call([os.sys.executable, "-m", "pip", "install"] + to_install)
            print("Requirements installed/updated successfully!")
        else:
            print("All required packages are already installed.")
    except subprocess.CalledProcessError as e:
        print("Failed to install requirements.")
        print(f"Error: {e}")