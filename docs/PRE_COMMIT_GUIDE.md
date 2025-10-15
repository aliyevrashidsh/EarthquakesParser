# Pre-commit Hooks Guide

Pre-commit hooks automatically check your code quality before each commit,
ensuring consistent code standards across the project.

## What Are Pre-commit Hooks?

Pre-commit hooks run automatically before `git commit` to:

- Format code with **black**
- Sort imports with **isort**
- Lint code with **flake8**
- Check for security issues with **bandit**
- Detect secrets and credentials
- Fix trailing whitespace and line endings
- Validate YAML, JSON, and TOML files
- Lint Markdown files

## Installation

### 1. Install Pre-commit

```bash
# Already included in dev dependencies
uv pip install -e ".[dev]"

# Or install separately
pip install pre-commit
```

### 2. Install Git Hooks

```bash
# Install hooks into your .git/hooks directory
pre-commit install

# Verify installation
pre-commit --version
```

### 3. (Optional) Install for Commit Messages

```bash
# Also check commit messages
pre-commit install --hook-type commit-msg
```

## Usage

### Automatic Checks (on commit)

Once installed, hooks run automatically:

```bash
git add .
git commit -m "feat: add new feature"

# Pre-commit hooks run automatically:
# ✅ Trim trailing whitespace............................Passed
# ✅ Fix end of files....................................Passed
# ✅ Check YAML..........................................Passed
# ✅ Format code with black..............................Passed
# ✅ Sort imports with isort.............................Passed
# ✅ Lint with flake8....................................Passed
# ✅ Security check with bandit..........................Passed
```

### Manual Checks

Run hooks manually on all files:

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
pre-commit run flake8 --all-files

# Run on specific files
pre-commit run --files earthquakes_parser/search/searcher.py
```

### Bypassing Hooks (Emergency Only)

For urgent commits, bypass hooks (use sparingly!):

```bash
# Skip all pre-commit hooks
git commit --no-verify -m "emergency fix"

# Or use environment variable
SKIP=flake8 git commit -m "skip flake8 only"
```

## What Each Hook Does

### Code Quality

**Black** - Code formatter

```text
Formats Python code to consistent style
Line length: 88 characters
Automatically fixes issues
```

**isort** - Import sorter

```text
Sorts and organizes imports
Groups: stdlib, third-party, local
Compatible with black
```

**Flake8** - Code linter

```text
Checks code style (PEP 8)
Detects common bugs
Enforces best practices
```

### Security

**Bandit** - Security scanner

```text
Scans for common security issues
Checks for hardcoded passwords
Detects SQL injection risks
Finds insecure functions
```

**detect-secrets** - Credential scanner

```text
Prevents committing secrets
Detects API keys, passwords
Checks base64 encoded strings
Finds JWT tokens
```

**detect-private-key** - SSH key scanner

```text
Prevents committing private keys
Detects RSA, DSA, EC keys
Finds PEM files
```

### File Checks

**trailing-whitespace** - Removes trailing spaces

**end-of-file-fixer** - Ensures newline at end of file

**mixed-line-ending** - Fixes CRLF/LF issues

**check-merge-conflict** - Detects merge conflict markers

### Syntax Validation

**check-yaml** - Validates YAML files

**check-json** - Validates JSON files

**check-toml** - Validates TOML files

### Markdown

**markdownlint** - Lints and fixes Markdown

```text
Checks markdown syntax
Fixes common issues
Enforces consistent style
```

## Configuration

### Pre-commit Config

Edit [.pre-commit-config.yaml](../.pre-commit-config.yaml):

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        args: ['--line-length=88']
```

### Tool-specific Configs

- **Black/isort**: [pyproject.toml](../pyproject.toml)
- **Flake8**: [.flake8](../.flake8)
- **Bandit**: [pyproject.toml](../pyproject.toml) `[tool.bandit]`
- **Markdownlint**: [.markdownlint.json](../.markdownlint.json)

