# JelkaSim
Simulation for jelka

# Building and publishing a package
You can build the package by running the following command in the same directory as pyproject.toml:
```sh
python3 -m build
```
Output should be located in dist directory:
```
dist/
├── jelka_validator-version-something.whl
└── jelka_validator-version.tar.gz
```
To securely upload your project, you’ll need a PyPI API token. It can be created here for TestPyPI and here for PyPI.

Run Twine to upload all of the archives under dist:
```sh
python3 -m twine upload dist/*
```
You will be prompted for a username and password. For the username, use token. For the password, use the token value, including the pypi- prefix.