Contributing
============

If you would like to contribute to this repository please create a fork and open a pull request with your changes.
After cloning the repository run

```
pip install -e.[dev]
```

from the repositories home directory to install the required packages for developing.

Style conventions
=================

``suppy`` follows [PEP 8](https://peps.python.org/pep-0008/) for naming and [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html) for docstring convention.
To ensure uniform code we use pre-commit hooks that are managed by the pre-commit library.
For setup run:

```
pre-commit install.
```
from the home of the repository.
