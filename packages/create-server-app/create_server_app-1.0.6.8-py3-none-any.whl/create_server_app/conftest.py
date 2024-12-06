import os

def create_conftest_file(server):
    conftest_content = """import pytest
from AppConfig import AppConfig  # Adjust the import path according to your project structure


def pytest_configure(config):
    app_config = AppConfig()

    if app_config.getIsProductionEnvironment():
        pytest.exit("Production environment is set. Skipping tests.")
"""

    conftest_path = os.path.join(server, 'conftest.py')
    with open(conftest_path, 'w') as f:
        f.write(conftest_content)