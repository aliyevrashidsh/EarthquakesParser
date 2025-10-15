# ✅ Pre-commit Hooks Added

## What Was Added

### 1. Pre-commit Configuration

**[.pre-commit-config.yaml](.pre-commit-config.yaml)** - Main config with hooks:

- **Black** - Code formatting
- **isort** - Import sorting
- **Flake8** - Code linting
- **Bandit** - Security scanning
- **detect-secrets** - Credential detection
- **Markdownlint** - Markdown formatting
- File checks (whitespace, line endings, YAML/JSON/TOML validation)

### 2. Configuration Files

- **[.secrets.baseline](.secrets.baseline)** - Secrets detection baseline
- **[.markdownlint.json](.markdownlint.json)** - Markdown linting rules
- Updated **[pyproject.toml](pyproject.toml)** - Added bandit config & pre-commit to dev deps

### 3. Documentation

- **[docs/PRE_COMMIT_GUIDE.md](docs/PRE_COMMIT_GUIDE.md)** - Complete usage guide
- Updated **[README.md](README.md)** - Added pre-commit section

### 4. CI Integration

- Updated **[.github/workflows/ci.yml](.github/workflows/ci.yml)** - Runs pre-commit in CI

## Quick Setup

```bash
# 1. Install dependencies (includes pre-commit)
uv pip install -e ".[dev]"

# 2. Install git hooks
pre-commit install

# 3. (Optional) Run on all files
pre-commit run --all-files
```

## How It Works

### Automatic (On Commit)

```bash
git add .
git commit -m "feat: add feature"

# Pre-commit runs automatically:
# ✅ Format code with black...........Passed
# ✅ Sort imports with isort..........Passed
# ✅ Lint with flake8.................Passed
# ✅ Security check with bandit.......Passed
# ✅ Detect secrets...................Passed
```

### Manual

```bash
# Run all hooks
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
```

## What Each Hook Does

| Hook | Purpose | Auto-fix |
|------|---------|----------|
| **black** | Format Python code | ✅ Yes |
| **isort** | Sort imports | ✅ Yes |
| **flake8** | Lint code (PEP 8) | ❌ No |
| **bandit** | Security scan | ❌ No |
| **detect-secrets** | Find credentials | ❌ No |
| **trailing-whitespace** | Remove trailing spaces | ✅ Yes |
| **end-of-file-fixer** | Add final newline | ✅ Yes |
| **check-yaml** | Validate YAML | ❌ No |
| **check-json** | Validate JSON | ❌ No |
| **check-toml** | Validate TOML | ❌ No |
| **markdownlint** | Lint Markdown | ✅ Yes |

## Benefits

### 🛡️ Prevents Issues Before Commit

- No more "fix linting" commits
- Catches security issues early
- Prevents committing secrets

### 🎨 Consistent Code Style

- Automatic formatting with black
- Sorted imports with isort
- Enforces PEP 8 with flake8

### 🔒 Security

- Scans for common vulnerabilities
- Detects hardcoded secrets
- Prevents private key commits

### 🚀 Faster Reviews

- Code already formatted
- Fewer style comments
- Focus on logic, not style

### ⚙️ CI Integration

- Same checks locally and in CI
- Faster CI (pre-validated)
- Fewer CI failures

## Common Workflows

### First Time Setup

```bash
# Clone and setup
git clone <repo>
cd earthquakes-parser
uv pip install -e ".[dev]"
pre-commit install

# All set! Hooks run on every commit
```

### Daily Development

```bash
# Work on code
vim earthquakes_parser/search/searcher.py

# Commit (hooks run automatically)
git add .
git commit -m "feat: improve search"

# If hooks fail, fix and retry
# Many hooks auto-fix, just re-stage and commit
git add .
git commit -m "feat: improve search"
```

### Before Pull Request

```bash
# Run all checks
pre-commit run --all-files

# Run tests
pytest

# All green? Push!
git push
```

### Emergency Bypass

```bash
# Only when absolutely necessary!
git commit --no-verify -m "emergency: critical fix"
```

## Example: Hooks in Action

### Example 1: Auto-formatting

```bash
# Write unformatted code
echo "x=1+2" >> test.py
git add test.py
git commit -m "add test"

# Black runs and fixes:
# - x=1+2  →  x = 1 + 2
# File auto-staged, commit succeeds
```

### Example 2: Security Caught

```bash
# Hardcode password
echo 'PASSWORD = "secret"' >> config.py  # pragma: allowlist secret
git add config.py
git commit -m "config"

# Bandit fails:
# ❌ Possible hardcoded password string

# Fix it
echo 'PASSWORD = os.getenv("PASSWORD")' > config.py
git add config.py
git commit -m "config"
# ✅ Success!
```

### Example 3: Linting Issue

```bash
# Write code with unused import
echo "import os\nprint('hi')" >> test.py  # pragma: allowlist secret
git add test.py
git commit -m "test"

# Flake8 fails:
# ❌ F401 'os' imported but unused

# Fix it
echo "print('hi')" > test.py
git add test.py
git commit -m "test"
# ✅ Success!
```

## Configuration Locations

| Tool | Config File |
|------|-------------|
| **Pre-commit** | [.pre-commit-config.yaml](.pre-commit-config.yaml) |
| **Black** | [pyproject.toml](pyproject.toml) `[tool.black]` |
| **isort** | [pyproject.toml](pyproject.toml) `[tool.isort]` |
| **Flake8** | [.flake8](.flake8) |
| **Bandit** | [pyproject.toml](pyproject.toml) `[tool.bandit]` |
| **Markdownlint** | [.markdownlint.json](.markdownlint.json) |

## Updating Hooks

```bash
# Update to latest versions
pre-commit autoupdate

# See what changed
git diff .pre-commit-config.yaml

# Commit updates
git add .pre-commit-config.yaml
git commit -m "chore: update pre-commit hooks"
```

## Useful Commands

```bash
# Install hooks
pre-commit install

# Run all hooks
pre-commit run --all-files

# Run specific hook
pre-commit run black

# Update hooks
pre-commit autoupdate

# Bypass (emergency only!)
git commit --no-verify

# Uninstall
pre-commit uninstall
```

## Troubleshooting

### "pre-commit: command not found"

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Or install separately
pip install pre-commit
```

### "Hook failed"

```bash
# See what failed
git status

# Many hooks auto-fix, just re-add
git add .
git commit -m "..."

# Or run manually to see details
pre-commit run --all-files
```

### "Too slow"

```bash
# Skip specific hook temporarily
SKIP=mypy git commit -m "..."

# Or disable in .pre-commit-config.yaml
```

## Resources

- **Full Guide**: [docs/PRE_COMMIT_GUIDE.md](docs/PRE_COMMIT_GUIDE.md)
- **Pre-commit Docs**: <https://pre-commit.com/>
- **Black**: <https://black.readthedocs.io/>
- **Flake8**: <https://flake8.pycqa.org/>
- **Bandit**: <https://bandit.readthedocs.io/>

---

## Your code quality is now protected
