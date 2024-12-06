import os
from create_server_app import mongoDb, AppConfig, app, requirements, objects, test_functions, vscodeTasks, updateSchema, conftest, utils, create_nextjs, dataChecker, schemas

def create_server_project():
    # Define the directory structure for the project
    server = os.path.join('server')
    client = os.path.join('client')
    vscode = os.path.join('.vscode')
    dirs = [
        server,
        client,
        vscode,
    ]
    # Create directories
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)

    # Create the app.py file
    app.create_app_routes(server)

    # create an AppConfig for the project
    AppConfig.create_app_config(server)

    # create a requirements file
    requirements.create_requirements_file(server)

    # create a mongoDb file
    mongoDb.create_mongoDb(server)

    # create an objects file
    objects.create_objects_file(server)

    # Create a basic test file in the tests folder
    test_functions.create_test_functions_file(server)

    # Create a vscode tasks directory
    vscodeTasks.create_vscode_tasks()

    # Create a schema update file
    updateSchema.create_update_schema_file(server)

    # Create a conftest file
    conftest.create_conftest_file(server)

    # Create a utils file
    utils.create_utils_file(server)

    # Create a dataChecker file
    dataChecker.create_data_checker_file(server)

    # Create a schemas folder
    schemas.create_schemas_folder(server)

    # Create a client app
    create_nextjs.create_next(client)

    # Create README.md with basic instructions
    readme_content = f"# \n\nA simple Flask server template with MongoDB integration."
    with open(os.path.join( 'README.md'), 'w') as f:
        f.write(readme_content)

    print(f"Project created successfully!")

if __name__ == '__main__':
    #  = input("Enter the project name: ")
    create_server_project()
