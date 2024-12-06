# palcode-infrastructure

Building  the package

py -m pip install twine
py -m pip install build
py -m build --sdist
py -m build --wheel
twine upload dist/*