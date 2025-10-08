# Documentation

Complete documentation for the EarthquakesParser project.

## Quick Links

- 📖 **[Main README](../README.md)** - Project overview
- 🚀 **[Quick Start Guide](QUICK_START.md)** - Get started in 5 minutes
- 🏗️ **[Project Structure](PROJECT_STRUCTURE.md)** - Architecture and design
- 🤝 **[Contributing](CONTRIBUTING.md)** - Contribution guidelines
- 📦 **[Release Policy](RELEASE_POLICY.md)** - Versioning and releases
- ✅ **[Setup Complete](SETUP_COMPLETE.md)** - Post-setup guide

## For Users

### Getting Started
1. Start with [Quick Start Guide](QUICK_START.md)
2. Review examples in `../sandbox/` and `../examples/`
3. Check the [Main README](../README.md) for API documentation

### Using the Library

The EarthquakesParser library provides three main modules:

#### Search Module
```python
from earthquakes_parser import KeywordSearcher

searcher = KeywordSearcher()
results = searcher.search("earthquake", max_results=5)
```

See [Quick Start Guide](QUICK_START.md#search-examples) for more examples.

#### Parser Module
```python
from earthquakes_parser import ContentParser

parser = ContentParser()
result = parser.parse_url("https://example.com/article")
```

See [Quick Start Guide](QUICK_START.md#parser-examples) for more examples.

#### Storage Module
```python
from earthquakes_parser.storage import CSVStorage

storage = CSVStorage(base_path="data")
storage.save_dataframe(df, "results.csv")
```

See [Quick Start Guide](QUICK_START.md#storage-examples) for more examples.

## For Developers

### Contributing
Read [Contributing Guidelines](CONTRIBUTING.md) for:
- Setting up development environment
- Code style and quality standards
- Testing requirements
- Pull request process

### Architecture
See [Project Structure](PROJECT_STRUCTURE.md) for:
- Directory layout
- Module descriptions
- Design principles
- Data flow diagrams

### Releases
Check [Release Policy](RELEASE_POLICY.md) for:
- Semantic versioning guidelines
- Release process
- Deprecation policy
- Hotfix procedures

## Project Files

```
docs/
├── README.md              # This file
├── QUICK_START.md         # 5-minute getting started
├── PROJECT_STRUCTURE.md   # Architecture details
├── CONTRIBUTING.md        # Developer guidelines
├── RELEASE_POLICY.md      # Release process
└── SETUP_COMPLETE.md      # Post-setup guide
```

## Additional Resources

- **Examples**: See `../examples/` for original scripts
- **Sandbox**: Check `../sandbox/` for experimentation
- **Tests**: Review `../tests/` for usage patterns
- **Source Code**: Explore `../earthquakes_parser/` for implementation

## External Links

- [Python Packaging Guide](https://packaging.python.org/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [pytest Documentation](https://docs.pytest.org/)
- [Semantic Versioning](https://semver.org/)

## Questions?

- 🐛 **Bug Reports**: Open an issue on GitHub
- 💡 **Feature Requests**: Open an issue with enhancement label
- 💬 **Questions**: Use GitHub Discussions
- 📧 **Private Inquiries**: Contact maintainers

---

**Happy coding!** 🚀
