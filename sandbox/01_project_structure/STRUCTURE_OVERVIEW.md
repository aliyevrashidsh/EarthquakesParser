# 📁 EarthquakesParser - Clean Project Structure

## Root Directory (Clean! 🎉)

```
earthquakes-parser/
├── .flake8                   # Linting configuration
├── .github/                  # CI/CD workflows & templates
├── .gitignore               # Git ignore rules
├── .python-version          # Python version (3.11)
├── CHANGELOG.md             # Version history
├── LICENSE                  # MIT License
├── README.md                # Main documentation
├── pyproject.toml           # Project config & dependencies
│
├── earthquakes_parser/      # 📦 Main library package
│   ├── __init__.py
│   ├── search/              # Search functionality
│   ├── parser/              # Content parsing
│   └── storage/             # Storage backends (CSV/S3)
│
├── tests/                   # 🧪 Test suite
│   ├── test_searcher.py
│   ├── test_parser.py
│   └── test_storage.py
│
├── examples/                # 📜 Original scripts (preserved)
│   ├── README.md
│   ├── main.py             # Original search script
│   ├── test1-1.py          # Original parser script
│   └── requirements.txt    # Old requirements (reference)
│
├── sandbox/                 # 🎪 Experiments & new examples
│   ├── README.md
│   ├── example_search.py
│   └── example_parser.py
│
├── docs/                    # 📚 Documentation
│   ├── README.md
│   ├── QUICK_START.md
│   ├── PROJECT_STRUCTURE.md
│   ├── CONTRIBUTING.md
│   ├── RELEASE_POLICY.md
│   └── SETUP_COMPLETE.md
│
├── scripts/                 # 🛠️ Utility scripts
│   ├── README.md
│   └── verify_setup.py
│
├── data/                    # 💾 Generated data (gitignored)
│   ├── README.md
│   ├── instagram_links.csv  (generated)
│   ├── links.csv           (generated)
│   └── output.json         (generated)
│
└── keywords.txt             # Keywords for searching
```

## Directory Purposes

### 📦 `earthquakes_parser/` - Main Library
The core library code with modular architecture:
- **search/** - Web search using DuckDuckGo
- **parser/** - Content extraction & LLM cleaning
- **storage/** - Abstract storage (CSV, S3)

### 🧪 `tests/` - Test Suite
Comprehensive tests with >80% coverage target:
- Unit tests with mocking
- Integration tests
- pytest configuration in pyproject.toml

### 📜 `examples/` - Original Scripts
Preserved original scripts that still work:
- `main.py` - Search script (updated paths)
- `test1-1.py` - Parser script (updated paths)
- `requirements.txt` - Reference only

### 🎪 `sandbox/` - Experimentation
New library usage examples:
- `example_search.py` - Modern search example
- `example_parser.py` - Modern parser example
- Data saved to `sandbox/data/`

### 📚 `docs/` - Documentation
All documentation in one place:
- Quick start guide
- Contributing guidelines
- Release policy
- Architecture details

### 🛠️ `scripts/` - Utilities
Helper scripts:
- `verify_setup.py` - Setup verification

### 💾 `data/` - Generated Files
Output from searches and parsing:
- CSV files from searches
- JSON files from parsing
- Gitignored (except README)

## Key Benefits

### ✨ Clean Root Directory
- Only essential config files in root
- Everything organized in folders
- Easy to navigate and understand

### 📂 Logical Organization
- Library code separate from examples
- Tests separate from source
- Documentation in one place
- Generated data isolated

### 🔄 Backward Compatible
- Original scripts preserved in `examples/`
- Updated to use new paths (`../data/`, `../keywords.txt`)
- Still fully functional

### 🚀 Future Ready
- Easy to add new modules
- Clear separation of concerns
- Scalable structure

## File Counts

- **Root files**: 8 (config + docs)
- **Library files**: 9 (.py files)
- **Test files**: 4 (.py files)
- **Example files**: 3 (.py + .txt)
- **Documentation**: 6 (.md files in docs/)
- **Total Python files**: 16

## Quick Navigation

| Need | Go To |
|------|-------|
| Use the library | `sandbox/example_*.py` |
| Run original scripts | `examples/main.py` |
| Read documentation | `docs/` or main `README.md` |
| Run tests | `uv run pytest` from root |
| Check setup | `python scripts/verify_setup.py` |
| See generated data | `data/` |

## Commands Reference

```bash
# From project root
python examples/main.py              # Run original search
python examples/test1-1.py           # Run original parser
python sandbox/example_search.py     # Run new search example
python scripts/verify_setup.py       # Verify setup
uv run pytest                        # Run tests
```

---

**Project is now clean, organized, and production-ready! 🎉**
