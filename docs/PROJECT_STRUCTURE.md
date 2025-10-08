# Project Structure

## Directory Layout

```
earthquakes-parser/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # CI pipeline (tests, linting)
│   │   ├── release.yml         # Release automation
│   │   └── codeql.yml          # Security scanning
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md       # Bug report template
│   │   └── feature_request.md  # Feature request template
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── dependabot.yml          # Dependency updates
│
├── earthquakes_parser/          # Main library package
│   ├── __init__.py
│   ├── search/
│   │   ├── __init__.py
│   │   └── searcher.py         # Keyword search functionality
│   ├── parser/
│   │   ├── __init__.py
│   │   └── content_parser.py   # Content extraction & LLM cleaning
│   └── storage/
│       ├── __init__.py
│       ├── base.py             # Storage backend interface
│       ├── csv_storage.py      # CSV storage implementation
│       └── s3_storage.py       # S3 storage implementation
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_searcher.py
│   ├── test_parser.py
│   └── test_storage.py
│
├── sandbox/                     # Experimentation area
│   ├── README.md
│   ├── example_search.py
│   └── example_parser.py
│
├── main.py                      # Original search script (preserved)
├── test1-1.py                   # Original parser script (preserved)
├── keywords.txt                 # Keywords for searching
├── requirements.txt             # Original requirements (preserved)
│
├── pyproject.toml               # Project configuration
├── .python-version              # Python version
├── .flake8                      # Flake8 configuration
├── .gitignore                   # Git ignore rules
│
├── README.md                    # Main documentation
├── QUICK_START.md               # Quick start guide
├── CONTRIBUTING.md              # Contribution guidelines
├── RELEASE_POLICY.md            # Release process
├── CHANGELOG.md                 # Version history
├── LICENSE                      # MIT License
└── PROJECT_STRUCTURE.md         # This file
```

## Module Descriptions

### `earthquakes_parser/search/`

**Purpose**: Web search functionality using DuckDuckGo

- `KeywordSearcher`: Main search class
  - Search by keywords
  - Site-specific filtering (e.g., Instagram)
  - Batch processing
  - Export to DataFrame

### `earthquakes_parser/parser/`

**Purpose**: Content extraction and cleaning

- `ContentParser`: Content processing class
  - Extract text with trafilatura
  - Clean with LLM (transformers)
  - Block-wise processing for large content
  - Batch URL parsing

### `earthquakes_parser/storage/`

**Purpose**: Flexible storage backends

- `StorageBackend`: Abstract interface
- `CSVStorage`: Local CSV file storage
- `S3Storage`: AWS S3 storage (future-ready)

## Key Files

### Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Package metadata, dependencies, tool configs |
| `.flake8` | Linting rules |
| `.python-version` | Python version specification |
| `.gitignore` | Git ignore patterns |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Main documentation and usage guide |
| `QUICK_START.md` | Quick start guide for new users |
| `CONTRIBUTING.md` | Developer contribution guidelines |
| `RELEASE_POLICY.md` | Release process and versioning |
| `CHANGELOG.md` | Version history and changes |

### CI/CD

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | Test, lint, coverage on push/PR |
| `.github/workflows/release.yml` | Automated releases on tag push |
| `.github/workflows/codeql.yml` | Security scanning |
| `.github/dependabot.yml` | Automated dependency updates |

## Design Principles

### 1. Modularity
Each component (search, parser, storage) is independent and can be used separately.

### 2. Extensibility
Storage backends follow an abstract interface, making it easy to add new backends (e.g., MongoDB, PostgreSQL).

### 3. Backward Compatibility
Original scripts (`main.py`, `test1-1.py`) are preserved and still functional.

### 4. Modern Tooling
- **uv**: Fast package manager
- **pytest**: Modern testing framework
- **black/isort/flake8**: Code quality
- **GitHub Actions**: CI/CD automation

### 5. Future-Ready
- S3 storage prepared for cloud deployment
- Extensible architecture
- Type hints for better IDE support

## Data Flow

```
Keywords (keywords.txt)
    ↓
KeywordSearcher → Search Results (DataFrame)
    ↓
CSVStorage.save() → CSV File
    ↓
CSVStorage.load() → DataFrame
    ↓
ContentParser → Parsed Content (List[dict])
    ↓
CSVStorage.save() → JSON File
```

## Testing Strategy

- **Unit Tests**: Test individual functions with mocking
- **Integration Tests**: Test component interactions
- **Coverage Target**: >80%
- **CI Pipeline**: Automated on every push

## Release Workflow

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit and create git tag: `git tag v0.1.0`
4. Push tag: `git push origin v0.1.0`
5. GitHub Actions automatically creates release

## Future Enhancements

- [ ] MongoDB storage backend
- [ ] PostgreSQL storage backend
- [ ] Async processing support
- [ ] CLI interface
- [ ] Web dashboard
- [ ] Real-time monitoring
- [ ] Publish to PyPI

