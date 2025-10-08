# EarthquakesParser Documentation

A Python library for searching and parsing earthquake-related content from the web.

## Quick Links

- [🚀 Quick Start Guide](QUICK_START.md) - Get started in 5 minutes
- [🏗️ Project Structure](PROJECT_STRUCTURE.md) - Architecture overview
- [🤝 Contributing](CONTRIBUTING.md) - How to contribute
- [📦 Release Policy](RELEASE_POLICY.md) - Versioning and releases
- [✅ Pre-commit Guide](PRE_COMMIT_GUIDE.md) - Code quality hooks
- [✨ Setup Complete](SETUP_COMPLETE.md) - Detailed setup info

## Features

- 🔍 **Keyword Search** - Search using DuckDuckGo with site filtering
- 📄 **Content Parsing** - Extract and clean web content with LLM
- 💾 **Flexible Storage** - CSV and S3 backends (extensible)
- 🧪 **Well-tested** - Comprehensive test suite with pytest
- 📦 **Modern Tooling** - Uses `uv` for fast dependency management
- 🛡️ **Code Quality** - Pre-commit hooks with black, isort, flake8, bandit

## Installation

### Using uv (recommended)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/yourusername/earthquakes-parser.git
cd earthquakes-parser

# Install with development dependencies
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Using pip

```bash
pip install -e ".[dev]"
```

## Quick Example

### Search for Content

```python
from earthquakes_parser import KeywordSearcher, CSVStorage

# Initialize
searcher = KeywordSearcher(delay=1.0)
storage = CSVStorage(base_path="data")

# Load keywords
keywords = KeywordSearcher.load_keywords_from_file("config/keywords.txt")

# Search
results = searcher.search_to_dataframe(keywords, max_results=5)
storage.save_dataframe(results, "results.csv")
```

### Parse Content

```python
from earthquakes_parser import ContentParser, CSVStorage

# Initialize
parser = ContentParser(model_name="google/flan-t5-large")
storage = CSVStorage()

# Parse URLs
df = storage.load("results.csv")
parsed = parser.parse_dataframe(df)

# Save
storage.save_records(parsed, "parsed_content.json")
```

## Project Structure

```
earthquakes-parser/
├── earthquakes_parser/     # Main library
│   ├── search/            # Search functionality
│   ├── parser/            # Content parsing
│   └── storage/           # Storage backends
├── tests/                 # Test suite
├── config/                # Configuration
├── docs/                  # Documentation
├── examples/              # Original scripts
└── sandbox/               # Experiments
```

## Documentation

### Getting Started

- **[Quick Start Guide](QUICK_START.md)** - 5-minute setup and examples
- **[Installation](../README.md#installation)** - Detailed installation instructions
- **[Examples](../sandbox/)** - Code examples and experiments

### Development

- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute
- **[Project Structure](PROJECT_STRUCTURE.md)** - Architecture and design
- **[Pre-commit Hooks](PRE_COMMIT_GUIDE.md)** - Code quality automation

### Releases

- **[Release Policy](RELEASE_POLICY.md)** - Versioning and release process
- **[Changelog](../CHANGELOG.md)** - Version history

## API Reference

### Search Module

#### KeywordSearcher

```python
from earthquakes_parser import KeywordSearcher

searcher = KeywordSearcher(delay=1.0)
```

**Methods:**
- `search(query, max_results=5, site_filter=None)` - Search for a query
- `search_keywords(keywords, max_results=5, site_filter=None)` - Search multiple keywords
- `search_to_dataframe(keywords, max_results=5, site_filter=None)` - Return as DataFrame
- `load_keywords_from_file(file_path)` - Load keywords from file

### Parser Module

#### ContentParser

```python
from earthquakes_parser import ContentParser

parser = ContentParser(
    model_name="google/flan-t5-large",
    block_size=3000,
    timeout=15
)
```

**Methods:**
- `extract_raw_text(url)` - Extract text with trafilatura
- `clean_with_llm(raw_text)` - Clean text with LLM
- `parse_url(url, query=None)` - Parse single URL
- `parse_dataframe(df, link_column='link', query_column='query')` - Parse DataFrame
- `parse_csv(csv_path)` - Parse from CSV file

### Storage Module

#### CSVStorage

```python
from earthquakes_parser.storage import CSVStorage

storage = CSVStorage(base_path="data")
```

**Methods:**
- `save(data, key)` - Save data
- `load(key)` - Load data
- `exists(key)` - Check if exists
- `save_dataframe(df, key)` - Save DataFrame
- `save_records(records, key)` - Save records
- `append(df, key)` - Append to CSV

#### S3Storage

```python
from earthquakes_parser.storage.s3_storage import S3Storage

storage = S3Storage(bucket_name="my-bucket", prefix="earthquakes")
```

Same methods as CSVStorage, but stores in AWS S3.

## Configuration

### Keywords

Keywords are stored in `config/keywords.txt` (one per line):

```
землетрясение
магнитуда
эпицентр
```

See [config/README.md](../config/README.md) for more configuration options.

### Environment Variables

For S3 storage:

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

## Testing

```bash
# Run all tests
uv run pytest

# With coverage
uv run pytest --cov=earthquakes_parser

# Specific test
uv run pytest tests/test_searcher.py
```

## Code Quality

```bash
# Run pre-commit hooks
pre-commit run --all-files

# Individual tools
uv run black earthquakes_parser tests
uv run isort earthquakes_parser tests
uv run flake8 earthquakes_parser tests
uv run bandit -r earthquakes_parser
```

## CI/CD

GitHub Actions automatically:
- ✅ Run tests on Python 3.9, 3.10, 3.11, 3.12
- ✅ Check code quality (black, isort, flake8)
- ✅ Run security scans (bandit, CodeQL)
- ✅ Generate coverage reports
- ✅ Create releases on tag push

## Support

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/yourusername/earthquakes-parser/issues)
- 💬 [Discussions](https://github.com/yourusername/earthquakes-parser/discussions)

## License

MIT License - see [LICENSE](../LICENSE) for details.

## Credits

Built with:
- [DuckDuckGo Search](https://pypi.org/project/ddgs/)
- [Trafilatura](https://trafilatura.readthedocs.io/)
- [Transformers](https://huggingface.co/transformers/)
- [uv](https://github.com/astral-sh/uv)

---

**[Back to Main README](../README.md)** | **[View on GitHub](https://github.com/yourusername/earthquakes-parser)**
