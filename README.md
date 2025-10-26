# Personal Grade Calculator (PGC)

## Overview

_Personal Grade Calculator (PGC)_ is a web-based tool designed for students who want to plan and track their academic goals without doing manual GPA calculations.

With PGC, users can easily find out what grades they need to achieve their target GPA, simply by entering:

- Desired GPA
- Current GPA (optional)
- Current semester course information

PGC will automatically calculate the required results and present them in an easy-to-understand format.

## Development Stack

PGC uses Django REST backend for calculating academic grades and storing the results. The service lets clients submit raw subject scores and credits via API endpoints, returns the calculated GPA with its corresponding letter grade, and archives each calculation for later review in the Django admin.

## Usages

Please refer to the [Documentation](#documentation) section to setup MkDocs. You can then read the full usages from there.

## Documentation

PGC uses MkDocs to create documentation webpage from markdown files, to set up the documentation page locally, follow these steps:

### 1. Install Pipenv

```sh
pip install pipenv
```

### 2. Install dependencies

```sh
pipenv sync
```

This will automatically install all dependencies required from the `Pipfile.lock` file.

### 3. Activate the virtual environment

```sh
pipenv shell
```

This will activate the virtual environment (venv) in the current shell, to check whether you're running commands from the venv, run `which pip` or `which python` (Linux/macOS).

If the path shown in the output contain `.virtualenvs/` followed by the project name, you're good to go.

### 4. Run MkDocs server locally

Run this command on the project root directory

```sh
mkdocs serve
```

This will run the MkDocs server locally, usually at <http://127.0.0.1:8000/> or other address as it shown in your shell.

You can now read the full documentation of this source code that webpage.

## Contributing

This backend is still evolving. Issues and pull requests that improve code quality, add validation, or expand the API are welcome. Please ensure any submitted changes include relevant documentation and tests where applicable.

## License

PGC is distributed under the terms of the [LICENSE](LICENSE) file included with the repository.
