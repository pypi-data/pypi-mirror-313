# python-lynxlynx

## About

Shared Python library used by my scripts.

## Installation

## Development docs

https://packaging.python.org/en/latest/tutorials/packaging-projects/

### Build

```shell
python -m build
```

### Install dev version

```shell
python -m pip install --user --break-system-packages .
```

### Upload to PyPI

First build the package as per Build.

Then create the config file `~/.pypirc`:
```ini
[pypi]
	username = __token__
	password = pypi-ABCDEFGHTOKEN
```

Then upload the package:
```shell
# Testing PyPI
python -m twine upload --repository testpypi dist/*
# Prod PyPI
python -m twine upload dist/*
```
## License

AGPL-3.0-only, contact me if you need other licensing.
