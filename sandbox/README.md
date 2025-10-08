# Sandbox

This directory is for experimentation and testing the library functionality.

## Structure

```
sandbox/
├── README.md                    # This file
├── example_search.py            # Search functionality example
├── example_parser.py            # Parser functionality example
├── data/                        # Generated data (gitignored)
└── 01_project_structure/        # Project setup documentation
```

## Examples

### [example_search.py](example_search.py)
Demonstrates keyword searching functionality using the library.

```bash
uv run python sandbox/example_search.py
```

### [example_parser.py](example_parser.py)
Demonstrates content parsing functionality with LLM.

```bash
uv run python sandbox/example_parser.py
```

## Data Directory

Results are saved to `sandbox/data/` directory (gitignored).

## Project Structure Documentation

The [01_project_structure/](01_project_structure/) directory contains:
- Project restructuring documentation
- Setup summaries and guides
- Historical record of organization decisions

See [01_project_structure/README.md](01_project_structure/README.md) for details.

## Creating New Experiments

Use numbered folders for organized experiments:

```
sandbox/
├── 01_project_structure/     # Setup docs
├── 02_async_search/           # Your experiment
├── 03_new_parser/             # Another experiment
└── ...
```

## Adding New Examples

Create new example files following the pattern:

```python
"""Example: Description of what this demonstrates."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from earthquakes_parser import KeywordSearcher, CSVStorage


def main():
    # Your example code here
    pass


if __name__ == "__main__":
    main()
```

## Running Examples

```bash
# From project root
python sandbox/example_search.py
python sandbox/example_parser.py

# Or with uv
uv run python sandbox/example_search.py
```

---

**Happy experimenting! 🎪**
