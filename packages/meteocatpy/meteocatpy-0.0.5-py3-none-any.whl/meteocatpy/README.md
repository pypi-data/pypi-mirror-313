# Meteocat Python Package for Meteocat Home Assistant Integration

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python version compatibility](https://img.shields.io/pypi/pyversions/meteocatpy)](https://pypi.org/project/meteocatpy)
[![pipeline status](https://gitlab.com/figorr/meteocatpy/badges/master/pipeline.svg)](https://gitlab.com/figorr/meteocatpy/commits/master)


`meteocatpy` is a Python package to interact with the Meteocat API. Allows you to obtain meteorological data and lists of municipalities from the Meteocat API.

**NOTE:** Meteocat API requires to use an API_KEY, you should ask to (https://apidocs.meteocat.gencat.cat/documentacio/acces-ciutada-i-administracio/)

# Installation

You can install the package from PyPI using `pip`:
```bash
pip install meteocatpy
```

```bash
from meteocatpy.town import MeteocatTown

# Replace 'tu_api_key' with your actual API key
API_KEY = "tu_api_key"
town_client = MeteocatTown(API_KEY)

# Get a list of municipalities (asynchronous call)
municipios_data = await town_client.get_municipis()
print(municipis)
```

# Credits

This is a personal project.

Authors:
- Figorr

# Contributing

If you would like to contribute to this project, please open an issue or create a pull request. I'd be happy to review your contributions!

1.  [Check for open features/bugs](https://gitlab.com/figorr/meteocatpy/issues)
    or [initiate a discussion on one](https://gitlab.com/figorr/meteocatpy/issues/new).
2.  [Fork the repository](https://gitlab.com/figorr/meteocatpy/forks/new).
3.  Install the dev environment: `make init`.
4.  Enter the virtual environment: `pipenv shell`
5.  Code your new feature or bug fix.
6.  Write a test that covers your new functionality.
7.  Update `README.md` with any new documentation.
8.  Run tests and ensure 100% code coverage for your contribution: `make coverage`
9.  Ensure you have no linting errors: `make lint`
10. Ensure you have typed your code correctly: `make typing`
11. Add yourself to `AUTHORS.md`.
12. Submit a pull request!

# License

[Apache-2.0](LICENSE). By providing a contribution, you agree the contribution is licensed under Apache-2.0.

# API Reference

[See the docs 📚](https://apidocs.meteocat.gencat.cat/section/informacio-general/).