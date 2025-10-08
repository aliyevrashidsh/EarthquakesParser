# Release Policy

This document outlines the release process and versioning strategy for the EarthquakesParser library.

## Semantic Versioning

We follow [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** version (x.0.0): Incompatible API changes
- **MINOR** version (0.x.0): New functionality in a backwards-compatible manner
- **PATCH** version (0.0.x): Backwards-compatible bug fixes

### Version Guidelines

#### Major Version (Breaking Changes)
- Removal of public APIs
- Changes to existing API signatures
- Major architectural changes
- Removal of deprecated features

#### Minor Version (New Features)
- New features that don't break existing functionality
- New storage backends
- New optional parameters with defaults
- Performance improvements
- Deprecation notices (with backward compatibility)

#### Patch Version (Bug Fixes)
- Bug fixes
- Documentation updates
- Internal refactoring
- Security patches
- Dependency updates (minor/patch)

## Release Process

### 1. Pre-Release Checklist

Before creating a release, ensure:

- [ ] All tests pass: `uv run pytest`
- [ ] Code quality checks pass: `uv run flake8`, `uv run black --check`, `uv run isort --check`
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated with release notes
- [ ] Version is updated in `pyproject.toml`
- [ ] All PRs are merged to `main`

### 2. Creating a Release

#### Step 1: Update Version

Update version in `pyproject.toml`:

```toml
[project]
name = "earthquakes-parser"
version = "0.2.0"  # New version
```

#### Step 2: Update CHANGELOG

Add release notes to `CHANGELOG.md`:

```markdown
## [0.2.0] - 2024-01-15

### Added
- New S3 storage backend
- Batch processing support

### Changed
- Improved error handling in parser

### Fixed
- Bug in keyword loading from file
```

#### Step 3: Commit Changes

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to 0.2.0"
git push origin main
```

#### Step 4: Create Git Tag

```bash
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

#### Step 5: Create GitHub Release

The GitHub Actions workflow will automatically:
1. Run all tests
2. Build the package
3. Create a GitHub Release with the tag
4. Attach build artifacts

Alternatively, create manually:
1. Go to GitHub Releases page
2. Click "Draft a new release"
3. Select the tag (v0.2.0)
4. Add release notes from CHANGELOG
5. Publish release

### 3. Post-Release

After release:
- Announce release in project channels
- Update documentation site (if applicable)
- Monitor for issues

## Release Schedule

- **Patch releases**: As needed for critical bugs
- **Minor releases**: Monthly or when significant features are ready
- **Major releases**: Annually or when breaking changes are necessary

## Deprecation Policy

When deprecating features:

1. Add deprecation warning in code
2. Document in CHANGELOG under "Deprecated"
3. Maintain backward compatibility for at least 2 minor versions
4. Remove in next major version

Example:

```python
import warnings

def old_function():
    warnings.warn(
        "old_function is deprecated and will be removed in v2.0.0. "
        "Use new_function instead.",
        DeprecationWarning,
        stacklevel=2
    )
    # ... implementation
```

## Hotfix Process

For critical bugs in production:

1. Create hotfix branch from release tag:
   ```bash
   git checkout -b hotfix/v0.1.1 v0.1.0
   ```

2. Fix the bug and update version to patch level

3. Create PR to main

4. After merge, create new tag:
   ```bash
   git tag -a v0.1.1 -m "Hotfix: critical bug"
   git push origin v0.1.1
   ```

## Release Artifacts

Each release includes:
- Source distribution (`.tar.gz`)
- Wheel distribution (`.whl`)
- Release notes
- CHANGELOG section for the version

## Rollback Procedure

If a release has critical issues:

1. Document the issue in GitHub Issues
2. Create hotfix or revert changes
3. Release new patch version
4. Update release notes with known issues
5. Consider yanking problematic release from PyPI (if published)

## Long-Term Support (LTS)

- Current major version: Full support
- Previous major version: Security fixes for 6 months
- Older versions: No support

## Questions?

For questions about the release process, open an issue or contact the maintainers.
