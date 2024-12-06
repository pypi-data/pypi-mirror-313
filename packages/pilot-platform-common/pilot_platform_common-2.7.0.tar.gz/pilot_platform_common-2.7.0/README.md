# common

[![Run Tests](https://github.com/PilotDataPlatform/common/actions/workflows/run-tests.yml/badge.svg?branch=develop)](https://github.com/PilotDataPlatform/common/actions/workflows/run-tests.yml)
[![Python](https://img.shields.io/badge/python-3.10-brightgreen.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/pilot-platform-common.svg)](https://pypi.org/project/pilot-platform-common/)

Importable package responsible for cross-service tasks within the Pilot Platform (e.g. logging, Vault connection, etc.).


## Getting Started

### Installation & Quick Start
The latest version of the common package is available on [PyPi](https://pypi.org/project/pilot-platform-common/) and can be installed into another service via Pip.

Pip install from PyPi:
```
pip install pilot-platform-common
```

In `pyproject.toml`:
```
pilot-platform-common = "^<VERSION>"
```

Pip install from a local `.whl` file:
```
pip install pilot_platform_common-<VERSION>-py3-none-any.whl
```

## Contribution

You can contribute the project in following ways:

* Report a bug.
* Suggest a feature.
* Open a pull request for fixing issues or adding functionality. Please consider using [pre-commit](https://pre-commit.com) in this case.
* For general guidelines on how to contribute to the project, please take a look at the [contribution guide](CONTRIBUTING.md).
