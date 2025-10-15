# Searcher Manual Testing

This folder contains manual testing scripts for the `KeywordSearcher` functionality.

## Setup

1. Make sure you have the development environment set up:

   ```bash
   # From project root
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e ".[dev]"
   ```

## Running the Tests

### Run All Tests

```bash
# From project root
python experiments/searcher_test/test_searcher_manual.py
```

### What Gets Tested

The script runs 5 different tests:

1. **Basic Search** - Search for a single keyword
2. **Multiple Keywords** - Search for multiple keywords sequentially
3. **Site Filter** - Search only on Instagram
4. **DataFrame Export** - Export results to CSV
5. **Custom Keywords** - Interactive test with your own keywords

## Test Results

Results will be saved to:

```text
experiments/searcher_test/data/
└── test_results.csv
```

## Example Output

```text
============================================================
TEST 1: Basic Search
============================================================

Searching for: землетрясение

Found 3 results:

1. Землетрясения в России
   URL: https://example.com/earthquakes

2. Новости о землетрясениях
   URL: https://example.com/news
...
```

## Notes

- Each test makes real web searches, so it may take time
- Default delay between searches is 1 second to avoid rate limiting
- The script uses DuckDuckGo for searching
- Results are saved to CSV for further analysis

## Customization

You can modify the test script to:

- Change keywords in the tests
- Adjust `max_results` parameter
- Modify the `delay` between searches
- Add additional site filters
- Test different storage backends
