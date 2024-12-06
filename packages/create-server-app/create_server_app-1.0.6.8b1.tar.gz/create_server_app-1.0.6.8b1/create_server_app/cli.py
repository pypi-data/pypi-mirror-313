import argparse
from create_server_app import create_server

def main():
    # parser = argparse.ArgumentParser(description="Create a server app project.")
    # parser.add_argument("name", type=str, help="The name of your project folder.")
    # args = parser.parse_args()

    create_server.create_server_project()

if __name__ == "__main__":
    main()
