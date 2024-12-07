import sys

if len(sys.argv) == 1:
    print("please enter a module_name eg. python -m create_pypi_skeleton mymodulename")
    exit()

from create_pypi_skeleton import create_pypi_skeleton

if __name__ == "__main__":
    module_name: str = sys.argv[1]
    create_pypi_skeleton(module_name)
