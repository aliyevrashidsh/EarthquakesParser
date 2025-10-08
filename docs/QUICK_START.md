# Quick Start Guide

Get up and running with EarthquakesParser in 5 minutes!

## Installation

### 1. Install uv (Fast Package Manager)

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and Set Up

```bash
# Clone the repository
git clone https://github.com/yourusername/earthquakes-parser.git
cd earthquakes-parser

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e ".[dev]"
```

## First Run

### 1. Test the Installation

```bash
# Run tests to verify everything works
uv run pytest
```

### 2. Try the Search Functionality

Create a simple script `my_search.py`:

```python
from earthquakes_parser import KeywordSearcher, CSVStorage

# Initialize
searcher = KeywordSearcher(delay=1.0)
storage = CSVStorage()

# Search
keywords = ["earthquake", "seismic activity"]
results_df = searcher.search_to_dataframe(keywords, max_results=3)

# Save
storage.save_dataframe(results_df, "my_results.csv")
print(f"Found {len(results_df)} results!")
```

Run it:

```bash
uv run python my_search.py
```

### 3. Parse Web Content

Create `my_parser.py`:

```python
from earthquakes_parser import ContentParser, CSVStorage

# Initialize (using smaller model for speed)
parser = ContentParser(model_name="google/flan-t5-small")
storage = CSVStorage()

# Load and parse
results_df = storage.load("my_results.csv")
parsed_content = parser.parse_dataframe(results_df.head(2))  # Parse first 2

# Save
storage.save_records(parsed_content, "parsed_output.json")
print(f"Parsed {len(parsed_content)} pages!")
```

Run it:

```bash
uv run python my_parser.py
```

## Working with the Library

### Search Examples

#### Basic Search

```python
from earthquakes_parser import KeywordSearcher

searcher = KeywordSearcher()
results = searcher.search("earthquake", max_results=5)

for result in results:
    print(f"{result.title}: {result.link}")
```

#### Site-Specific Search

```python
# Search Instagram only
results = searcher.search(
    "earthquake",
    max_results=10,
    site_filter="instagram.com"
)
```

#### Batch Search from File

```python
keywords = KeywordSearcher.load_keywords_from_file("keywords.txt")
df = searcher.search_to_dataframe(keywords, max_results=5)
```

### Parser Examples

#### Parse Single URL

```python
from earthquakes_parser import ContentParser

parser = ContentParser()
result = parser.parse_url(
    "https://example.com/article",
    query="earthquake"
)

print(result["main_text"])
```

#### Parse from DataFrame

```python
import pandas as pd

df = pd.DataFrame({
    "link": ["https://example.com/1", "https://example.com/2"],
    "query": ["earthquake", "seismic"]
})

results = parser.parse_dataframe(df)
```

### Storage Examples

#### CSV Storage

```python
from earthquakes_parser.storage import CSVStorage

storage = CSVStorage(base_path="data")

# Save
storage.save_dataframe(df, "results.csv")

# Load
df = storage.load("results.csv")

# Append
storage.append(new_df, "results.csv")
```

#### S3 Storage (Future)

```python
from earthquakes_parser.storage.s3_storage import S3Storage

storage = S3Storage(bucket_name="my-bucket", prefix="earthquakes")

# Save to S3
storage.save_dataframe(df, "results.csv")

# Load from S3
df = storage.load("results.csv")
```

## Using Original Scripts

The original `main.py` and `test1-1.py` scripts are preserved and still work:

```bash
# Original search script
python main.py

# Original parser script
python test1-1.py
```

## Experiment in Sandbox

The `sandbox/` directory contains examples:

```bash
# Run search example
uv run python sandbox/example_search.py

# Run parser example
uv run python sandbox/example_parser.py
```

## Running Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=earthquakes_parser

# Specific test file
uv run pytest tests/test_searcher.py

# Verbose output
uv run pytest -v
```

## Development Commands

```bash
# Format code
uv run black earthquakes_parser tests

# Sort imports
uv run isort earthquakes_parser tests

# Lint
uv run flake8 earthquakes_parser tests

# Check docstrings
uv run interrogate earthquakes_parser

# Run all checks
uv run pytest && \
uv run flake8 earthquakes_parser tests && \
uv run black --check earthquakes_parser tests && \
uv run isort --check-only earthquakes_parser tests
```

## Next Steps

1. **Read the full documentation**: Check [README.md](README.md)
2. **Explore examples**: Look at files in `sandbox/`
3. **Run original scripts**: Try `main.py` and `test1-1.py`
4. **Customize for your needs**: Modify search parameters, models, etc.
5. **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Common Issues

### Issue: "Module not found"

**Solution**: Ensure you've installed the package in editable mode:

```bash
uv pip install -e .
```

### Issue: "uv: command not found"

**Solution**: Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Issue: Tests fail

**Solution**: Install dev dependencies:

```bash
uv pip install -e ".[dev]"
```

## Getting Help

- 📖 Read [README.md](README.md) for detailed documentation
- 🐛 Report issues on [GitHub Issues](https://github.com/yourusername/earthquakes-parser/issues)
- 💬 Ask questions in [GitHub Discussions](https://github.com/yourusername/earthquakes-parser/discussions)

Happy parsing! 🎉