## Updating Hooks

```bash
# Update to latest versions
pre-commit autoupdate

# Clean hook cache
pre-commit clean

# Reinstall hooks
pre-commit install --install-hooks
```

## Troubleshooting

### Hook fails on commit

```bash
# See what failed
git status

# Fix automatically (if possible)
pre-commit run --all-files

# Check specific file
pre-commit run --files path/to/file.py
```

### Black/Flake8 conflict

Black and flake8 are configured to work together:

- Line length: 88 (black default)
- Flake8 ignores: E203, W503 (black-compatible)

### Import errors in hooks

```bash
# Reinstall dev dependencies
uv pip install -e ".[dev]"

# Reinstall hooks
pre-commit install --install-hooks
```

### Slow hooks

```bash
# Skip slow hooks temporarily
SKIP=mypy git commit -m "message"

# Or comment out in .pre-commit-config.yaml
```

## CI Integration

Pre-commit hooks also run in CI pipeline ([.github/workflows/ci.yml](../.github/workflows/ci.yml)):

```yaml
- name: Run pre-commit hooks
  run: pre-commit run --all-files
```

## Best Practices

### 1. Install Early

```bash
# Right after cloning
git clone <repo>
cd earthquakes-parser
pre-commit install
```

### 2. Run Before Push

```bash
# Check everything before pushing
pre-commit run --all-files
git push
```

### 3. Keep Updated

```bash
# Update monthly
pre-commit autoupdate
```

### 4. Don't Bypass Without Reason

```bash
# ❌ Bad: Bypass to avoid fixing issues
git commit --no-verify

# ✅ Good: Fix issues, then commit
pre-commit run --all-files
# Fix any issues
git commit
```

### 5. Configure for Your Needs

```bash
# Disable specific hooks if needed
# Edit .pre-commit-config.yaml
```

## Examples

### Example 1: Fixing Code Style

```bash
# Make changes
echo "x=1+2" >> earthquakes_parser/example.py

# Try to commit
git add .
git commit -m "add example"

# Black reformats: x = 1 + 2
# Isort organizes imports
# Auto-fixed and staged

# Commit succeeds
```

### Example 2: Security Issue Caught

```bash
# Add code with hardcoded password
echo 'password = "secret123"' >> config.py  # pragma: allowlist secret

# Try to commit
git commit -m "add config"

# Bandit detects: Possible hardcoded password
# Commit blocked

# Fix issue
echo 'password = os.getenv("PASSWORD")' > config.py  # pragma: allowlist secret
git commit -m "add config"
# Success!
```

### Example 3: Manual Check

```bash
# Check all files manually
pre-commit run --all-files

# Fix any issues
# Commit when all pass
```

## Useful Commands

```bash
# Install
pre-commit install

# Run all hooks
pre-commit run --all-files

# Run specific hook
pre-commit run black

# Update hooks
pre-commit autoupdate

# Uninstall
pre-commit uninstall

# Show installed hooks
pre-commit run --help

# Bypass (emergency)
git commit --no-verify
```

## FAQ

**Q: Do I need to run hooks manually?**

A: No, they run automatically on commit after installation.

**Q: Can I disable a specific hook?**

A: Yes, comment it out in `.pre-commit-config.yaml` or use `SKIP=hook_id`.

**Q: Why did my commit fail?**

A: A hook detected an issue. Check the output and fix it.

**Q: Can hooks modify files?**

A: Yes, some hooks (black, isort) auto-fix files and stage changes.

**Q: Do hooks run in CI?**

A: Yes, configured in `.github/workflows/ci.yml`.

**Q: Are hooks required?**

A: Strongly recommended. Ensures code quality and catches issues early.

## Resources

- [Pre-commit Documentation](https://pre-commit.com/)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)

---

## Pre-commit hooks keep your code clean, secure, and consistent
