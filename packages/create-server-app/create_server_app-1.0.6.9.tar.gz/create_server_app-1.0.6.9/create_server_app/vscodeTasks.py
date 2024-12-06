import os

def create_vscode_tasks():
    vscode_tasks_content = """{
    "version": "2.0.0",
    "tasks": [
      {
        "label": "Activate venv",
        "type": "shell",
        "command": "ven\\\\Script\\\\activate",
        "options": {
          "cwd": "${workspaceFolder}\\\\server",
          "shell": {
            "executable": "cmd.exe",
            "args": [
              "/c"
            ]
          }
        },
        "presentation": {
          "echo": true,
          "reveal": "always",
          "focus": false,
          "panel": "shared"
        },
        "problemMatcher": []
      },
      {
        "label": "Server app.py",
        "type": "shell",
        "command": "ven\\\\Script\\\\activate && python app.py",
        "options": {
          "cwd": "${workspaceFolder}\\\\server",
          "shell": {
            "executable": "cmd.exe",
            "args": [
              "/c"
            ]
          }
        },
        "presentation": {
          "echo": true,
          "reveal": "always",
          "focus": true,
          "panel": "shared"
        },
        "problemMatcher": [],
        "detail": "Activate virtual environment and run python app.py"
      },
      {
        "label": "pytest",
        "type": "shell",
        "command": "ven\\\\Script\\\\activate && pytest --cov=objects --cov-report=term-missing",
        "options": {
          "cwd": "${workspaceFolder}\\\\server",
          "shell": {
            "executable": "cmd.exe",
            "args": [
              "/c"
            ]
          }
        },
        "presentation": {
          "echo": true,
          "reveal": "always",
          "focus": true,
          "panel": "shared"
        },
        "problemMatcher": [],
        "detail": "Activate virtual environment and run python app.py"
      },
      {
        "label": "Client npm run dev",
        "type": "shell",
        "command": "netlify dev",
        "options": {
          "cwd": "${workspaceFolder}\\\\Client\\\\accounting",
          "shell": {
            "executable": "cmd.exe",
            "args": [
              "/c"
            ]
          }
        },
        "presentation": {
          "echo": true,
          "reveal": "always",
          "focus": true,
          "panel": "shared"
        },
        "problemMatcher": [],
        "detail": "Activate virtual environment and run npm run dev"
      },
      {
        "label": "Client npm run test App",
        "type": "shell",
        "command": "npm run test App",
        "options": {
          "cwd": "${workspaceFolder}\\\\client\\\\accounting",
          "shell": {
            "executable": "cmd.exe",
            "args": [
              "/c"
            ]
          }
        },
        "presentation": {
          "echo": true,
          "reveal": "always",
          "focus": true,
          "panel": "shared"
        },
        "problemMatcher": [],
        "detail": "Activate virtual environment and run npm run dev"
      }
    ]
}
"""

    vscode_launch_content = """{
    "version": "0.2.0",
    "configurations": [
    {
        "name": "Server Debug app.py",
        "type": "debugpy",
        "request": "launch",
        "program": "${workspaceFolder}/server/app.py",
        "console": "integratedTerminal",
        "preLaunchTask": "Activate venv"
        },
        {
            "name": "Client debug test App",
            "type": "node",
            "request": "launch",
            "runtimeExecutable": "bash",
            "runtimeArgs": [
              "-c",
              "cd client/accounting && npm run test App"
            ],
            "console": "integratedTerminal",
            "internalConsoleOptions": "neverOpen"
          },
          {
            "name": "Launch Chrome against localhost",
            "type": "chrome",
            "request": "launch",
            "url": "http://localhost:5173",
            "webRoot": "${workspaceFolder}/src",
            "sourceMaps": true,
            "trace": true,
            "sourceMapPathOverrides": {
              "webpack:///src/*": "${webRoot}/*"
            }
          }
    ]
  }
"""
    with open(os.path.join('.vscode', 'launch.json'), 'w') as f:
        f.write(vscode_launch_content)
    
    with open(os.path.join('.vscode', 'tasks.json'), 'w') as f:
        f.write(vscode_tasks_content)