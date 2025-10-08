# Contributing to EarthquakesParser

Thank you for considering contributing to EarthquakesParser! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Setting Up Development Environment

1. **Fork and clone the repository**

```bash
git clone https://github.com/yourusername/earthquakes-parser.git
cd earthquakes-parser
```

2. **Install uv** (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Set up virtual environment and install dependencies**

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

4. **Verify installation**

```bash
pytest
```

## Development Workflow

### Creating a Branch

Create a feature branch for your work:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### Making Changes

1. Make your changes in the appropriate module
2. Add/update tests in the `tests/` directory
3. Update documentation if needed
4. Run tests and code quality checks

### Code Quality

Before committing, ensure your code passes all checks:

```bash
# Run tests
uv run pytest

# Format code
uv run black earthquakes_parser tests sandbox

# Sort imports
uv run isort earthquakes_parser tests sandbox

# Lint code
uv run flake8 earthquakes_parser tests

# Check docstring coverage
uv run interrogate earthquakes_parser
```

Or run all checks at once:

```bash
uv run pytest && \
uv run black --check earthquakes_parser tests && \
uv run isort --check-only earthquakes_parser tests && \
uv run flake8 earthquakes_parser tests && \
uv run interrogate -v earthquakes_parser
```

### Writing Tests

- Place tests in the `tests/` directory
- Follow the naming convention: `test_*.py`
- Use descriptive test names: `test_<functionality>_<scenario>`
- Aim for high test coverage (>80%)

Example:

```python
def test_search_with_site_filter():
    """Test search with site filter."""
    searcher = KeywordSearcher(delay=0.1)
    results = searcher.search("earthquake", site_filter="instagram.com")
    assert all("instagram.com" in r.link for r in results)
```

### Commit Guidelines

Follow conventional commit format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

Example:

```bash
git commit -m "feat: add support for custom user agents in parser"
git commit -m "fix: handle empty search results gracefully"
git commit -m "docs: update README with S3 storage examples"
```

### Submitting a Pull Request

1. **Push your branch**

```bash
git push origin feature/your-feature-name
```

2. **Create a Pull Request** on GitHub

3. **Fill out the PR template** with:
   - Description of changes
   - Related issues
   - Testing performed
   - Checklist completion

4. **Wait for review** - maintainers will review your PR and may request changes

5. **Address feedback** - make requested changes and push updates

6. **Merge** - once approved, a maintainer will merge your PR

## Code Style

### Python Style

- Follow PEP 8 guidelines
- Use Black for formatting (line length: 88)
- Use type hints where appropriate
- Write docstrings for all public functions/classes

### Documentation Style

Use Google-style docstrings:

```python
def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
    """Perform a search for a given query.

    Args:
        query: The search query.
        max_results: Maximum number of results to return.

    Returns:
        List of SearchResult objects.

    Raises:
        ValueError: If query is empty.
    """
```

## Project Structure

```
earthquakes-parser/
├── earthquakes_parser/     # Main package
│   ├── search/            # Search functionality
│   ├── parser/            # Content parsing
│   └── storage/           # Storage backends
├── tests/                 # Test suite
├── sandbox/               # Experiments and examples
├── .github/               # GitHub Actions workflows
└── docs/                  # Documentation (future)
```

## Testing Guidelines

### Unit Tests

- Test individual functions/methods in isolation
- Use mocking for external dependencies
- Test edge cases and error conditions

### Integration Tests

- Test components working together
- Use fixtures for setup/teardown
- Test realistic scenarios

### Running Specific Tests

```bash
# Run specific test file
uv run pytest tests/test_searcher.py

# Run specific test function
uv run pytest tests/test_searcher.py::test_search_without_filter

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=earthquakes_parser
```

## Documentation

### Updating Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md for all changes
- Add docstrings to new functions/classes
- Update examples in sandbox/ if needed

### Building Documentation (Future)

```bash
# When documentation is set up
cd docs
make html
```

## Release Process

See [RELEASE_POLICY.md](RELEASE_POLICY.md) for the complete release process.

## Getting Help

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers at [email]

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing others' private information
- Unprofessional conduct

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- CHANGELOG.md for significant contributions
- Future documentation

Thank you for contributing! 🎉
