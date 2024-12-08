# Validator
Decoder for data stream sent to x-mas tree and simulation.

## Development
This is a compact version of [https://packaging.python.org/en/latest/tutorials/packaging-projects/](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

Some of the commands require a newer version of pip, so start by making sure you have the latest version installed:
```sh
python3 -m pip install --upgrade pip
```
Make sure you have the latest version of PyPA’s build installed:
```sh
python3 -m pip install --upgrade build
```
You need twine to upload package to the index.
```sh
python3 -m pip install --upgrade twine
```

Do NOT use `requirements.txt` for package dependencies. It should
be used for development requirements.
Similarly `README.md` is for GitHub. To update what people see
on index change `PackageREADME.md`.

It is reasonable to support Python 3.8 and above. Fo this reason do
not use type hints with subscripts (For example: `l: list[int] = []`).

### Building and publishing a package
You can build the package by running the following command in the 
same directory as `pyproject.toml`:
```sh
python3 -m build
```
Output should be located in `dist` directory:
```
dist/
├── jelka_validator-version-something.whl
└── jelka_validator-version.tar.gz
```

To securely upload your project, you’ll need a PyPI API token.
It can be created [here](https://test.pypi.org/manage/account/#api-tokens) for TestPyPI
and [here](https://pypi.org/manage/account/#api-tokens) for PyPI.

Run Twine to upload all of the archives under dist:
```sh
python3 -m twine upload dist/*
```
You will be prompted for a username and password. For the 
username, use __token__. For the password, use the token value, 
including the pypi- prefix.

To install library from the PyPi you ca use:
```
python3 -m pip install jelka-validator

To install library from the TestPyPi you ca use:
```sh
python3 -m pip install --index-url https://test.pypi.org/simple/ jelka-validator --extra-index-url https://pypi.org/simple poirot
```

# Linting and testing
To run the linter you can use:
```sh
ruff check
```
Replace `check` to tell the formatter to fix your code.

To typecheck the code use:
```sh
pyright
```
and to run tests:
```sh
pytest --doctest-modules --ignore=test/test_cppsim.py --ignore=test/test_pysim.py
```

To test things manually use the following command at toplevel:
```sh
pip install -e .
```
Then you can run `test_cpp.py` and `test_pysim.py` inside `test/` directory.
