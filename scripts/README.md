# Scripts

Utility scripts for the EarthquakesParser project.

## Available Scripts

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
```
🔍 EarthquakesParser Setup Verification

📁 Checking package structure...
✅ Main package: earthquakes_parser
✅ Search module: earthquakes_parser/search
...

🎉 All checks passed! (24/24)
```

## Running Scripts

### From project root:
```bash
python scripts/verify_setup.py
```

### Make executable (Unix/macOS):
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
