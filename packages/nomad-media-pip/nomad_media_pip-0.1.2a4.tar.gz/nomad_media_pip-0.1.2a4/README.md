## Prerequisites
Install the following packages using pip.
```bash
pip install twine
pip install build
pip install poetry
```

## Build and Publish
To build the package, run the following command in the root directory of the project.
```bash
.\publish
```

It will prompt you to enter your username and password for PyPl. After entering the credentials, the files will be uploaded to PyPl.

If you want to set it up to not ask for your credentials every time, create a file called `.pypirc` in your home directory and add the following content to it.
```pypirc
[pypi]
username = __token__
password = pypi-<your-token>
```

## Minor and Major Version Bumps
To bump the minor version, change `patch` in `call poetry version patch` to `minor` in the `pyproject.toml` file. To bump the major version, change `patch` in `call poetry version patch` to `major` in the `pyproject.toml` file.

## Testing
To test a specific file in the test directory, run the following command in the root directory of the project.
```bash
python -m unittest test/<file-name>
```

To test all the files in the test directory, run the following command in the root directory of the project.
```bash
python -m unittest
```