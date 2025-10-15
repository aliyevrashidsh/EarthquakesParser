# Changelog

<!-- markdownlint-disable MD024 -->
<!-- MD024: Multiple headings with the same content are allowed in changelog sections -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial library structure with search, parser, and storage modules
- KeywordSearcher for DuckDuckGo-based web searches
- ContentParser for extracting and cleaning web content using LLM
- CSV storage backend
- S3 storage backend (requires boto3)
- Comprehensive test suite with pytest
- Code quality tools: flake8, isort, black, interrogate
- GitHub Actions CI/CD pipelines
- Documentation and examples
- Sandbox directory for experiments

### Changed

- Restructured project as a proper Python library
- Migrated from Poetry to uv for package management

### Fixed

- N/A

## [0.1.0] - 2024-01-XX

### Added

- Initial release of EarthquakesParser library
- Basic search functionality
- Content parsing with trafilatura and LLM
- CSV storage support
- Unit tests
- Documentation
