import os

def create_app_routes(project_name):
    app_py_content = """from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
"""
    with open(os.path.join(project_name, 'app.py'), 'w') as f:
        f.write(app_py_content)