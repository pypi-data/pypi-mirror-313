import os
import subprocess
import time

def validate_create_next_app():
    try:
        subprocess.run([r"C://Program Files//nodejs//npx.cmd", "create-next-app", "--version"], check=True)
        print("create-next-app is installed.")
    except subprocess.CalledProcessError as e:
        print("create-next-app is not installed.")
        print("Installing create-next-app...")
        try:
            subprocess.run([r"C://Program Files//nodejs//npm.cmd", "install", "-g", "create-next-app"], check=True)
            print("create-next-app installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install create-next-app: {e}")
            print("Please install create-next-app manually.")
            exit(1)

def create_next_app(project_dir):
    try:
        command = [r"C://Program Files//nodejs//npx.cmd", "create-next-app@latest", project_dir, "--typescript", "--eslint",
                    "--tailwind", "--app", "--no-src-dir", "--no-turbopack", "--yes"]
        subprocess.run(command, check=True)
        print(f"Successfully created Next.js app in {project_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create Next.js app: {e}")
    time.sleep(5)


def create_next(project_dir):
    validate_create_next_app()

    create_next_app(project_dir)

    time.sleep(5)

    # subprocess.run([r"C://Program Files//nodejs//npm.cmd", "run", "dev"], cwd=project_dir)


if __name__ == "__main__":
    create_next() 