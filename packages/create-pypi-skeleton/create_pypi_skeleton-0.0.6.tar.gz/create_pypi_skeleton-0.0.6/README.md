
# create_pypi_skeleton

This module automatically creates a PyPI project skeleton for you so you don't have to do this manually.

# Installation using pip
```
pip install create-pypi-skeleton
```

# How to use (from command line)
```
python -m create_pypi_skeleton your_module_name
```

# how to use (from Python script)
```python
from create_pypi_skeleton import create_pypi_skeleton

create_pypi_skeleton("your_module_name")
```

# Sample PyPI project skeleton 

```
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
```