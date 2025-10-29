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

## Contributing

This backend is still evolving. Issues and pull requests that improve code quality, add validation, or expand the API are welcome. Please ensure any submitted changes include relevant documentation and tests where applicable.

## License

PGC is distributed under the terms of the [LICENSE](LICENSE) file included with the repository.
