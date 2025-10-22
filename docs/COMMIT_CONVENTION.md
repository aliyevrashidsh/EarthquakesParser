# Commit Message Convention

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

## Format

```text
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

Must be one of the following:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Code style changes (formatting, missing semi-colons, etc)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Changes to build system or dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

### Scope (Optional)

The scope should be the name of the module affected:

- `parser` - Content parser module
- `search` - Search functionality
- `storage` - Storage backends
- `cli` - Command-line interface
- `deps` - Dependencies
- `config` - Configuration files
- `docs` - Documentation
- `tests` - Test files
- `ci` - CI/CD workflows

### Subject

The subject contains a succinct description of the change:

- Use the imperative, present tense: "change" not "changed" nor "changes"
- Don't capitalize the first letter
- No period (.) at the end
- Maximum 72 characters

### Body (Optional)

The body should include the motivation for the change and contrast with previous behavior.

- Use the imperative, present tense
- Wrap at 72 characters

### Footer (Optional)

The footer should contain:

- **Breaking Changes**: Start with `BREAKING CHANGE:` followed by description
- **Issue References**: `Fixes #123` or `Closes #123, #456`

## Examples

### Simple Feature

```bash
feat(search): add Instagram site filter support

Allow users to filter search results to only show Instagram posts.
```

### Bug Fix

```bash
fix(parser): handle empty content gracefully

Previously, the parser would crash on empty content.
Now it returns None and logs a warning.

Fixes #42
```

### Breaking Change

```bash
feat(storage)!: change CSV backend API

BREAKING CHANGE: CSVStorage.save() now requires a 'key' parameter
instead of inferring the filename from data.

Migration:
  # Before
  storage.save(data)

  # After
  storage.save(data, "results.csv")

Closes #89
```

### Multiple Types

```bash
feat(search): add retry logic for failed searches
test(search): add tests for retry mechanism

Adds exponential backoff retry logic when DuckDuckGo searches fail.
Includes comprehensive test coverage.
```

### Documentation

```bash
docs: update installation instructions

Add instructions for installing with uv package manager.
```

### Chore

```bash
chore(deps): update flake8 to v7.1.0
```

## Commit Message Rules

### ✅ Good Examples

```bash
feat: add earthquake magnitude filter
fix(parser): handle malformed HTML
docs(api): add examples for KeywordSearcher
test: increase coverage for storage module
refactor(search): simplify query builder
perf(parser): optimize content extraction
```

### ❌ Bad Examples

```bash
# Missing type
updated readme

# Capitalized subject
feat: Add new feature

# Period at end
fix: resolve bug.

# Past tense
feat: added search filter

# Too vague
fix: fixes

# Too long subject (> 72 chars)
feat(search): add the ability to search for earthquakes with multiple keywords and filters
```

## Version Bumping Rules

Version bumps are determined automatically based on commit types:

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `fix:` | **PATCH** | 0.1.0 → 0.1.1 |
| `feat:` | **MINOR** | 0.1.0 → 0.2.0 |
| `BREAKING CHANGE:` or `!` | **MAJOR** | 0.1.0 → 1.0.0 |
| Other types | **NO BUMP** | - |

**Important Notes:**

- ✅ **Only `feat:` and `fix:` trigger version bumps**
- ❌ **Other types do NOT bump version** (`docs:`, `style:`, `refactor:`, `test:`, `chore:`, `build:`, `ci:`)
- ⚠️ **Breaking changes always bump MAJOR version**, regardless of type

### Version Bump Examples

```bash
# PATCH: Bug fixes
fix(parser): handle malformed HTML
fix: resolve crash on empty input

# MINOR: New features
feat(search): add Instagram filter
feat: implement retry logic

# MAJOR: Breaking changes
feat(storage)!: change save() API signature
fix!: remove deprecated methods

# Breaking change in body
feat(api): redesign search interface

BREAKING CHANGE: search() now returns iterator instead of list

# NO VERSION BUMP (still included in changelog!)
docs: update API documentation
test: add integration tests
refactor: simplify parser logic
style: format code with black
chore: update dependencies
```

## Why Conventional Commits?

1. **Automatic Changelog Generation**: Generate CHANGELOG.md automatically
2. **Semantic Versioning**: Determine version bumps (major/minor/patch)
3. **Better History**: Easy to understand project history
4. **CI/CD Integration**: Automate releases based on commit types
5. **Filtering**: Easy to filter commits by type

## Tools

### Pre-commit Hook

The project uses a pre-commit hook to validate commit messages:

```bash
# Install pre-commit hooks
pre-commit install --hook-type commit-msg
```

### Manual Validation

You can validate your commit message before committing:

```bash
# Check last commit
git log -1 --pretty=%B | grep -E "^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+"
```

## Commit Message Templates

You can set up a commit message template:

```bash
# Create template
cat > ~/.gitmessage << 'EOF'
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>
#
# Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
# Scope: parser, search, storage, cli, deps, config, docs, tests, ci
#
# Examples:
#   feat(search): add keyword filtering
#   fix(parser): handle empty responses
#   docs: update API documentation
EOF

# Configure git to use it
git config --global commit.template ~/.gitmessage
```

## Branch Naming Convention

Branch names should follow this pattern:

```text
<type>/<description>
```

### Branch Name Examples

```bash
feature/add-instagram-filter
fix/parser-empty-content
docs/update-contributing-guide
refactor/simplify-storage-api
test/increase-parser-coverage
chore/update-dependencies
```

## Release Process

1. Feature development happens in `feature/*` branches
2. Features are merged to `dev` branch via PR
3. When ready for release, merge `dev` to `main`
4. Version is bumped automatically based on commit types
5. CHANGELOG.md is updated automatically
6. GitHub Release is created with tag

### Automatic Version Bumping

Based on commit types:

- `feat`: Bumps **MINOR** version (0.1.0 → 0.2.0)
- `fix`: Bumps **PATCH** version (0.1.0 → 0.1.1)
- `BREAKING CHANGE`: Bumps **MAJOR** version (0.1.0 → 1.0.0)

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
