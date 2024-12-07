# OpenAPI CLI Generator

A command line utility that automatically generates Python CLIs from OpenAPI v3.x specifications. This tool allows you to interact with any OpenAPI-compliant API through an intuitive command-line interface.

## Features

- 🚀 Automatic CLI generation from OpenAPI v3.x specs
- 🔄 Support for all standard HTTP methods (GET, POST, PUT, DELETE, etc.)
- 🏷️ Alias management for easy access to multiple APIs
- 📝 Interactive help and documentation
- ✨ Automatic request/response handling
- 🔍 Parameter validation and type conversion

## Installation

```bash
# Install from PyPI
pip install openapi-cli

# Install from source
git clone https://github.com/yourusername/openapi-cli-generator.git
cd openapi-cli-generator
make install
```

## Quick Start

1. Add an API alias:
```bash
openapi_cli alias add http://example.com/api/v1/openapi.json example
```

2. Use the generated CLI:
```bash
# Show available commands
openapi_cli example --help

# List resources
openapi_cli example users list

# Create a new resource
openapi_cli example users create --data '{"name": "John Doe"}'
```

## API Management Commands

### Alias Management
```bash
# Add a new API alias
openapi_cli alias add http://example.com/api/v1/openapi.json example

# List all configured aliases
openapi_cli alias list

# Show details for a specific alias
openapi_cli alias show example

# Update an existing alias
openapi_cli alias update example http://new-url.com/api/v1/openapi.json

# Remove an alias
openapi_cli alias remove example
```

## Development

### Prerequisites
- Python 3.7+
- Make (for development commands)

### Setup Development Environment
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
make install-dev
```

### Development Commands
```bash
# Run tests
make test

# Run linting
make lint

# Run type checking
make typecheck

# Format code
make format
```

### Pre-commit Hooks
We use pre-commit hooks to ensure code quality. Install them with:
```bash
pre-commit install
```

The following checks are run on each commit:
- Code formatting (Black)
- Import sorting (isort)
- Style checking (Flake8)
- YAML/JSON validation
- End-of-file fixing
- Trailing whitespace removal

## Dependencies

- Python 3.7+
- PyYAML >= 6.0
- Requests >= 2.31.0
- OpenAPI Spec Validator >= 0.5.1
- Click >= 8.1.3

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
