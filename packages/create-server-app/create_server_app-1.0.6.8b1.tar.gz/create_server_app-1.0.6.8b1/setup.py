from setuptools import setup, find_packages

setup(
    name="create-server-app",
    version="1.0.6.8.beta-1",
    description="A CLI tool to create a server app project.",
    long_description=open("README.md").read(),
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "create-server-app=create_server_app.cli:main",
        ],
    },
    author='Michael',
    install_requires=[
        'flask',
        'pytest',
        'pytest-cov',
        'pymongo',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    url='https://github.com/FloresTristan/create-server-app'
)
