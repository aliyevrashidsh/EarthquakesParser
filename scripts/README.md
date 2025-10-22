# Scripts

Utility scripts for the EarthquakesParser project.

## Available Scripts

### [bump_version.py](bump_version.py)

Automatically bumps project version and updates CHANGELOG based on conventional commits.

**Usage:**

```bash
# Auto-detect version bump from commits
python scripts/bump_version.py

# Specify bump type manually
python scripts/bump_version.py --type minor

# Dry run (preview changes)
python scripts/bump_version.py --dry-run

# Skip tag creation
python scripts/bump_version.py --no-tag
```

**What it does:**

- Analyzes commits since last tag
- Determines version bump type (major/minor/patch)
- Updates version in `pyproject.toml` and `__init__.py`
- Updates `CHANGELOG.md` with categorized commits
- Creates git tag for new version

**Version bump rules:**

- `feat:` commits → **minor** version bump
- `fix:` commits → **patch** version bump
- `BREAKING CHANGE:` or `!` → **major** version bump

### [verify_setup.py](verify_setup.py)

Verifies that the project is properly set up with all required files and structure.

**Usage:**

```bash
python scripts/verify_setup.py
```

**What it checks:**

- Package structure (earthquakes_parser/, tests/, etc.)
- Configuration files (pyproject.toml, .flake8, etc.)
- Documentation files
- CI/CD workflows
- Module imports (if package is installed)

**Example output:**

```text
🔍 EarthquakesParser Setup Verification

📁 Checking package structure...
✅ Main package: earthquakes_parser
✅ Search module: earthquakes_parser/search
...

🎉 All checks passed! (24/24)
```

## Running Scripts

### From project root

```bash
python scripts/verify_setup.py
```

### Make executable (Unix/macOS)

```bash
chmod +x scripts/verify_setup.py
./scripts/verify_setup.py
```

## Adding New Scripts

When adding utility scripts:

1. Place them in this `scripts/` directory
2. Add a shebang line: `#!/usr/bin/env python3`
3. Document them in this README
4. Make them executable if needed
