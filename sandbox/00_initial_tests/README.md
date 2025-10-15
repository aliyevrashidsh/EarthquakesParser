# Examples

This directory contains the original scripts and examples for using the EarthquakesParser library.

## Original Scripts

These are the original scripts that were used before the library restructure. They have been preserved and still work:

### [main.py](main.py)

Original search script that:

- Loads keywords from `../keywords.txt`
- Searches Instagram and general web using DuckDuckGo
- Saves results to CSV files in `../data/`

**Usage:**

```bash
cd examples
python main.py
```

### [test1-1.py](test1-1.py)

Original content parser script that:

- Loads URLs from `../data/links.csv`
- Extracts content using trafilatura
- Cleans content with LLM (google/flan-t5-large)
- Saves parsed content to JSON

**Usage:**

```bash
cd examples
python test1-1.py
```

### [requirements.txt](requirements.txt)

Original requirements file (now replaced by `pyproject.toml`)

## Using the Library

For modern usage with the restructured library, see:

- [../sandbox/example_search.py](../sandbox/example_search.py) - New search example
- [../sandbox/example_parser.py](../sandbox/example_parser.py) - New parser example

## Data Files

Generated data files are stored in `../data/`:

- `instagram_links.csv` - Instagram search results
- `links.csv` - General web search results
- `output.json` - Parsed content

## Migration Guide

### Old Way (Original Scripts)

```python
# main.py
with open("keywords.txt", "r") as file:
    keywords = [line.strip() for line in file if line.strip()]

ddgs = DDGS()
for word in keywords:
    results = ddgs.text(f"site:instagram.com {word}")
    # ... manual processing
```

### New Way (Library)

```python
from earthquakes_parser import KeywordSearcher, CSVStorage

searcher = KeywordSearcher()
keywords = KeywordSearcher.load_keywords_from_file("keywords.txt")
results = searcher.search_to_dataframe(
    keywords,
    max_results=5,
    site_filter="instagram.com"
)

storage = CSVStorage()
storage.save_dataframe(results, "instagram_results.csv")
```

## Notes

- Original scripts reference `../keywords.txt` in the root directory
- Data files are saved to/loaded from `../data/` directory
- The library provides the same functionality with better structure and testing
