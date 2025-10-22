# EarthquakesParser

A Python library for searching and parsing earthquake-related content from the web. This library provides tools for
keyword-based web searches, content extraction, and storage management with support for both CSV and S3 backends.

## Features

- 🔍 **Keyword Search**: Search for earthquake-related content using DuckDuckGo
- 📄 **Content Parsing**: Extract and clean web content using trafilatura and LLM
- 💾 **Flexible Storage**: Support for CSV files, AWS S3, and Supabase (database + object storage)
- 🧪 **Well-tested**: Comprehensive test suite with pytest
- 📦 **Modern Tooling**: Uses `uv` for fast dependency management

## Installation

### Using uv (recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/yourusername/earthquakes-parser.git
cd earthquakes-parser

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

### Using pip

```bash
pip install -e ".[dev]"
```

### For Storage Options

```bash
# For Supabase support (recommended for fake detection project)
uv pip install -e ".[supabase]"

# For AWS S3 support
uv pip install -e ".[s3]"
```

## Quick Start

### Searching for Content

```python
from earthquakes_parser import KeywordSearcher, CSVStorage

# Initialize components
searcher = KeywordSearcher(delay=1.0)
storage = CSVStorage(base_path="data")

# Load keywords from file
keywords = KeywordSearcher.load_keywords_from_file("keywords.txt")

# Search Instagram
instagram_df = searcher.search_to_dataframe(
    keywords,
    max_results=5,
    site_filter="instagram.com"
)
storage.save_dataframe(instagram_df, "instagram_results.csv")

# Search general web
web_df = searcher.search_to_dataframe(keywords, max_results=5)
storage.save_dataframe(web_df, "web_results.csv")
```

### Parsing Content

```python
from earthquakes_parser import ContentParser, CSVStorage

# Initialize parser with LLM
parser = ContentParser(model_name="google/flan-t5-large")
storage = CSVStorage()

# Parse URLs from CSV
results = parser.parse_csv("web_results.csv")

# Save parsed content
storage.save_records(results, "parsed_content.json")
```

### Using Supabase Storage (Recommended)

```python
from earthquakes_parser import SupabaseStorage

# Initialize Supabase storage (uses SUPABASE_URL and SUPABASE_KEY env vars)
storage = SupabaseStorage()

# Save search results to database
inserted_ids = storage.save_search_results(results_df)

# Check if URL exists (deduplication)
if not storage.url_exists("https://example.com"):
    # Download and save HTML to storage
    storage.save_html_to_storage(html_content, url, search_result_id)

# Get pending URLs for processing
pending_df = storage.get_pending_urls(limit=100)
```

See [docs/SUPABASE_USAGE.md](docs/SUPABASE_USAGE.md) for complete guide.

### Using S3 Storage

```python
from earthquakes_parser.storage.s3_storage import S3Storage

# Initialize S3 storage
storage = S3Storage(bucket_name="my-bucket", prefix="earthquakes")

# Save data to S3
storage.save_dataframe(df, "results.csv")

# Load data from S3
df = storage.load("results.csv")
```

## Project Structure

```text
earthquakes-parser/
├── earthquakes_parser/     # Main library package
│   ├── search/            # Search functionality
│   ├── parser/            # Content parsing
│   └── storage/           # Storage backends (CSV, S3)
├── tests/                 # Test suite
├── sandbox/               # Experimentation area
├── examples/              # Original scripts (preserved)
│   ├── main.py           # Original search script
│   └── test1-1.py        # Original parser script
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── data/                  # Generated data files
├── pyproject.toml        # Project configuration
└── README.md             # This file
```

## Development

### Setting Up Development Environment

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify setup
python scripts/verify_setup.py
```

### Running Tests

```bash
# Run all tests with coverage
uv run pytest

# Run specific test file
uv run pytest tests/test_searcher.py

# Run with verbose output
uv run pytest -v
```

### Code Quality Checks

#### Using Pre-commit Hooks (Recommended)

```bash
# Run all quality checks automatically
pre-commit run --all-files

# Runs: black, isort, flake8, bandit, and more
```

#### Manual Checks

```bash
# Format code with black
uv run black earthquakes_parser tests

# Sort imports
uv run isort earthquakes_parser tests

# Lint with flake8
uv run flake8 earthquakes_parser tests

# Security check
uv run bandit -r earthquakes_parser

# Check docstring coverage
uv run interrogate earthquakes_parser

# Run all checks
uv run pytest && \
uv run pre-commit run --all-files
```

See [Pre-commit Guide](docs/PRE_COMMIT_GUIDE.md) for detailed information.

### Using the Sandbox

The `sandbox/` directory is for experimentation and testing:

```bash
# Run search example
uv run python sandbox/example_search.py

# Run parser example
uv run python sandbox/example_parser.py
```

## Configuration

### Keywords

Keywords are stored in [config/keywords.txt](config/keywords.txt). One keyword per line:

```text
землетрясение
магнитуда
эпицентр
```

To use custom keywords, create `config/keywords.local.txt` (gitignored) or edit the main file.

See [config/README.md](config/README.md) for more configuration options.

### Environment Variables

#### For Supabase Storage (Recommended)

```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-service-role-key"
```

#### For AWS S3 Storage

```bash
export AWS_ACCESS_KEY_ID=your_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

## CI/CD

The project uses GitHub Actions for continuous integration:

- **Tests**: Run on every push and pull request
- **Linting**: Flake8, isort, black checks
- **Coverage**: Pytest coverage reporting
- **Docs**: Documentation coverage with interrogate

See [.github/workflows/](.github/workflows/) for pipeline configurations.

## Release Process

Releases are managed through GitHub Releases and semantic versioning:

1. Update version in `pyproject.toml`
2. Create a git tag: `git tag v0.1.0`
3. Push tag: `git push origin v0.1.0`
4. GitHub Actions will automatically create a release

See [RELEASE_POLICY.md](RELEASE_POLICY.md) for detailed release guidelines.

## Documentation

- **[Quick Start Guide](docs/QUICK_START.md)** - Get started in 5 minutes
- **[Supabase Usage Guide](docs/SUPABASE_USAGE.md)** - Complete Supabase integration guide
- **[Contributing Guidelines](docs/CONTRIBUTING.md)** - How to contribute
- **[Release Policy](docs/RELEASE_POLICY.md)** - Versioning and releases
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Architecture overview
- **[Setup Complete Guide](docs/SETUP_COMPLETE.md)** - Detailed setup info

## Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed contribution guidelines.

## License

MIT License - see LICENSE file for details

## Credits

Built with:

- [DuckDuckGo Search](https://pypi.org/project/ddgs/) for web searches
- [Trafilatura](https://trafilatura.readthedocs.io/) for content extraction
- [Transformers](https://huggingface.co/transformers/) for LLM-based cleaning
- [uv](https://github.com/astral-sh/uv) for fast package management
