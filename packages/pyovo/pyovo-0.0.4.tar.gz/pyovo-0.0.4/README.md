<img align="right" alt="OVOLab logo" height="168" src="/assets/ovo_logo.webp">

# PyOVO

[![PyPI](https://github.com/Ancient-Gadget-Laboratory/pyovo/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Ancient-Gadget-Laboratory/pyovo/actions/workflows/python-publish.yml)
[![LICENSE](https://img.shields.io/badge/license-MIT-blue)](https://github.com/Ancient-Gadget-Laboratory/pyovo?tab=MIT-1-ov-file)

PyOVO provides a set of tools for physical simulation and optimization. Given that we want to collect and simplify the introduction of frequently used functions in our research, this package is designed to be lightweight and easy-to-use.

## File Structure

> [!NOTE]
> The main file structure of this project is shown below. And to add one more thing, `.pypirc` restores the API token for PyPI while `pyproject.toml` is the configuration file for the package.

```bash
.
├── doc         # documentation
├── src         # package source code
│   └── pyovo
├── test        # test scripts
├── .gitignore
└── README.md
```

## Dependencies

Use the commands below to add git hooks to local git configuration.

```bash
cd .githooks
git config core.hooksPath .githooks
```

## Usage

### Publish to PyPI

> [!TIP]
> See the [tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/) by Python for more information on how to package and distribute python projects. The instructions below provides with a summary of the tutorial.

Before building and uploading the package to PyPI, make sure the package is tested. Use the command below to do that.

```bash
python -m build
python -m twine upload --repository testpypi dist/*
```

Then input the API token for TestPyPI when prompted (you may find it in [.pypirc](/.pypirc)). Once uploaded, the package should be viewable on TestPyPI at [`https://test.pypi.org/project/pyovo`](https://test.pypi.org/project/pyovo).

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps pyovo
```

After the test is passed, use the commands below to build and formally upload the package to PyPI. Remember to change the version number in [pyproject.toml](/pyproject.toml) before building the package.

```bash
python -m build
python -m twine upload dist/*
```

### Install Package

Use the command below to install the package from PyPI. You may check the package on PyPI at [`https://pypi.org/project/pyovo`](https://pypi.org/project/pyovo) for more version info.

```bash
pip install pyovo
```
