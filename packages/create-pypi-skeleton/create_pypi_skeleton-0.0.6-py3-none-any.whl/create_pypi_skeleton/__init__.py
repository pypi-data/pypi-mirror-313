import os
from pathlib import Path
from textwrap import dedent

def create_pypi_skeleton(
    module_name: str,
    target_path: str = ".",
    author_name: str = "YOUR_NAME",
    author_email: str = "YOUR_EMAIL",
    project_description: str = "SOME DESCRIPTION",
    project_homepage: str = "https://github.com/github_username/project_name",
    project_issues_link: str = "https://github.com/github_username/project_name/issues",  
) -> None:
    """
    Automatically creates PyPI project skeleton in the current directory

    Typical PyPI project skeleton given module_name="testing123"

    testing123/                 
        src/                    # all code goes here
            testing123/         
                __init__.py     # main folder where users import functions from
            tests/              
                main.py         # unit tests go here
            __init__.py
        .gitignore              # files/folders written here are ignored by git
        LICENSE                 # license stuff
        pyproject.toml          # contains important config stuff for PyPI
        README.md               # tells users what your project is about
        upload.py               # helper script to upload project to PyPI

    Args:
        module_name (str): name of module. This will be your folder name.
        target_path (str): where you want to create your project folder. Defualts to current directory "."
        author_name (str): your name
        author_email (str): your email
        project_description (str): one-liner description of project
        project_homepage (str): homepage of project repo eg. https://github.com/username/projectname
        project_issues_link (str): issues page of project repo eg. https://github.com/username/projectname/issues
    """
    # create required folders
    BASE_PATH: Path = Path(target_path) / module_name
    SRC_PATH: Path = BASE_PATH / 'src'
    CODE_PATH: Path = SRC_PATH / module_name
    TESTS_PATH: Path = SRC_PATH / 'tests'

    paths: list[Path] = [
        BASE_PATH,
        SRC_PATH,
        CODE_PATH,
        TESTS_PATH
    ]
    for path in paths:
        os.mkdir(path)

    # created required .py files
    with open(SRC_PATH / "__init__.py", "w") as f:
        pass

    with open(CODE_PATH / "__init__.py", "w") as f:
        pass

    with open(TESTS_PATH / "main.py", "w") as f:
        f.write(dedent("""
            import unittest

            class TestMain(unittest.TestCase):
                \"\"\"
                Unit test cases go here
                \"\"\"
                def test_something(self):
                    pass
        """))

    with open(BASE_PATH / ".gitignore", "w") as f:
        f.write(dedent("""
            __pycache__
            */__pycache__ 
            */__pycache__/*
            .DS_Store
            *.pyc
            dist/
            */dist
            venv
            */venv
        """))

    with open(BASE_PATH / "LICENSE", "w") as f:
        f.write("this is a license")

    with open(BASE_PATH / "pyproject.toml", "w") as f:
        f.write(dedent(f"""
            [build-system]
            requires = ["hatchling"]
            build-backend = "hatchling.build"

            [project]
            name = "{module_name}"
            version = "0.0.1"
            authors = [
                {{ name="{author_name}", email="{author_email}" }},
            ]
            description = "{project_description}"
            readme = "README.md"
            requires-python = ">=3.8"
            classifiers = [
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ]
            dependencies = [

            ]

            [project.urls]
            Homepage = "{project_homepage}"
            Issues = "{project_issues_link}"
        """))

    with open(BASE_PATH / "README.md", "w") as f:
        f.write(dedent(f"""
            # {module_name}

            This file is the first thing users see when they visit PyPI or github

            describe what your project does here
        """))

    with open(BASE_PATH / "upload.py", "w") as f:
        f.write(dedent(f"""
            \"\"\"
            This script:
            - edits pyproject.toml
                - finds the project version eg. 0.0.4
                - increments it by 1 eg. 0.0.5
                - if we don't do this, PyPI won't allow us to push this version
                - this is because of an "existing version conflict"
            - automatically pushes your project to PyPI
            - though you still need to key in your PyPI API key manually for security purposes
                       
            Note: you need to "pip install build twine" before running this
                - "build" allows us to build our PyPI project locally
                - "twine" allows us to upload our project to PyPI
            \"\"\"
                       
            import os
            import re

            with open('pyproject.toml') as f:
                text = f.read()

            old_version: str = re.findall('version = "(.*?)"', text)[0]     # "0.0.4"
                       
            major, minor, patch = old_version.split('.')            # major="0" minor="0" patch="4"
                       
            new_patch = int(patch) + 1
            
            new_version = f'{{major}}.{{minor}}.{{new_patch}}'      # "0.0.5"
                       
            text = re.sub(old_version, new_version, text)

            with open('pyproject.toml', 'w') as f:
                f.write(text)    

            # TODO: this works for MacOS, but might not for Windows
            commands = [
                'rm -rf ./dist',                    # removes current dist folder
                'python3 -m build',                 # build PyPI project
                'python3 -m twine upload dist/*'    # upload to PyPI
            ]

            for command in commands:
                print(command)
                os.system(command)
        """))

    print(f"successfully created PyPI project skeleton for {module_name}")
