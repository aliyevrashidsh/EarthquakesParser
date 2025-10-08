#!/usr/bin/env python
"""Script to verify the project setup is correct."""

import sys
from pathlib import Path


def check_file_exists(path: Path, description: str) -> bool:
    """Check if a file exists."""
    exists = path.exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists


def check_directory_exists(path: Path, description: str) -> bool:
    """Check if a directory exists."""
    exists = path.is_dir()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists


def check_imports() -> bool:
    """Check if main modules can be imported."""
    print("\n📦 Checking imports...")
    all_ok = True

    modules = [
        ("earthquakes_parser", "Main package"),
        ("earthquakes_parser.search", "Search module"),
        ("earthquakes_parser.parser", "Parser module"),
        ("earthquakes_parser.storage", "Storage module"),
    ]

    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✅ {description}: {module_name}")
        except ImportError as e:
            print(f"❌ {description}: {module_name} - {e}")
            all_ok = False

    return all_ok


def main():
    """Run all verification checks."""
    print("🔍 EarthquakesParser Setup Verification\n")

    root = Path(__file__).parent.parent  # Go up from scripts/ to root
    all_checks = []

    # Check core package structure
    print("📁 Checking package structure...")
    all_checks.append(
        check_directory_exists(root / "earthquakes_parser", "Main package")
    )
    all_checks.append(
        check_directory_exists(root / "earthquakes_parser" / "search", "Search module")
    )
    all_checks.append(
        check_directory_exists(root / "earthquakes_parser" / "parser", "Parser module")
    )
    all_checks.append(
        check_directory_exists(
            root / "earthquakes_parser" / "storage", "Storage module"
        )
    )
    all_checks.append(check_directory_exists(root / "tests", "Tests directory"))
    all_checks.append(check_directory_exists(root / "sandbox", "Sandbox directory"))

    # Check key files
    print("\n📄 Checking configuration files...")
    all_checks.append(check_file_exists(root / "pyproject.toml", "Project config"))
    all_checks.append(check_file_exists(root / ".flake8", "Flake8 config"))
    all_checks.append(
        check_file_exists(root / ".python-version", "Python version file")
    )
    all_checks.append(check_file_exists(root / ".gitignore", "Git ignore file"))

    # Check documentation
    print("\n📚 Checking documentation...")
    all_checks.append(check_file_exists(root / "README.md", "Main README"))
    all_checks.append(check_file_exists(root / "docs" / "README.md", "Docs README"))
    all_checks.append(
        check_file_exists(root / "docs" / "QUICK_START.md", "Quick Start")
    )
    all_checks.append(
        check_file_exists(root / "docs" / "CONTRIBUTING.md", "Contributing guide")
    )
    all_checks.append(
        check_file_exists(root / "docs" / "RELEASE_POLICY.md", "Release policy")
    )
    all_checks.append(check_file_exists(root / "CHANGELOG.md", "Changelog"))
    all_checks.append(check_file_exists(root / "LICENSE", "License"))

    # Check CI/CD
    print("\n🔧 Checking CI/CD configuration...")
    all_checks.append(
        check_file_exists(root / ".github" / "workflows" / "ci.yml", "CI workflow")
    )
    all_checks.append(
        check_file_exists(
            root / ".github" / "workflows" / "release.yml", "Release workflow"
        )
    )
    all_checks.append(
        check_file_exists(
            root / ".github" / "workflows" / "codeql.yml", "CodeQL workflow"
        )
    )
    all_checks.append(
        check_file_exists(root / ".github" / "dependabot.yml", "Dependabot config")
    )

    # Check organized directories
    print("\n📂 Checking organized directories...")
    all_checks.append(check_directory_exists(root / "examples", "Examples directory"))
    all_checks.append(check_directory_exists(root / "docs", "Documentation directory"))
    all_checks.append(check_directory_exists(root / "scripts", "Scripts directory"))
    all_checks.append(check_directory_exists(root / "data", "Data directory"))

    # Check original scripts (in examples/)
    print("\n📜 Checking original scripts...")
    all_checks.append(
        check_file_exists(root / "examples" / "main.py", "Original search script")
    )
    all_checks.append(
        check_file_exists(root / "examples" / "test1-1.py", "Original parser script")
    )

    # Check config directory
    print("\n⚙️  Checking configuration...")
    all_checks.append(check_directory_exists(root / "config", "Config directory"))
    all_checks.append(
        check_file_exists(root / "config" / "keywords.txt", "Keywords file")
    )

    # Check imports (only if package is installed)
    try:
        import_ok = check_imports()
        all_checks.append(import_ok)
    except Exception as e:
        print(f"\n⚠️  Import check skipped: {e}")
        print("   Run 'uv pip install -e .' to install the package in development mode")

    # Summary
    print("\n" + "=" * 60)
    passed = sum(all_checks)
    total = len(all_checks)

    if passed == total:
        print(f"🎉 All checks passed! ({passed}/{total})")
        print("\n✨ Your project is properly set up!")
        print("\nNext steps:")
        print("  1. Install dependencies: uv pip install -e '.[dev]'")
        print("  2. Run tests: uv run pytest")
        print("  3. Check QUICK_START.md for usage examples")
        return 0
    else:
        print(f"⚠️  Some checks failed: {passed}/{total} passed")
        print("\n💡 Review the failed checks above and ensure all files are present.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
